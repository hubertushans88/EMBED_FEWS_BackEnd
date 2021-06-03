import tensorflow as tf
import random

x = int(input("Number Of Data : "))
data = {'x':[],'y':[]}
test = {'x':[],'y':[]}

for i in range(x):
	start = random.uniform(0,50)
	speed = random.uniform(-1, 1)
	newDataX = [200,speed,start]
	newDataY = 0

	if(speed > 0.5 and start > 40):
		newDataY = 1
	
	data['x'].append(newDataX)
	data['y'].append(newDataY)

for i in range(100):
	start = random.uniform(0,50)
	speed = random.uniform(-1, 1)
	newDataX = [200,speed,start]
	newDataY = 0
	
	if(speed > 0.5 and start > 40):
		newDataY = 1
	
	test['x'].append(newDataX)
	test['y'].append(newDataY)

model = tf.keras.Sequential([
		#Flatten layer take 2D input array and turn it to 1D
		tf.keras.layers.Dense(128, activation="relu",input_shape=(3,)),
		#ReLU Function: ReLU(h) = h if and only if h > 0 otherwise 0
		#The reason we use ReLU here is because it will be faster to process
		#When we use the sigmoid function when we count the derivative the reduce error delta is becoming smaller and smaller for each epoch
		#ReLU hope is that the Reduce error delta keep the same across all epoch making computional much faster
		tf.keras.layers.Dense(128, activation="relu"),
		tf.keras.layers.Dense(128, activation="relu"),
		#Ouput layer
		tf.keras.layers.Dense(1, activation="sigmoid")
	])

optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)

model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])

model.summary()

print(test['x'])

# train model
#history = model.fit(data['x'], data['y'], validation_data=(test['x'],test['y']), batch_size=32, epochs=10)