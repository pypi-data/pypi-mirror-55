import os

NICE_PROTOCOL = os.environ.get("NICE_PROTOCOL", "http")
NICE_HOST = os.environ.get("NICE_HOST", "connect.nicezhuanye.com/schoolscheduleserv/integration")

NIRVANA_PROTOCOL = os.environ.get("NICE_PROTOCOL", "http")
NIRVANA_HOST = os.environ.get("NICE_HOST", "edtech-test.h3c.com")
NIRVANA_PORT = int(os.environ.get("NIRVANA_PORT", 14001))
NIRVANA_SCHOOL = os.environ.get("NIRVANA_SCHOOL", "35482fb5-6215-4187-a025-0562819eaef2")
NIRVANA_TOKEN = os.environ.get("NIRVANA_TOKEN", "skeleton gjtxsjtyjsxqsl Z2p0eHNqdHlqc3hxc2w=")

SCHOOL_NAME = os.environ.get("SCHOOL_NAME", "北京好专业考勤管理学校")
