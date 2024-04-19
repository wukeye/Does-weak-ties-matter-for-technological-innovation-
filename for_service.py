import glob

import pandas as pd
'''1.找到真正机构合作的专利'''

'''2. prepare complete networks for calculate prior ties'''
import numpy as np
import glob
import networkx as nx
flist = glob.glob('data/psnid_data/psnid_data/*.csv')
flist.sort(key=lambda l: l.split('/')[-1].split('_')[-1].split('.')[0])  # 利用key索引列表中每个元素的第二个位置，并依此排序
print(flist)
complete_data = pd.read_csv(flist[0])
complete_data = complete_data[complete_data['psn_id1'] != complete_data['psn_id2']]
for f in flist[1:]:
    print(f)
    ff_this = f.split('/')[-1]
    print(ff_this)
    da = pd.read_csv(f)
    da = da[da['psn_id1'] != da['psn_id2']]

    complete_data = pd.concat([complete_data, da])
    complete_data = complete_data.groupby(['psn_id1', 'psn_sector1', 'psn_id2', 'psn_sector2'])[['count']].sum()
    complete_data.reset_index(inplace=True)
    print(len(complete_data))
    print(f.split('/')[-1].split('_')[-1].split('.')[0])
    if int(f.split('/')[-1].split('_')[-1].split('.')[0])>=2005:

        G = nx.Graph()
        if 'count_x' in complete_data.columns:
            tup = complete_data[['psn_id1', 'psn_id2', 'count_x']]
            tup.rename(columns={'count_x': 'count'}, inplace=True)
        else:
            tup = complete_data[['psn_id1', 'psn_id2', 'count']]

        print(tup)
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
            print('really_{},totally_{}'.format(str(i), str(len(tup))))
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

        resss.to_csv('data/psnid_data/accumlate_data/{}'.format(ff_this), index = False)

