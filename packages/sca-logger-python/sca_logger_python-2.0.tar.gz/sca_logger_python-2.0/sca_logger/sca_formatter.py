import datetime
import json
import logging

JSON_LOG_KEYS = ['aws_request_id', 'asctime', 'filename', 'funcName', 'levelname', 'message',
                 'exc_info']


class SCAFormatter(logging.Formatter):
    def __init__(self, config_params: dict, frmt: str):
        super(SCAFormatter, self).__init__(frmt)
        self.config_params = config_params

    def formatTime(self, record: logging.LogRecord, datefmt=None) -> str:
        timestamp = record.created
        py_datetime = datetime.datetime.fromtimestamp(timestamp)
        return py_datetime.isoformat()

    def format(self, record: logging.LogRecord) -> str or dict:
        """
            Calling super() here will format the record and prepends fields like
            asctime etc. It will also serialize the message field into a string.
            marshal_as_json:
                It will log in splunk as JSON. The message is also in JSON if we store the message
                first before invoking super()
            string:
                Format to the desired structure passed in __init__ above.
        """
        if self.config_params['marshal_as_json']:
            response = dict()
            message = getattr(record, 'msg', None)
            response['message'] = message
            for _key in JSON_LOG_KEYS:
                if getattr(record, _key, None):
                    response[_key] = getattr(record, _key)
            response['event'] = getattr(record, 'event', None)
            super(SCAFormatter, self).format(record)
            response['asctime'] = getattr(record, 'asctime', None)
            return response
        else:
            return super(SCAFormatter, self).format(record)
