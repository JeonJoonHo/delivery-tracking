from abc import *
from enum import Enum


class Courier(metaclass=ABCMeta):
    track_id = '송장번호'

    class Status(Enum):
        PENDING = 0  # 상품 준비 중
        TAKE = 1  # 상품 인수
        MOVE = 2  # 이동중
        START = 3  # 배송 출발
        ARRIVE = 4 # 배송 도착
        COMPLETE = 5  # 완료

    def track(self):
        try:
            data = self.delivery_data()
            delivery_info = self.delivery_info(data)
            progresses = self.progress(data)
            info = self.info()

            if delivery_info['status'] == Courier.Status.PENDING.value:
                for progress in progresses['progresses']:
                    delivery_info['status'] = progress['status']

                    if delivery_info['status'] == Courier.Status.COMPLETE.value:
                        break

            return dict(delivery_info, **info, **progresses)
        except Exception as ex:
            print(ex)
            return {}

    @abstractmethod
    def delivery_data(self):
        pass

    @abstractmethod
    def parse_status(self, status):
        pass

    @abstractmethod
    def parse_date(self, date_str):
        pass

    @abstractmethod
    def delivery_info(self, data):
        pass

    @abstractmethod
    def progress(self, data):
        pass

    @abstractmethod
    def info(self):
        return {
            'name': '',
            'tel': ''
        }

    def generate_information_info(self, sender, receiver, status):
        return {
            'track_id': self.track_id,
            'sender': sender,
            'receiver': receiver,
            'status': self.parse_status(status)
        }

    def generate_progress_info(self, date_at, location, status, description):
        return {
            'date_at': date_at,
            'location': location,
            'status': self.parse_status(status),
            'description': description
        }

    @staticmethod
    def clean_string(value):
        try:
            value = value.replace('<br/>', '')
            value = value.replace('\n', '')
            value = value.replace('\t', '')
            value = value.replace('\r', '')
            ' '.join(value.split())
            return value.strip()
        except Exception as ex:
            return ''
