import pickle
import paho.mqtt.client as mqtt
import pymysql
from simple_websocket_server import WebSocketServer, WebSocket
import tensorflow as tf
import numpy as np
import time
import datetime





lreg = pickle.load(open("./DG.sav",'rb'))
nn = tf.keras.models.load_model('DGNN')
width=10 #static waterway width 

nlog={"node1":0, "node2":0, "node3":0}

def on_connect(client, userdata, flags, rc):
    client.subscribe("tugasEmbed")
    client.subscribe("feEmbed")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if msg.topic == "tugasEmbed":
        ts = time.time()
        con = pymysql.connect(host='localhost',user='root',password='',db='sipdba',charset='utf8mb4')
        data = msg.payload.decode('utf-8').split('#')
        print(data)
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        dcurs = pymysql.cursors.DictCursor(con)
        gcurs = pymysql.cursors.DictCursor(con)
        get = "SELECT value FROM measurements WHERE node ='"+data[0]+"' ORDER BY created_at DESC LIMIT 1"
        insert = "INSERT INTO measurements (node, value, created_at) VALUES (%s,%s,%s)"
        gcurs.execute(get)
        dcurs.execute(insert,(data[0],data[1],timestamp))
        con.commit()
        rv = 0
        for x in gcurs:
            rv = x['value']
        gcurs.close()
        dcurs.close()
        y = [[float(rv),float(data[1])]]
        speed = lreg.predict(y)
        tmp = np.array([[100,float(speed[0]), float(data[1])]])
        prediction = nn.predict(tmp)
        pv=prediction[0][0]
        if pv<0.01:
            pv=0.01
        xcurs = pymysql.cursors.DictCursor(con)
        pins = "INSERT INTO predictions (node, value, created_at) VALUES (%s,%s,%s)"
        xcurs.execute(pins, (data[0],pv,timestamp))
        con.commit()
        xcurs.close()
        con.close()
    # elif msg.topic == "feEmbed":
    #     avg = (nlog['node1']+nlog['node2']+nlog['node3'])/3.0
    #     c = avg
    #     if avg<1:
    #         c=1
    #     client.publish("embedRX",c)



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("iotalabs.id", 1883, 60)
client.loop_forever()
