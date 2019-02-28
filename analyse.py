import pandas as pd
import matplotlib.pyplot as plt
import matplotlib


def calc_data(layer_data, attr, range):
    data = []
    i = 0
    while i < len(range):
        if i == len(range)-1:
            data.append(layer_data[layer_data[attr] >= range[i]].shape[0])
        else:
            data.append(layer_data[(layer_data[attr] >= range[i])
                                   & (layer_data[attr] < range[i+1])].shape[0])
        i += 1
    return data


plt.rcParams['font.family'] = [u'Arial Unicode MS']
data_path = "./data/layer_info.csv"
layer_info = pd.read_csv(data_path)
layer_info['count'] = 1
size_base = 1e6
avg_layer_size = layer_info['size'].mean()/size_base
layer_size_range = [0, 25, 50, 100, 200]
layer_size_range_byte = [t*size_base for t in layer_size_range]
layer_size_data = calc_data(layer_info, 'size', layer_size_range_byte)
# --------------------------绘制单个layer大小的分布图 ---------------------
fig2 = plt.figure(3, dpi=100)
plt.title(u'layer大小分布')
plt.pie(layer_size_data, explode=[0.1, 0.1, 0, 0, 0], autopct='%1.1f%%', labels=[
        u'大于0小于{0}MB'.format(layer_size_range[1]),
        u'大于{0}MB小于{1}MB'.format(layer_size_range[1], layer_size_range[2]),
        u'大{0}MB小于{1}MB'.format(layer_size_range[2], layer_size_range[3]),
        u'大于{0}MB小于{1}MB'.format(layer_size_range[3], layer_size_range[4]),
        u'大于{0}MB'.format(layer_size_range[4])], radius=1)
# ----------------------------------------------------------------------
layer_data = layer_info[['image_id', 'count', 'size']
                        ].groupby(['image_id']).sum().reset_index()
max_layer_count = layer_data['count'].max()  # 70
avg_layer_count = layer_data['count'].mean()
min_layer_count = layer_data['count'].min()  # 1
max_total_layer_size = layer_data['size'].max()/size_base
avg_total_layer_size = layer_data['size'].mean()/size_base
min_total_layer_size = layer_data['size'].min()/size_base
print("\n\nlayer平均大小:{0:.3f}MB\n最大layer层数:{1}\n最小layer层数:{2}\n平均layer层数:{3}\n\
最大image大小:{4:.3f}MB\n最小image大小:{5:.3f}MB\n平均image大小:{6:.3f}MB\n".format(avg_layer_size,
                                                                        max_layer_count,
                                                                        min_layer_count,
                                                                        avg_layer_count,
                                                                        max_total_layer_size,
                                                                        min_total_layer_size,
                                                                        avg_total_layer_size))
count_range = [0, 10, 20, 30]
total_size_range = [0.0, 100, 200, 400, 600]
total_size_range_byte = [t*size_base for t in total_size_range]
count_data = calc_data(layer_data, 'count', count_range)
size_data = calc_data(layer_data, 'size', total_size_range_byte)
# --------------------------绘制镜像包含layer个数的分布图 ---------------------
fig = plt.figure(1, dpi=100)
plt.title(u"镜像layer的个数分布")
plt.pie(count_data, explode=[0.1, 0.1, 0, 0], autopct='%1.1f%%', labels=[
        u'大于0小于10', u'大于10小于20', u'大于20小于30', u'大于30'], radius=1)
# ----------------------------------------------------------------------

# --------------------------绘制镜像大小的分布图 ---------------------
fig2 = plt.figure(2, dpi=100)
plt.title(u'镜像大小分布')
plt.pie(size_data, explode=[0.1, 0.1, 0, 0, 0], autopct='%1.1f%%', labels=[
        u'大于0小于{0}MB'.format(total_size_range[1]),
        u'大于{0}MB小于{1}MB'.format(total_size_range[1], total_size_range[2]),
        u'大{0}MB小于{1}MB'.format(total_size_range[2], total_size_range[3]),
        u'大于{0}MB小于{1}MB'.format(total_size_range[3], total_size_range[4]),
        u'大于{0}MB'.format(total_size_range[4])], radius=1)
# ----------------------------------------------------------------------
plt.show()
