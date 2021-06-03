import os
import pickle
from simple_websocket_server import WebSocketServer, WebSocket
import tensorflow as tf
import numpy as np

lreg = pickle.load(open("./DG.sav",'rb'))
nn = tf.keras.models.load_model('DGNN')
width=10 #static waterway width 

class WebSock(WebSocket):
    def handle(self):
        data = self.data.split('#')
        x = [[float(data[0]),float(data[1])]]
        speed = lreg.predict(x)
        q = (float(data[1]) * float(speed[0]) * width)%100
        tmp = np.array([[q,float(speed[0]), float(data[1])]])
        prediction = nn.predict(tmp)
        print(prediction)
        self.send_message(str(speed[0])+"#"+str(prediction[0][0]))

    def connected(self):
        print(self.address, 'connected')

    def handle_close(self):
        print(self.address, 'closed')




server = WebSocketServer('', 1235, WebSock)
server.serve_forever()