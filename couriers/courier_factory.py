from enum import Enum

from .epost import Epost


class CourierFactory:
    courier_code = ''
    track_id = ''

    class CourierCode(Enum):
        EPOST = 'kr_ep'

    class CourierName(Enum):
        EPOST = '우체국택배'

    def __init__(self, courier_code, track_id):
        self.courier_code = courier_code
        self.track_id = track_id

    def build(self):
        courier_codes = {
            self.CourierCode.EPOST.value: Epost(self.track_id),
            self.CourierName.EPOST.value: Epost(self.track_id)
        }

        if self.courier_code not in courier_codes:
            return ""

        return courier_codes[self.courier_code]
