from sync.student import StudentSync
from sync.teacher import TeacherSync
from sync.clas import ClassSync
from sync.classroom import ClassroomSync
from sync.course import CourseSyncV1
from sync.subject import SubjectSync


def start_sync_v1():
    # teacher_sync = TeacherSync()
    # teacher_sync.start()
    # class_sync = ClassSync()
    # class_sync.start()
    # student_sync = StudentSync(class_entrance=class_sync.class_entrance)
    # student_sync.start()
    # classroom_sync = ClassroomSync()
    # classroom_sync.start()
    # subject_sync = SubjectSync()
    # subject_sync.start()
    course_sync = CourseSyncV1()
    course_sync.start()


if __name__ == '__main__':
    start_sync_v1()
