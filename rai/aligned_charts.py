import matplotlib.pyplot as plt
import numpy as np

# 创建示例数据
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

# 创建图形和子图
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(10, 8))

# 绘制第一个图表
ax1.plot(x, y1, 'b-', label='sin(x)')
ax1.set_ylabel('sin(x)')
ax1.legend()
ax1.grid(True)

# 绘制第二个图表
ax2.plot(x, y2, 'r-', label='cos(x)')
ax2.set_xlabel('x')
ax2.set_ylabel('cos(x)')
ax2.legend()
ax2.grid(True)

# 调整子图之间的间距
plt.subplots_adjust(hspace=0.1)

# 显示图表
plt.show() 