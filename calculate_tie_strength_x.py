import glob
import networkx as nx
import pandas as pd
from itertools import combinations
import numpy as np
'''1. calculate new tie_strength'''
# collaborate_patents = pd.read_csv('data/collaboration_patents_all_variables.csv')
# print(collaborate_patents)
# # print(collaborate_patents[collaborate_patents['Bool_collaboration'] == 'Yes'])
# only_collaborated = collaborate_patents[collaborate_patents['Bool_collaboration']=='Yes']
# print(only_collaborated)
# flist = glob.glob('data/psnid_data/accumlate_data/result_co_combine_count_*.csv')
#
#
# appln_l = []
# st_l = []
# wst_l = []
# sp_l = []
# bool_st_l = []
# bool_wst_l = []
#
# j=0
# for i in only_collaborated.index:
#     ids_list = only_collaborated.loc[i, 'INSTITUTION_IDS'].split(';')
#     print(j)
#     j += 1
#     year = str(only_collaborated.loc[i, 'appln_filing_year'])
#     s = 'data/psnid_data/accumlate_data\\result_co_combine_count_{}.csv'.format(year)
#     ind = flist.index(s)-1
#
#     # 之前的网络
#     before_graph = flist[ind]
#
#     thisdata = pd.read_csv(before_graph)
#     thisdata.drop_duplicates(subset=['psn_id1', 'psn_id2', 'count_x'], keep='first')
#
#     xx = np.median(list(thisdata['structural']))    # tie strength的中位数
#     weight_xx = np.median(list(thisdata['weighted_structural']))    # 加权tie strength的中位数
#
#     G = nx.Graph()
#     tup = thisdata[['psn_id1', 'psn_id2', 'count_x']]
#     tup.rename(columns={'count_x': 'count'}, inplace=True)
#     tuples = [tuple(x) for x in tup.values]
#     G.add_weighted_edges_from(tuples)
#     all_nodes = G.nodes
#
#     stl = []
#     wstl = []
#     sp = []
#     bool_stl = []
#     bool_wstl = []
#     for couple in combinations(ids_list, 2):
#         if couple[0] < couple[1]:
#             a = couple[0]
#             b = couple[1]
#         else:
#             b = couple[0]
#             a = couple[1]
#         a = int(a)
#         b = int(b)
#         # 如果某一方不在网络中,赋值为-1
#         if (a not in all_nodes) or (b not in all_nodes):
#             stl.append(-1)
#             wstl.append(-1)
#             sp.append(-1)
#             bool_stl.append(-1)
#             bool_wstl.append(-1)
#             continue
#
#         a_degree = int(G.degree()[a])
#         b_degree = int(G.degree()[b])
#         m = len(list(nx.common_neighbors(G, a, b)))
#
#         # 如果他们没有共同邻居,赋值为0
#         if m == 0:
#             stl.append(0)
#             wstl.append(0)
#             if nx.has_path(G, a, b):
#                 sp.append(nx.shortest_path_length(G, source=a, target=b))
#             else:
#                 sp.append(0)
#             if 0 <= xx:
#                 bool_stl.append('T')
#             else:
#                 bool_stl.append('F')
#             if 0 <= weight_xx:
#                 bool_wstl.append('T')
#             else:
#                 bool_wstl.append('F')
#             continue
#
#         '''真正计算tie strength'''
#         # tie strength
#         direct_tup = tup[((tup['psn_id1'] == a) & (tup['psn_id2'] == b)) | ((tup['psn_id1'] == b) & (tup['psn_id2'] == a))]
#         if len(direct_tup) >= 1:
#             n = b_degree + a_degree - 2
#         else:
#             n = b_degree + a_degree
#
#         structral_tie = m / n
#         stl.append(structral_tie)
#
#         if structral_tie <= xx:
#             bool_stl.append('T')
#         else:
#             bool_stl.append('F')
#
#         # tup.loc[i, 'structural'] = structral_tie
#
#         # 加权的tie strength
#         a_tup = tup[(tup['psn_id1'] == a) | (tup['psn_id2'] == a)]
#         b_tup = tup[(tup['psn_id1'] == b) | (tup['psn_id2'] == b)]
#         sa = sum(list(a_tup['count']))
#         sb = sum(list(b_tup['count']))
#         fenzi = 0
#         for co_node in nx.common_neighbors(G, a, b):
#             a_co = list(tup[((tup['psn_id1'] == a) & (tup['psn_id2'] == co_node)) | (
#                         (tup['psn_id1'] == co_node) & (tup['psn_id2'] == a))]['count'].unique())[0]
#             b_co = list(tup[((tup['psn_id1'] == b) & (tup['psn_id2'] == co_node)) | (
#                         (tup['psn_id1'] == co_node) & (tup['psn_id2'] == b))]['count'].unique())[0]
#             fenzi += a_co
#             fenzi += b_co
#
#         if len(direct_tup) >= 1:
#             mutual = list(direct_tup['count'].unique())[0]
#             weighted_tie_strengh = fenzi / (sa + sb - (2 * mutual))
#         else:
#             weighted_tie_strengh = fenzi / (sa + sb)
#
#         wstl.append(weighted_tie_strengh)
#
#         if weighted_tie_strengh <= weight_xx:
#             bool_wstl.append('T')
#         else:
#             bool_wstl.append('F')
#
#         if nx.has_path(G, a, b):
#             sp.append(nx.shortest_path_length(G, source=a, target=b))
#         else:
#             sp.append(0)
#
#         print('fuck')
#         # tup.loc[i, 'weighted_structural'] = weighted_tie_strengh
#     stl = [str(x) for x in stl]
#     wstl = [str(x) for x in wstl]
#     sp = [str(x) for x in sp]
#     bool_stl = [str(x) for x in bool_stl]
#     bool_wstl = [str(x) for x in bool_wstl]
#
#     appln_l.append(only_collaborated.loc[i, 'focal_aid'])
#     st_l.append(';'.join(stl))
#     wst_l.append(';'.join(wstl))
#     sp_l.append(';'.join(sp))
#     bool_st_l.append(';'.join(bool_stl))
#     bool_wst_l.append(';'.join(bool_wstl))
#
# resres = pd.DataFrame({'focal_aid': appln_l, 'tie_strength': st_l, 'weighted_tie_strengh': wst_l, 'shortest_pathway': sp_l,
#                        'Bool_weak': bool_st_l, 'Bool_weighted_weak': bool_wst_l})
# resres.to_csv('variables_x.csv', index=False)


'''2. 合并数据'''
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


# new = pd.read_csv('variables_x.csv')
# for i in range(len(new)):
#     print(i)
#     al = [float(x) for x in new.loc[i, 'tie_strength'].split(';')]
#     al = [0 if x == -1 else x for x in al]
#     resa = sum(al)/len(al)
#     new.loc[i, 'tie_strength'] = resa
#
#     al = [float(x) for x in new.loc[i, 'weighted_tie_strengh'].split(';')]
#     al = [0 if x == -1 else x for x in al]
#     resa = sum(al)/len(al)
#     new.loc[i, 'weighted_tie_strengh'] = resa
#
#     al = [float(x) for x in new.loc[i, 'shortest_pathway'].split(';')]
#     al = [0 if x == -1 else x for x in al]
#     resa = sum(al)/len(al)
#     new.loc[i, 'shortest_pathway'] = resa
#
#     al = new.loc[i, 'Bool_weak'].split(';')
#     if 'T' in al:
#         new.loc[i, 'Bool_weak'] = 1
#     elif 'F' in al:
#         new.loc[i, 'Bool_weak'] = 0
#     else:
#         new.loc[i, 'Bool_weak'] = 2
#
#     al = new.loc[i, 'Bool_weighted_weak'].split(';')
#     if 'T' in al:
#         new.loc[i, 'Bool_weighted_weak'] = 1
#     elif 'F' in al:
#         new.loc[i, 'Bool_weighted_weak'] = 0
#     else:
#         new.loc[i, 'Bool_weighted_weak'] = 2
#
# new.to_csv('variables_x_new.csv', index=False)


# da = pd.read_csv('回归数据_加入分类weakties.csv')
# print(da)
# new = pd.read_csv('variables_x_new.csv')[['focal_aid', 'tie_strength', 'Bool_weak', 'weighted_tie_strengh', 'Bool_weighted_weak']]
# da = pd.merge(da, new, how='left', left_on='appln_id', right_on='focal_aid')
# da.to_csv('回归数据_all_variables.csv', index=False)

da = pd.read_csv('回归数据_all_variables.csv')
# da.loc[da['Bool_weighted_weak'] == 2, "new_Bool_weighted_weak"] = '弱链接'
da.loc[da['Bool_weighted_weak'] == 1, "new_Bool_weighted_weak"] = '弱链接'
da.loc[da['Bool_weighted_weak'] == 0, "new_Bool_weighted_weak"] = '强链接'


da.to_csv('回归数据.csv', index=False)


# yl = []
# w_num = []
# s_num = []
# oldw_num = []
# olds_num = []
# no_heuo_num = []
# for y, group_data in da.groupby('appln_filing_year'):
#     yl.append(y)
#     w_num.append(len(group_data[group_data['new_Bool_weighted_weak'] == '弱链接']))
#     s_num.append(len(group_data[group_data['new_Bool_weighted_weak'] == '强链接']))
#     oldw_num.append(len(group_data[group_data['Bool_weighted_weak'] == 1]))
#     olds_num.append(len(group_data[group_data['Bool_weighted_weak'] == 0]))
#     no_heuo_num.append(len(group_data[group_data['Bool_weighted_weak'] == 2]))
#
# pd.DataFrame({'年份': yl, '弱链接专利数量': w_num, '强链接专利数量': s_num, 'old弱链接专利数量': oldw_num, 'old强链接专利数量': olds_num, 'old首次':no_heuo_num}).to_excel('数量分布图.xlsx', index=False)

# da = da[da['appln_filing_year'] >= 2000]

rc = {'font.sans-serif': 'SimHei',
      'axes.unicode_minus': False}
sns.set(context='notebook', style='ticks', rc=rc)


print(len(da))
p = sns.boxplot(x=da['new_Bool_weighted_weak'], y=da['d_index'], showfliers=False)
p.set_xlabel("")
p.set_ylabel("颠覆性指数")
plt.show()

p = sns.boxplot(x=da['new_Bool_weighted_weak'], y=da['citation_num'], showfliers=False)
p.set_xlabel("")
p.set_ylabel("专利影响力")
plt.show()

p = sns.boxplot(x=da['new_Bool_weighted_weak'], y=da['docdb_family_size'], showfliers=False)
p.set_xlabel("")
p.set_ylabel("专利市场规模")
plt.show()

da = da[da['appln_filing_year'] >= 2000]

sns.lineplot(x='appln_filing_year', y='d_index', hue='new_Bool_weighted_weak', markers="O", data=da)
plt.show()

sns.lineplot(x='appln_filing_year', y='citation_num', hue='new_Bool_weighted_weak', markers="O", data=da)
plt.show()

sns.lineplot(x='appln_filing_year', y='docdb_family_size', hue='new_Bool_weighted_weak', markers="O", data=da)
plt.show()