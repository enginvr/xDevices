#! /usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, render_template, request
import zmq

#адрес и порт сервера сообщений ZeroMQ
ZMQ_SUB_ADDR = 'tcp://127.0.0.1:5000'

app = Flask(__name__)


'''
Получение данных от сервера сообщений и отправка клиенту.
Данные в формате JSON, пример:
{Device_1_name : {
                  Port_1_name : Port_1_status, 
                  Port_2_name : Port_2_status}, 
 Device_2_name : {
                  Port_1_name : Port_1_status, 
                  Port_2_name : Port_2_status}

                  }
'''
@app.route('/refresh_data')
def refresh_data():
    context = zmq.Context.instance()
    zmq_sub_sock = context.socket(zmq.SUB)
    zmq_sub_sock.setsockopt(zmq.SUBSCRIBE, '')
    zmq_sub_sock.connect(ZMQ_SUB_ADDR)
    
    poller = zmq.Poller()
    poller.register(zmq_sub_sock, zmq.POLLIN)

    socks = dict(poller.poll(timeout=2000))

    if zmq_sub_sock in socks:
        data = zmq_sub_sock.recv_json()
        return jsonify(data)
    else:
        print 'No data...'


@app.route('/')
def index():
    return render_template('index.html')


def run_serv(zmq_sub_addr):
    ZMQ_SUB_ADDR = zmq_sub_addr
    #web сервер Flask
    app.run(host='127.0.0.2', debug=False, threaded=True)
    

if __name__ == '__main__':
    run_serv(ZMQ_SUB_ADDR)