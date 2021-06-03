import os
import pickle
#from sklearn.linear_model import LinearRegression


x = [[23,25],[50,43],[40,18]]

model = "./DG.sav"

if os.path.getsize(model)>0:
	print("file is found")
	with open(model, 'rb') as file:
		print("file loaded")
		reg = pickle.load(file)


		preds = reg.predict(x)
		print(preds)
		# diabetes_y_pred = reg.predict(test['x'])

		# xTest = [[i[1]] for i in test['x']]

		# print(xTest)
		# print(len(test['y']))

		# plt.plot(xTest, diabetes_y_pred, color='blue', linewidth=3)
		# plt.scatter(xTest, test['y'],  color='black')

		# plt.xticks(())
		# plt.yticks(())

		# plt.show()