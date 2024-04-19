import glob

import pandas as pd
'''1.找到真正机构合作的专利'''
# da = pd.read_csv('data/合作者及其id.csv')
# print(da)
# for i in range(len(da)):
#     aid = str(da.loc[i, 'INSTITUTION_SECTORS'])
#     namel = aid.split(';')
#     idl = str(da.loc[i, 'INSTITUTION_IDS']).split(';')
#
#     name_id_dict = dict()
#     print(i)
#     for ii in range(len(namel)):
#         if (namel[ii] == ' ') or (namel[ii]=='INDIVIDUAL') or (namel[ii]=='UNKNOWN'):
#             continue
#         else:
#             name_id_dict[namel[ii]] = idl[ii]
#
#     if len(name_id_dict) >= 2:
#         da.loc[i, 'colla'] = 'Yes'
#         da.loc[i, 'INSTITUTION_SECTORS'] = ';'.join(list(name_id_dict.keys()))
#         da.loc[i, 'INSTITUTION_IDS'] = ';'.join(list(name_id_dict.values()))
#     else:
#         da.loc[i, 'colla'] = 'No'
#
# da = da[da['colla'] == 'Yes']
# da.to_csv('data/new_collaboration.csv', index=False)      # 所有合作专利
# print(da)


'''2. prepare complete networks for calculate prior ties'''
import numpy as np
import glob
import networkx as nx
flist = glob.glob('data/psnid_data/psnid_data/*.csv')
complete_data = pd.read_csv(flist[0])
complete_data = complete_data[complete_data['psn_id1'] != complete_data['psn_id2']]
for f in flist[1:]:
    print(f)
    da = pd.read_csv(f)
    da = da[da['psn_id1'] != da['psn_id2']]

    complete_data = pd.concat([complete_data, da])
    complete_data = complete_data.groupby(['psn_id1', 'psn_sector1', 'psn_id2', 'psn_sector2'])[['count']].sum()
    complete_data.reset_index(inplace=True)
    print(len(complete_data))

    G = nx.Graph()
    tup = complete_data[['psn_id1', 'psn_id2', 'count']]
    tuples = [tuple(x) for x in tup.values]
    G.add_weighted_edges_from(tuples)
    # print(tuples)

    tup['structural'] = 1000
    tup['weak_ties'] = 0

    tup['weighted_structural'] = 1000
    tup['weighted_weak_ties'] = 0

    tup['new_measure'] = 1000
    tup['new_weak_ties'] = 0

    for i in range(len(tup)):
        a = tup.loc[i, 'psn_id1']
        b = tup.loc[i, 'psn_id2']
        a_degree = int(G.degree()[a])
        b_degree = int(G.degree()[b])
        m = len(list(nx.common_neighbors(G, a, b)))
        n = b_degree+a_degree-m-2
        if n == 0:
            structral_tie = 0
        else:
            structral_tie = m/n
        tup.loc[i, 'structural'] = structral_tie

        # 加权的tie strength
        a_tup = tup[(tup['psn_id1'] == a) | (tup['psn_id2'] == a)]
        b_tup = tup[(tup['psn_id1'] == b) | (tup['psn_id2'] == b)]
        sa = sum(list(a_tup['count']))
        sb = sum(list(b_tup['count']))
        fenzi = 0
        for co_node in nx.common_neighbors(G, a, b):
            a_co = list(tup[((tup['psn_id1'] == a) & (tup['psn_id2'] == co_node)) | ((tup['psn_id1'] == co_node) & (tup['psn_id2'] == a))]['count'].unique())[0]
            b_co = list(tup[((tup['psn_id1'] == b) & (tup['psn_id2'] == co_node)) | ((tup['psn_id1'] == co_node) & (tup['psn_id2'] == b))]['count'].unique())[0]
            fenzi += a_co
            fenzi += b_co
        mutual = list(tup[((tup['psn_id1'] == a) & (tup['psn_id2'] == b)) | ((tup['psn_id1'] == b) & (tup['psn_id2'] == a))]['count'].unique())[0]
        weighted_tie_strengh = fenzi/(sa+sb-(2*mutual))
        tup.loc[i, 'weighted_structural'] = weighted_tie_strengh

        tup.loc[i, 'new_measure'] = (m+1)*tup.loc[i, 'count']

    tup.fillna({'weighted_structural': 0}, inplace=True)

    xx = np.median(list(tup['structural']))
    tup.loc[(tup['structural'] <= xx), 'weak_ties'] = 1

    xxx = np.median(list(tup['weighted_structural']))
    tup.loc[(tup['weighted_structural'] <= xxx), 'weighted_weak_ties'] = 1

    xxxx = np.median(list(tup['new_measure']))
    tup.loc[(tup['new_measure'] <= xxxx), 'new_weak_ties'] = 1

    resss = pd.merge(tup, complete_data, on=['psn_id1', 'psn_id2'])
    print(len(resss[resss['weighted_weak_ties'] == 1]))

    # resss.to_csv('data/psnid_data/accumlate_data/{}'.format(f.split('\\')[-1]), index = False)


'''3. 描述性统计'''
import numpy as np
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt

da = pd.read_csv('data/new_collaboration.csv')
# year-distribution Figure 1
orginial_da = pd.read_csv('data/2015_all_variables.csv')
res = pd.merge(orginial_da, da, how='left', left_on='focal_aid', right_on='appln_id')
print(len(res[res['colla'] == 'Yes']))
res.rename(columns={'colla': 'Bool_collaboration'}, inplace=True)
res.fillna({'Bool_collaboration': 'No'}, inplace=True)
res.to_csv('data/collaboration_patents_all_variables.csv', index=False)
print('fuck')
yearl = []
y_l = []
n_l = []
for year, this_yres in res.groupby('appln_filing_year'):
    co_res = this_yres[this_yres['Bool_collaboration'] == 'Yes']
    no_res = this_yres[this_yres['Bool_collaboration'] == 'No']
    yearl.append(year)
    y_l.append(len(co_res))
    n_l.append(len(no_res))
pd.DataFrame({'year': yearl, 'collaboration_patents': y_l, 'no_collaboration_patents': n_l}).to_csv('data/year_distribution.csv')


# print(res)
# # res = res[res['appln_filing_year'] >= 2000]
#
# # d index
# dindex_s = list(res[res['Bool_collaboration'] == 'Yes']['d_index'])
# print(np.mean(dindex_s))    # 0.18 (近20年)
# dindex_without_s = list(res[res['Bool_collaboration'] == 'No']['d_index'])
# print(np.mean(dindex_without_s))    # 0.12
#
# sample1 = np.asarray(dindex_s)
# sample2 = np.asarray(dindex_without_s)
# # Run a two sample t-test to compare the two samples
# tstat, pval = stats.ttest_ind(a=sample1, b=sample2, alternative="two-sided")
# # Display results
# print("t-stat: {:.2f}   pval: {:.4f}".format(tstat, pval)) # t-stat: 75.34   pval: 0.0000
# sns.lineplot(x='appln_filing_year', y='d_index', hue='Bool_collaboration', markers="O", data=res, legend=True)
#
# plt.show()
#
# print('sucker')
#
# sns.lineplot(x='appln_filing_year', y='citation_num', hue='Bool_collaboration', markers="O", data=res, legend=True)
# plt.show()

'''4. calculate the ties strength for each collaborated patent'''
# only_collborate = res[res['Bool_collaboration'] == 'Yes']
# for i in range(len(only_collborate)):
#     ids = res.loc[i, 'INSTITUTION_IDS'].split(';').sort()
#     year = res.loc[i, 'appln_filing_year']-1
#     prior_linkages = pd.read_csv('data/psnid_data/accumlate_data/result_co_combine_count_{}.csv'.format(str(year)))
#     prior_linkages = prior_linkages[(prior_linkages['psn_id1'] == ids[0]) & (prior_linkages['psn_id2'] == ids[1])]
#     if len(prior_linkages) == 0:
#         res['prior_tie_type'] = 'First collaboration'
#     else:
#         prior_linkages['count'][0]
#     print(prior_linkages)

# control variables:
# references_num; familiy_size; type_dummy; year_dummy; authority_dummy
#　media variable: ipc_recombination ties (同类型 不同类型)