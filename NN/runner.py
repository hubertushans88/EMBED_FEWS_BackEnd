import tensorflow as tf
import numpy as np


nn = tf.keras.models.load_model('./DGNN')

a = np.array([[200,2.56,40]]) #debit,speed,height
x = [200,2.56,40]
print(nn.predict(a))
