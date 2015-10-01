#! /usr/bin/python
# -*- coding: utf-8 -*-

import zmq
from xbee import XBee
import time
import serial

'''
Получение и обработка данных с xDevices 
'''
class xBeeDevices():
    def __init__(self):
        self.PORT = 'COM4'
        self.BAUD_RATE = 9600

        #словарь 'адрес MY : Имя' для xCoordinator'ов
        self.dict_src_addr_coord = {'\x01\x01':'Coordinator (101)'}

        #словарь 'адрес MY : Имя' для xSlave'ов
        self.dict_src_addr_slave = {'\x00\x02':'Slave (2)'}

        #словари для преобразования получаемых данных в удобный вид
        self.dict_names_in_coord = {'dio-0':'IN1', 
                                    'dio-1':'IN2', 
                                    'dio-2':'IN3'}

        self.dict_names_out_coord = {'dio-3':'OUT1', 
                                    'dio-4':'OUT2', 
                                    'dio-5':'OUT3'}

        self.dict_status_in_coord = {True:'OFF', False:'ON'}

        self.dict_status_out_coord = {True:'ON', False:'OFF'}

        self.dict_names_in_slave = {'dio-0':'IN1', 
                                    'dio-1':'IN2', 
                                    'dio-2':'IN3', 
                                    'dio-3':'IN4', 
                                    'dio-4':'IN5', 
                                    'dio-5':'IN6'}

        self.dict_names_out_slave = {'dio-6':'OUT1', 'dio-7':'OUT2'}

        self.dict_names_analog_in_slave = {'adc-0':'ANALOG_IN1', 
                                            'adc-1':'ANALOG_IN2', 
                                            'adc-2':'ANALOG_IN3', 
                                            'adc-3':'ANALOG_IN4', 
                                            'adc-4':'ANALOG_IN5', 
                                            'adc-5':'ANALOG_IN6'}

        self.dict_status_in_slave = {True:'OFF', False:'ON'}

        self.dict_status_out_slave = {True:'ON', False:'OFF'}

        self.dictionary_json = {}

        try:
            self.ser = serial.Serial(self.PORT, self.BAUD_RATE)
            self.xbee = XBee(self.ser, callback=self.message_received)
        except:
            print 'Could not open port ' + self.PORT
        
        
    def message_received(self, data):
        try:
            #Преобразование полученного пакета от xCoordinator'ов в читаемый вид
            if data['id']=='rx_io_data' and data['source_addr'] in self.dict_src_addr_coord:
                self.name = self.dict_src_addr_coord[data['source_addr']]
                self.dictionary_json[self.name]={None : None}
                for i in data['samples'][0]:
                    if i in self.dict_names_in_coord:
                        self.port, self.status = self.dict_names_in_coord[i], self.dict_status_in_coord[data['samples'][0][i]]
                    elif i in self.dict_names_out_coord:
                        self.port, self.status = self.dict_names_out_coord[i], self.dict_status_out_coord[data['samples'][0][i]]
                    self.dictionary_json[self.name][self.port] = self.status
                    #print self.name, self.port, self.status
                del self.dictionary_json[self.name][None]
            
            #Преобразование полученного пакета от xSlave'ов в читаемый вид
            elif data['id']=='rx_io_data' and data['source_addr'] in self.dict_src_addr_slave:
                self.name = self.dict_src_addr_slave[data['source_addr']]
                self.dictionary_json[self.name]={None : None}
                for i in data['samples'][0]:
                    if i in self.dict_names_in_slave:
                        self.port, self.status =  self.dict_names_in_slave[i], self.dict_status_in_slave[data['samples'][0][i]]
                    elif i in self.dict_names_out_slave:
                        self.port, self.status =  self.dict_names_out_slave[i], self.dict_status_out_slave[data['samples'][0][i]]
                    elif i in self.dict_names_analog_in_slave:
                        self.port, self.status =  self.dict_names_analog_in_slave[i], data['samples'][0][i]
                    self.dictionary_json[self.name][self.port] = self.status
                    #print self.name, self.port, self.status
                del self.dictionary_json[self.name][None]
        except:
            print 'Error read packet'    
    

    def message_transmit(self):
        try:
            #Отправка запроса на состояние портов у локального xCoordinator'а
            self.xbee.send('at', frame_id='R', command='IS', parameter=None)
        except:
            print 'Error send message'


#сервер сообщений
zmq_context = zmq.Context()
zmq_socket = zmq_context.socket(zmq.PUB)
zmq_socket.bind("tcp://127.0.0.1:5000")

xbee_devices = xBeeDevices()

while True:
    try:
        xbee_devices.message_transmit()
        #print xbee_devices.dictionary_json
        zmq_socket.send_json(xbee_devices.dictionary_json)
        xbee_devices.dictionary_json.clear()
        time.sleep(1.)
    except KeyboardInterrupt:
        xbee_devices.xbee.halt()
        xbee_devices.ser.close()
        break