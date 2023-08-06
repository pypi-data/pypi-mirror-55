from sync import BaseSync
from classcard_dataclient.models.classroom import Classroom
from utils.loggerutils import logging

logger = logging.getLogger(__name__)


class ClassroomSync(BaseSync):
    def sync(self):
        res = self.nice_requester.get_classroom_list()
        res_data = res['locations']
        classroom_list = []
        for rd in res_data:
            try:
                floor = int(rd['building'][-3])
            except (Exception, ):
                floor = None
            classroom = Classroom(number=rd['locationID'], name=rd['locationName'], building=rd['building'],
                                  floor=floor, school=self.school_id)
            classroom_list.append(classroom)
        self.client.create_classrooms(self.school_id, classroom_list)
