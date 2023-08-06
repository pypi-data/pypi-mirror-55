import datetime
from requester.profession import NiceRequester
from requester.nirvana import NirvanaRequester
from utils.dateutils import datetime2str_z, str2datetime


class AttendanceStatus(object):
    STATUS_NO_SIGN = 1
    STATUS_ABSENCE = 2
    STATUS_ATTENDANCE = 3
    STATUS_LATER = 4
    STATUS_EARLIER = 5

    MESSAGE = {
        STATUS_NO_SIGN: "未打卡",
        STATUS_ABSENCE: "请假",
        STATUS_ATTENDANCE: "正常出勤",
        STATUS_LATER: '迟到',
        STATUS_EARLIER: '早退',
    }


def upload_student_attendance(content):
    attendance_id, school_id = content['attendance_id'], content['school_id']
    nirvana_requester = NirvanaRequester(school_id=school_id)
    attendance_data = nirvana_requester.get_student_attendance_info(attendance_id)
    record_time = attendance_data['record_time']
    if not record_time:
        return
    record_time = str2datetime(record_time)
    checking_time = datetime2str_z(record_time - datetime.timedelta(hours=8))
    school_data = nirvana_requester.get_school_info(school_id)
    student_data = nirvana_requester.get_student_info(content['student_id'])
    attendance_data = {"checkingTime": checking_time, "studentEID": student_data['number'],
                       "locationID": attendance_data['classroom']['num'],
                       "cardID": student_data['ecard']['sn'],
                       "checkingStatus": AttendanceStatus.MESSAGE[attendance_data['status']]}
    data = {"schoolID": school_data['code'], "data": [attendance_data], "serial": 0}
    nice_requester = NiceRequester()
    nice_requester.upload_attendance(data)
