import pandas as pd
import itertools

reg_data = pd.read_csv('回归数据.csv')
print(reg_data)

appln_ipc = pd.read_csv('PHARMACEUTICAL_PATENTS_IPC4LIST.csv')
print(appln_ipc)

merge_result = pd.merge(reg_data, appln_ipc, how='left', on='appln_id')

def square(x):
    ss = ';'.join(list(set(list(x.split(';')))))
    return ss

def sss(x):
    ss = len(list(x.split(';')))
    return ss

merge_result['IPC_LIST'] = merge_result['IPC_LIST'].map(square)

merge_result['number_of_ipc4'] = merge_result['IPC_LIST'].map(sss)
print(merge_result)

ipcsim = pd.read_csv(r'C:\Users\Windows\PycharmProjects\STI 2024 code and data\data\ipc_sim.csv')

ipcsim = ipcsim.set_index('index')

for i in range(len(merge_result)):
    ipclist = str(merge_result.loc[i, 'IPC_LIST']).split(';')
    dis = 0
    j = 0
    for item in itertools.combinations(ipclist, 2):
        if (item[0] in ipcsim.index) and (item[1] in ipcsim.index):
            dis += (2 - (ipcsim.loc[item[0], item[1]] + ipcsim.loc[item[1], item[0]]))/2
            j += 1
    if j != 0:
        dis = dis/j
    merge_result.loc[i, 'ipc_distance'] = dis

merge_result.to_csv('sti_data.csv', index=False)