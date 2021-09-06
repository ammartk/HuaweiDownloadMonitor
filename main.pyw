import requests
from bs4 import BeautifulSoup
import lxml
import sched, time
from datetime import datetime

datetime_str = '09/19/18 13:55:26'

s = sched.scheduler(time.time, time.sleep)
def getDownloadData(sc):
    response = requests.get('http://192.168.8.1/')
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.select_one('meta[name=csrf_token]')['content']

    headers = {
        '__RequestVerificationToken' : csrf_token
    }
    headers['cookie'] = '; '.join([x.name + '=' + x.value for x in response.cookies])

    newResponse = requests.get('http://192.168.8.1/api/monitoring/traffic-statistics', headers=headers)
    soup = BeautifulSoup(newResponse.content, 'lxml')
    currDownload = int(soup.find('currentdownload').get_text())
    currDownload = currDownload / (1024 * 1024)
    line = str(datetime.today()) + "," + str(currDownload) + " MB \n"
    file = open('data.csv', 'a')
    file.write(line)
    file.close()
    s.enter(300, 1, getDownloadData, (sc,))
s.enter(300, 1, getDownloadData, (s,))
s.run()