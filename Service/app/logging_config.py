from pytz import timezone
from datetime import date , datetime

fmt = "%Y-%m-%d"
time_zone = "Asia/Bangkok"  
now_utc = datetime.now(timezone('UTC'))
now_pacific = now_utc.astimezone(timezone("Asia/Bangkok"))
date_folder = now_pacific.strftime(fmt)

dict_config = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '%(asctime)s [%(levelname)s:%(name)s] {%(funcName)s:%(lineno)d} [SYSTEM]:%(message)s',
        },
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'formatter': 'default',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': "log/{}.log".format(date_folder),
            'maxBytes': 10000000,
            'backupCount': 10
        },
        'console': {
            'level': 'DEBUG',
            'formatter': 'default',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'main': {
            'handlers': ["default"],
            'level': 'DEBUG',
        },
        'planner_api': {
            'handlers': ["default"],
            'level': 'DEBUG',
        },
        'planner_controller': {
            'handlers': ["default"],
            'level': 'DEBUG',
        },
        'user_api': {
            'handlers': ["default"],
            'level': 'DEBUG',
        },
    },
    'root': {
        'handlers': ["console"],
        'level': 'DEBUG',
    },
}