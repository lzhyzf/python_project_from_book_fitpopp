import matplotlib.pyplot as plt

squares = [1, 4, 9, 16, 25]
inputs = [1, 2, 3, 4, 5]
plt.plot(inputs, squares, linewidth=5)

#设置图标标题，并给坐标轴加上标签
plt.title('Square Numbers', fontsize=24)
plt.xlabel('Value', fontsize=14)
plt.ylabel('Square of Value', fontsize=14)

#设置刻度标记的大小
plt.tick_params(axis='both', labelsize=14)

plt.show()#打开matplotlib查看器
