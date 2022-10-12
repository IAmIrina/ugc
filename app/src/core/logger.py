import os
import logging
from logging.config import dictConfig
from logging.handlers import TimedRotatingFileHandler

import ecs_logging
from asgi_correlation_id.context import correlation_id
from asgi_correlation_id.log_filters import CorrelationIdFilter, _trim_string

LOG_FILENAME = os.getenv('LOG_FILENAME', '/var/log/app/logs.json')
LOG_LEVEL =  os.getenv('LOG_LEVEL', 'INFO')

class RequestIdFilter(CorrelationIdFilter):
    def filter(self, record: 'LogRecord') -> bool:
        """
        Attach a request ID to the log record.
        """
        cid = correlation_id.get()
        record.request_id = _trim_string(cid, self.uuid_length)
        return True

LOGGING = {
    'version': 1,
    'filters': {
       'request_id': {
            '()': RequestIdFilter,
            'uuid_length': 32,
       },
    },
    'formatters': {
        'default': {'format': '[%(request_id)s] [%(asctime)s] %(levelname)s in %(module)s: %(message)s'},
        'ecs_logging': {
            '()': ecs_logging.StdlibFormatter,
        },
    },
    'handlers': {
        'default': { 
            'formatter': 'default',
            'class': 'logging.StreamHandler',
            'filters': ['request_id'],
        },
        'web': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': LOG_FILENAME,
            'when': 'h',
            'interval': 1, 
            'backupCount': 5,
            'formatter': 'ecs_logging',
            'filters': ['request_id']
        }
    },
    'root': {
        'level': LOG_LEVEL,
        'handlers': ['web', 'default']
    }
}
