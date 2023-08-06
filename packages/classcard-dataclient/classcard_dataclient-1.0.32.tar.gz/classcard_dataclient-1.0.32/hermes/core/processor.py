from business.profession import upload_student_attendance


class Processor(object):
    TOPIC_FUNC = {"open/classcard/attendance": "upload_student_attendance"}

    @classmethod
    def distribute(cls, topic, payload):
        if topic in cls.TOPIC_FUNC:
            getattr(cls, cls.TOPIC_FUNC[topic])(payload)

    @staticmethod
    def upload_student_attendance(payload):
        upload_student_attendance(payload)
