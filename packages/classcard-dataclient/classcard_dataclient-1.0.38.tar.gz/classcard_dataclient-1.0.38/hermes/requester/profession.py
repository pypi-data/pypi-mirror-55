from requester.base import Requester


class NiceRequester(Requester):
    def __init__(self, *args, **kwargs):
        base_data = kwargs.pop("base_data", {})
        super(NiceRequester, self).__init__(*args, **kwargs)
        self.base_data = {"schoolID": "1499", "login": "banpai_01",
                          "token": "d0df559761fdd8ad0db754def2f56954"}
        self.base_data.update(base_data)

    def check_res(self, data):
        if data['status'] != 'success':
            raise ConnectionError(data['errorMessage'])
        return data['result'], True

    def upload_attendance(self, data={}):
        route = "/classadmin/loadCheckings/"
        data.update(self.base_data)
        res = self._post_method(route, data)
        return res
