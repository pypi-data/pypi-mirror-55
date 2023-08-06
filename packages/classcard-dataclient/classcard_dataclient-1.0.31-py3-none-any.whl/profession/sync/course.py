import datetime
from sync import BaseSync
from classcard_dataclient.models.course import CourseV1, CourseTableManagerV1, CourseCategory
from classcard_dataclient.models.schedule import RestSchedule, RestTable, PeriodSet
from utils.code import b64encode
from utils.loggerutils import logging
from utils.dateutils import str2datetime, time2str

logger = logging.getLogger(__name__)


class CourseSyncV1(BaseSync):
    def __init__(self, *args, **kwargs):
        super(CourseSyncV1, self).__init__(*args, **kwargs)
        self.class_member = {}
        self.teach_member = {}
        self.used_course_category = set()
        self.course_map = {}

    def related_member(self):
        res = self.nice_requester.get_student_list()
        res_data = res['studentInfos']
        for rd in res_data:
            student_num, class_num = rd['studentEID'], rd['qualifiedClassID']
            if class_num not in self.class_member:
                self.class_member[class_num] = []
            self.class_member[class_num].append(student_num)
            for teach_num in rd['teachingClassFullIDs']:
                if teach_num not in self.teach_member:
                    self.teach_member[teach_num] = []
                self.teach_member[teach_num].append(student_num)

    def analyse_schedule(self, schedule_info):
        num = schedule_info['timeslotInDay']
        begin_datetime = str2datetime("2019-12-12 {}:00".format(schedule_info['beginTime']))
        end_datetime = begin_datetime + datetime.timedelta(minutes=schedule_info['duration'])
        pre_datetime = begin_datetime - datetime.timedelta(minutes=5)
        schedule_data = {"num": num, "order": num, "start_time": time2str(begin_datetime),
                         "stop_time": time2str(end_datetime), "pre_time": time2str(pre_datetime)}
        return schedule_data

    def create_school_rest_table(self, rest_table, rest_table_info):
        morning_index = rest_table_info['earlyMorningLessons'] + rest_table_info['morningLessons']
        afternoon_index = morning_index + rest_table_info['afternoonLessons']
        for week in (1, rest_table_info['daysPerWeek']):
            for schedule_info in rest_table_info["times"]:
                num = schedule_info['timeslotInDay']
                if num <= morning_index:
                    time_period = PeriodSet.MORNING
                elif num <= afternoon_index:
                    time_period = PeriodSet.AFTERNOON
                else:
                    time_period = PeriodSet.NIGHT
                schedule_data = self.analyse_schedule(schedule_info)
                rest_schedule = RestSchedule(week=week, time_period=time_period, **schedule_data)
                rest_table.add_schedule(rest_schedule)

    def create_course(self, course_schedule, manager, forbidden_category=set()):
        used_category = set()
        category_map = {0: 0, 1: 1, 2: 2}
        for course_info in course_schedule:
            category = category_map.get(course_info['oddDual'], 0)
            if category in forbidden_category:
                continue
            is_walking = course_info['classType'] == "教学班"
            name = course_info['classFullName'] + course_info['subjectName']
            number = "{}-{}".format(course_info['qualifiedClassID'], course_info['subjectID'])
            if number in self.course_map:
                course = self.course_map[number]
            else:
                try:
                    teacher_number = course_info["teachers"][0]["teacherEID"]
                except (Exception,):
                    teacher_number = None
                course_data = {'name': name, 'number': number, 'subject_number': course_info['subjectID'],
                               'classroom_number': course_info['locationID'], 'is_walking': is_walking,
                               "teacher_number": teacher_number, "is_present": False}
                if is_walking:
                    course_data['student_list'] = self.teach_member.get(course_info['qualifiedClassID'], [])
                else:
                    course_data['class_name'] = course_info['qualifiedClassID']
                    course_data['student_list'] = self.class_member.get(course_info['qualifiedClassID'], [])
                course = CourseV1(**course_data)
                self.course_map[number] = course
                manager.add_course(course)
            course.add_position(course_info['timeslot'], course_info['weekDay'])
            used_category.add(category)
        return used_category

    def sync(self):
        res = self.nice_requester.get_table()
        rest_table = RestTable(name="全校作息", number=b64encode("全校作息")[:20])
        rest_table_info = res['timeSettings']
        self.create_school_rest_table(rest_table, rest_table_info)
        self.related_member()
        course_table = CourseTableManagerV1(name=res['semester'], number=b64encode(res['semester'])[:20])
        self.create_course(res['schedule'], course_table, self.used_course_category)
        print(">>> CREATE_REST_TABLE")
        self.client.create_rest_table(self.school_id, rest_table, is_active=True)
        print(">>> CREATE_COURSE_TABLE")
        self.client.create_course_table(self.school_id, course_table, is_active=True)
