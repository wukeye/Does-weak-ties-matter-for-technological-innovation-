import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import StandardScaler  # 实现z-score标准化

da = pd.read_csv('sti_data.csv')
data = da[['citation_num', 'd_index', 'docdb_family_size', 'weighted_tie_strengh', 'ipc_distance']] #  'techsum'
data.rename(columns={'d_index':'disruptiveness', 'citation_num': 'impact', 'docdb_family_size': 'lg(market_value)',
                     'weighted_tie_strengh': 'weighted_tie_strength', 'ipc_distance':'knowledge_distance'}, inplace=True) #, 'techsum': 'lg(tech_accum)'

data['lg(market_value)'] = data['lg(market_value)'].apply(np.log1p)
# data['lg(tech_accum)'] = data['lg(tech_accum)'].apply(np.log1p)

# 计算相关矩阵
corr_matrix = data.corr()

# 绘制热力图
sns.heatmap(corr_matrix, annot = True, vmax = 1, square = True, cmap = "Reds")
plt.xticks(rotation=20)

plt.show()


# 定义标准化函数
import numpy as np


def z_score_normalize(data):
    mean = np.mean(data, axis=0)
    std_dev = np.std(data, axis=0)
    normalized_data = (data - mean) / std_dev
    return normalized_data


X_test = data.loc[:, 'weighted_tie_strength'] # 实例化对象
res = z_score_normalize(X_test)
data['weighted_tie_strength'] = res


X_test = data.loc[:, 'knowledge_distance'] # 实例化对象
res = z_score_normalize(X_test)
data['knowledge_distance'] = res

data['interaction_term'] = data['weighted_tie_strength'] * data['knowledge_distance']
# data['interaction_term'] = data['interaction_term'].apply(np.log1p)

# 计算相关矩阵
corr_matrix = data.corr()

# 绘制热力图
sns.heatmap(corr_matrix, annot = True, vmax = 1, square = True, cmap = "Reds")
plt.xticks(rotation=20)

plt.show()

print(da)
print('yes')