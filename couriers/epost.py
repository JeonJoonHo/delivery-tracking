import datetime
import requests
from bs4 import BeautifulSoup

from couriers.courier import *

class Epost(Courier):

    def __init__(self, track_id):
        self.track_id = track_id

    def delivery_data(self):
        tracking_data = requests.get('https://service.epost.go.kr/trace.RetrieveDomRigiTraceList.comm',
                                     {'sid1': self.track_id})

        return BeautifulSoup(tracking_data.text, 'html.parser')

    def delivery_info(self, data):
        information = data.find_all('table', class_='table_col')[0].find_all('td')

        sender = self.clean_string(information[0].contents[0])
        receiver = self.clean_string(information[1].contents[0])

        status = self.clean_string(information[3].contents[0])

        return self.generate_information_info(sender, receiver, status)

    def progress(self, data):
        progresses = data.find_all('table', class_='table_col')[1].find('tbody').find_all('tr')

        progress_infos = []
        for progress in progresses:
            progress_html = progress.find_all('td')
            date_at = self.parse_date(progress_html[0].text + ' ' + progress_html[1].text)
            location = self.clean_string(progress_html[2].text)
            status = self.clean_string(progress_html[3].text)

            progress_infos.append(self.generate_progress_info(date_at, location, status, ''))

        progress_infos = sorted(progress_infos, key=lambda progress: (progress['date_at']))
        return {'progresses': progress_infos}

    def info(self):
        return {
            'name': '우체국택배',
            'tel': '+8215881300'
        }

    def parse_status(self, status):
        if '집하완료' in status:
            return self.Status.TAKE.value
        elif '배달준비' in status:
            return self.Status.START.value
        elif '배달완료' in status:
            return self.Status.COMPLETE.value
        else:
            return self.Status.MOVE.value

    def parse_date(self, date_str):
        date = datetime.datetime.strptime(date_str, '%Y.%m.%d %H:%M')
        return date.strftime('%m-%d %H:%M')
