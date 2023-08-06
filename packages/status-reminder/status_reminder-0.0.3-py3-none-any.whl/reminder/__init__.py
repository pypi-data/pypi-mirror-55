import json
import logging
from datetime import datetime, timedelta

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

version = "0.0.3"
import_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def send_message(phone_number, sms_code, template_param):
    client = AcsClient('LTAIF9B9RAYsVTLw',
                       'HPkju8B4fIJwQWJIiDLKKDirCiAXsA', 'cn-hangzhou')

    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')  # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')

    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('PhoneNumbers', phone_number)
    request.add_query_param('SignName', "高洪杰")
    request.add_query_param('TemplateCode', sms_code)
    request.add_query_param('TemplateParam', template_param)
    response = client.do_action_with_exception(request)
    return response


class Reminder:
    logger = logging.getLogger(name="ReminderLogger")
    logger.setLevel(logging.INFO)
    stream = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt="%(name)s %(asctime)s %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    stream.setFormatter(formatter)
    logger.addHandler(stream)

    def __init__(self, name, time_interval=timedelta(seconds=60)):
        self.name = name
        self.time_interval = time_interval
        self.records = dict()

    def send_message(self, phone_number, message):
        if not isinstance(phone_number, str) and not isinstance(phone_number, list):
            raise TypeError(
                'phone_number is like "17801016666" or ["17801016666", "17801018888"]')

        if not isinstance(message, str):
            raise TypeError("message shoult be str")

        if len(message) > 20:
            raise ValueError("max length of message is 20")


class TaskReminder(Reminder):
    sms_code = "SMS_176943540"

    def send_message(self, phone_number, current_status):
        super().send_message(phone_number, current_status)
        if not isinstance(phone_number, list):
            phone_number = [phone_number]
        current_time = datetime.now()
        for pn in phone_number:
            if pn in self.records and self.records[pn] - current_time < self.time_interval:
                self.logger.warn(f"Too frequent for phone {pn}")
            else:
                # 默认大家都在文件头import
                template_param = {"name": self.name,
                                "start_time": import_time,
                                "current_state": current_status}
                response = send_message(pn, self.sms_code, json.dumps(template_param))
                self.logger.info(
                    f"seed message response: {str(response, encoding = 'utf-8')}")
                if json.loads(response).get("Code") == "OK":
                    self.records[pn] = current_time


class APIReminder(Reminder):
    sms_code = "SMS_177248371"

    def send_message(self, phone_number, current_status):
        super().send_message(phone_number, current_status)
        if not isinstance(phone_number, list):
            phone_number = [phone_number]
        current_time = datetime.now()
        for pn in phone_number:
            if pn in self.records and self.records[pn] - current_time < self.time_interval:
                self.logger.warn(f"Too frequent for {pn}")
            else:
                # 默认大家都在文件头import
                template_param = {"name": self.name,
                                    "current_time": import_time,
                                    "status": current_status}
                response = send_message(pn, self.sms_code, json.dumps(template_param))
                self.logger.info(
                    f"seed message response: {str(response, encoding = 'utf-8')}")
                if json.loads(response).get("Code") == "OK":
                    self.records[pn] = current_time