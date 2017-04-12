import telnetlib
from bs4 import BeautifulSoup
from urllib import error
import requests
import csv
import os
import re
import time

import Settings


def gethtml(url):
    try:
        html = requests.get(url, headers=Settings.USER_AGENT).content
    except error.URLError as e:
        print("the url is wrong!" + str(e.reason))
        return None
    try:
        bsObj = BeautifulSoup(html, "lxml")
    except AttributeError as e:
        return None
    return bsObj

class ProxyIP():

    def __init__(self, ip, port, type, speed, connect_time):
        self.ip = ip
        self. port = port
        self.type = type
        self.speed = speed
        self.connect_time = connect_time


ip_record = []
for i in range(1, 10):
    url = "http://www.xicidaili.com/nn/" + str(i)
    page = gethtml(url)

    ip_list = page.find_all("table", {"id": "ip_list"})[0].find_all("tr")
    for record in ip_list:
        if record.find_all("td"):
            country = record.find_all("td")[0].get_text()
            ip = record.find_all("td")[1].get_text()
            port = record.find_all("td")[2].get_text()
            type = record.find_all("td")[5].get_text().lower()
            speed = record.find_all("td")[6].find_all("div", {"class": "bar"})[0].attrs["title"].strip("秒")
            connect_time = record.find_all("td")[7].find_all("div", {"class": "bar"})[0].attrs["title"].strip("秒")
            if float(speed) < 2and float(connect_time) < 2:
                time.sleep(0.1)
                proxies = {'http': 'http'+"://"+ip+":"+port}
                try:
                    page = requests.get("http://1212.ip138.com/ic.asp", proxies=proxies, timeout=2)
                except:
                    print("failed to connect")
                else:
                    if page.status_code == 200:
                        ip_ban = ['222.44.86.190', '222.44.86.185']
                        ip_exp = re.compile('\d+\.\d+\.\d+\.\d+')
                        ip_content = ip_exp.findall(BeautifulSoup(page.content, "lxml").get_text())[0]
                        if ip_content not in ip_ban:
                            # ip_record.append(ProxyIP(ip, port, type, speed, connect_time))
                            with open("D:/MyPythonProjects/ip_record.csv", 'a+', newline='') as csvFile:
                                writer = csv.writer(csvFile)
                                if os.path.getsize('D:/MyPythonProjects/ip_record.csv') == 0:
                                    writer.writerow(['ip', 'port', 'type'])
                                else:
                                    writer.writerow([ip, port, type])
