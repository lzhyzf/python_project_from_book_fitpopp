import pygal
import matplotlib.pyplot as plt
from die import Die

#创建一个D6骰子，一个D10骰子
die_1 = Die()
die_2 = Die(10)

#掷几次骰子，并将结果存储在一个列表中
results = [die_1.roll() + die_2.roll() for roll_num in range(50000)]

#分析结果
max_result = die_1.num_sides + die_2.num_sides
frequencies = [results.count(value) for value in range(2, max_result+1)]

#对结果进行可视化
hist = pygal.Bar()

hist.title = 'Results of rolling D6 and D10 50000 times'
hist.x_labels = [str(a) for a in range(2, 17)]
hist.x_title = 'Result'
hist.y_title = 'Frequency of Result'

hist.add('D6 + D10', frequencies)
hist.render_to_file('die_visual.svg')

#以点数和为x轴，次数为y轴画一个掷骰子50000次的折线图
plt.plot(hist.x_labels, frequencies, linewidth=0.5)

#设置图标标题，并给坐标轴加上标签
plt.title('Results of rolling D6 and D10 50000 times', fontsize=24)
plt.xlabel('D6+D10', fontsize=14)
plt.ylabel('Frequency', fontsize=14)

#设置刻度标记的大小
plt.tick_params(axis='both', labelsize=14)

#把每个关键点涂成红色
for i in range(2, 17):    
    plt.scatter(i - 2, frequencies[i - 2], c='red', edgecolors='none', s=100)

plt.show()#打开matplotlib查看器
