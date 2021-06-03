import random
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import pickle

x = int(input("Number Of Data : "))
data = {'x':[],'y':[]}
test = {'x':[],'y':[]}

for i in range(x):
	speed = random.uniform(-1, 1)
	start = 1
	step = 0
	while step < 20:
		step+=1
		speed = random.uniform(-1, 1)
		newDataX = [start,start+speed]
		start = start + speed
		data['x'].append(newDataX)
		data['y'].append(speed)

for i in range(1):
	speed = random.random()
	start = 1
	step = 0
	while step < 20:
		step+=1
		speed = random.random()
		newDataX = [start,start+speed]
		start = start + speed
		test['x'].append(newDataX)
		test['y'].append(speed)

reg = LinearRegression().fit(data['x'], data['y'])
print(reg.score(test['x'], test['y']))

diabetes_y_pred = reg.predict(test['x'])

xTest = [[i[1]] for i in test['x']]

print(xTest)
print(len(test['y']))

plt.plot(xTest, diabetes_y_pred, color='blue', linewidth=3)
plt.scatter(xTest, test['y'],  color='black')

plt.xticks(())
plt.yticks(())

plt.show()
pickle.dump(reg, open("Saved Model/DG.sav", 'wb'))