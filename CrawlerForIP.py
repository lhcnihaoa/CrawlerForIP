from lxml import  etree
from bs4 import BeautifulSoup
from urllib import error
import requests
import csv
import os

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

    def __init__(self, ip, port, type):
        self.ip = ip
        self. port = port
        self.type = type



for i in range(1,5):
    url = "http://www.xicidaili.com/nn/1"
    page = gethtml(url)

    ip_list = page.find_all("table", {"id": "ip_list"})[0].find_all("tr")
    ip_record = []
    for record in ip_list:
        if record.find_all("td"):
            country = record.find_all("td")[0].get_text()
            ip = record.find_all("td")[1].get_text()
            port = record.find_all("td")[2].get_text()
            type = record.find_all("td")[5].get_text()

            proxies = {type: ip+port}
            if requests.get("https://www.baidu.com", proxies=proxies).status_code==200:
                ip_record.append(ProxyIP(ip, port, type))
with open("D:/MyPhyonProjects/ip_record.csv", 'a+', newline='') as csvFile:
    writer = csv.writer(csvFile)
    if os.path.getsize('D:/MyPhyonProjects/ip_record.csv') == 0:
        writer.writerow(['ip', 'port', 'type'])
    for record in ip_record:
        writer.writerow([record.ip, record.port, record.type])
