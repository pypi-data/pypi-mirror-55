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

    def get_teach_class_list(self):
        route = "/scheduler/getTeachingClasses/"
        res = self._post_method(route, self.base_data)
        return res

    def get_table(self, current=True):
        route = "/scheduler/getSchedule/" if current else "/scheduler/getNextSchedule/"
        res = self._post_method(route, self.base_data)
        return res

    def get_student_class(self):
        route = "/scheduler/getStudentClasses/"
        res = self._post_method(route, self.base_data)
        return res

    def get_teacher_list(self):
        route = "/scheduler/getTeachers/"
        res = self._post_method(route, self.base_data)
        return res

    def get_class_list(self):
        route = "/scheduler/getClasses/"
        res = self._post_method(route, self.base_data)
        return res

    def get_student_list(self):
        route = "/scheduler/getStudentInfos/"
        res = self._post_method(route, self.base_data)
        return res

    def get_subject_list(self):
        route = "/scheduler/getSubjects/"
        res = self._post_method(route, self.base_data)
        return res

    def get_classroom_list(self):
        route = "/scheduler/getLocations/"
        res = self._post_method(route, self.base_data)
        return res

    def get_school_info(self):
        route = "/scheduler/getSchoolInfo/"
        res = self._post_method(route, self.base_data)
        return res