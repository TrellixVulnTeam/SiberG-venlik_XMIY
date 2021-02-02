import requests
import subprocess
import sqlite3
import datetime
import socket

header={"X-ApiKeys":"accessKey=81f3cc49d00838379cf57b974200d33ebefc88840d0ac7553defd7a03a4523; secretKey=4cbad646e0f9cbb3de329cd02e629ab7bf9a6593e913258492feb95b90a0d36;"}
cikti=subprocess.check_output("dir",shell=True)

if not "host_discovery.db" in str(cikti):
    print("veritabanı yok")
    conn=sqlite3.connect("host_discovery.db")
    c=conn.cursor()
    c.execute('''CREATE TABLE hosts (ip text, zaman text)''')
    c.close()
conn=sqlite3.connect("host_discovery.db")
c=conn.cursor()
c.execute('SELECT ip from hosts')
ipler=c.fetchall()
ipler_liste=[]

for i in ipler:
    ipler_liste.append(str(i[0]))
conn.close()

url="https://192.168.1.100:8834/scans"
sonuc=requests.get(url=url,headers=header,verify=False)

for i in sonuc.json()['scans']:
   if "HD" in i['name'] and "completed" in i['status']:
       url="https://192.168.1.100:8834/scans/"+str(i['id'])
       sonuc=requests.get(url=url,headers=header,verify=False)
       for j in sonuc.json()['hosts']:
           if not j['hostname'] in ipler_liste:
               print("Yeni IP:",j['hostname'])
               conn=sqlite3.connect('host_discovery.db')
               c=conn.cursor()
               c.execute('INSERT INTO hosts values(?,?)',str(j['hostname'],str(datetime.datetime.now())))
               conn.close()
               s=socket.socket()
               s.connect("192.168.1.100",515)
               log="yeni IP bulundu"+str(j['hostname'])
               s.sendall(str(log))
               s.close()
