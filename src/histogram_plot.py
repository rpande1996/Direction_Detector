import matplotlib.pyplot as plt

x = []
y = []

with open('../output/data.txt', 'r') as f:
    data = f.read().split('\n')
    print(data)
    for i in data:
        try:
            y.append(float(i.strip()))
        except:
            continue

x = list(range(len(y)))

print(y)
plt.plot(x, y)
# plt.hist(y, density=True, bins = 50, edgecolor = 'black', linewidth = 1.2)
plt.xlabel('Frame Number')
plt.xlabel('Frame Number')
plt.ylabel('Processing Time')
plt.legend(['Raw Data'])
plt.title('Object Tracking: Processing Time')
plt.savefig('../output/hist.png')
plt.show()