#!/usr/bin/env python3
# -*- coding: utf-8 -*
import os
import requests
import json
from requests.exceptions import ConnectionError

API_BASE_URL = 'https://app-api.niu.com'
ACCOUNT_BASE_URL = 'https://account.niu.com'
TOKEN_FILE = os.sep+"token.json"
SN_FILE = os.sep+"sn.json"

class Scooter:
    def __init__(self, email, passwd,cc="86"):
        #print("init")
        self._token = None
        self._sn = None
        self._batteryInfo = None
        self._motorInfo = None
        self._overallTally = None
        
        try:
            self.get_token(email, passwd,cc)
            #print(self._token)
            self.get_vehicles(self._token)
            #print(self._sn)
        except:
            print("error getting token/sn")

    def load_local_file(self,fn):
        work_path = os.getcwd()
        #print(work_path+fn)
        try:
            with open(work_path+fn) as data_file:
                #print("load:"+work_path+fn)
                return data_file.read()
        except Exception as e:
            print("load fail:"+fn)
            self._token = None
 
    
    def save_local_file(self,fn,content):
        work_path = os.getcwd()
        with open(work_path+fn, 'w') as data_file:
            data_file.write(content)
            
       
    
    def get_token(self,email, password, cc="86"):
        #print("get_token")
        self._token = self.load_local_file(TOKEN_FILE)
        if self._token is None:
            #print("get token from internet")
            url = ACCOUNT_BASE_URL + '/appv2/login'
            data = {'account': email, 'countryCode': cc, 'password': password}
            try:
                r = requests.post(url, data=data)
                data = json.loads(r.content.decode())
                self._token = data['data']['token']
                self.save_local_file(TOKEN_FILE,self._token)
                return self._token
            except BaseException as e:
                print ("Exception")
                raise
    
    
    def get_vehicles(self,token):
        #print("get_sn")
        self._sn = self.load_local_file(SN_FILE)
        if self._sn is None:
            #print("get sn from internet")
            url = API_BASE_URL + '/motoinfo/list'
            headers = {'token': token, 'Accept-Language': 'en-US'}
            try:
                r = requests.post(url, headers=headers, data=[])
                data = json.loads(r.content.decode())
                self._sn = data['data'][0]['sn']
                self.save_local_file(SN_FILE,self._sn)
                return self._sn
            except BaseException as e:
                print ("Exception")
                raise
    
    def get_battery_info(self):
        try:
            data = self.get_info('/v3/motor_data/battery_info', self._sn, self._token)
            
            self._batteryInfo = data['data']['batteries']['compartmentA']
            self._batteryInfo.pop("items")
            '''
            print ('Battery Info:')
            print ('BMS-Id:        ', batteryInfo['bmsId'])
            print ('BatteryCharge: ', batteryInfo['batteryCharging'])
            print ('Is connected:  ', batteryInfo['isConnected'])
            print ('Times charged: ', batteryInfo['chargedTimes'])
            print ('Temperature:   ', batteryInfo['temperature'])
            print ('Battery Grade: ', batteryInfo['gradeBattery'])
            '''
        except Exception as e:
            print("fail to get battery info")
            print(e)
            
    def get_motor_info(self):
        try:
            motorInfo = self.get_info('/v3/motor_data/index_info', self._sn, self._token)
            
            self._motorInfo = motorInfo['data']
            '''
            print ('Motor Info:')
            print ('exp. range:    ', motorInfo['estimatedMileage'])
            print ('current speed: ', motorInfo['nowSpeed'])
            print ('is connected:  ', motorInfo['isConnected'])
            print ('is charging:   ', motorInfo['isCharging'])
            print ('is locked:     ', motorInfo['lockStatus'])
            print ('gsm signal:    ', motorInfo['gsm'])
            print ('gps signal:    ', motorInfo['gps'])
            print ('Time left:     ', motorInfo['leftTime'])
            print ('centreCtrlBatt:', motorInfo['centreCtrlBattery'])
            print ('Position lat:  ', motorInfo['postion']['lat'])
            print ('Position lng:  ', motorInfo['postion']['lng'])
            print ('HDOP:          ', motorInfo['hdop'])
            if (len(motorInfo['data']['lastTrack'])) != 0:
                print ('Last Track:  ')
                print ('  Timestamp:   ', motorInfo['data']['lastTrack']['time'])
                print ('  Distance:    ', motorInfo['data']['lastTrack']['distance'])
                print ('  Riding Time: ', motorInfo['data']['lastTrack']['ridingTime'])
            '''
        except Exception as e:
            print("fail to get battery info")
            print(e)        

    def get_overall_tally(self):
        try:
            overallTally = self.post_info('/motoinfo/overallTally', self._sn, self._token)
            
            self._overallTally = overallTally['data']
            '''
            print ('Total km:      ', overallTally['data']['totalMileage'])
            print ('Total km since:', overallTally['data']['bindDaysCount'], 'days')
            '''
        except Exception as e:
            print("fail to get battery info")
            print(e)
             
            
    def get_info(self,path, sn, token):
        url = API_BASE_URL + path
    #    print (url)
        params = {'sn': sn}
        headers = {'token': token, 'Accept-Language': 'en-US'}
        try:
            r = requests.get(url, headers=headers, params=params)
    #        print (r.content)
    #        print (r.status_code)
        except ConnectionError as e:
            print("Caught Error")
            print(e)
            return False
        if r.status_code != 200:
            return False
        data = json.loads(r.content.decode())
        if data['status'] != 0:
            print (data)
            return False
    #    data = data['data']['batteries']['compartmentA']
    #    del data['items']
        return data
    
    
    def post_info(self,path, sn, token):
        url = API_BASE_URL + path
    #    print (url)
        params = {}
        headers = {'token': token, 'Accept-Language': 'en-US'}
        try:
            r = requests.post(url, headers=headers, params=params, data={'sn':sn})
    #        print (r.content)
    #        print (r.status_code)
        except ConnectionError as e:
            print("Caught Error")
            print(e)
            return False
        if r.status_code != 200:
            return False
        data = json.loads(r.content.decode())
        if data['status'] != 0:
            print (data)
            return False
    #    data = data['data']['batteries']['compartmentA']
    #    del data['items']
        return data
