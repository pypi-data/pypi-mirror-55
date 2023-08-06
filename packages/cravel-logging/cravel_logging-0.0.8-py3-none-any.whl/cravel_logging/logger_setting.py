import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class logger_setting:
    def __init__(self, filepath, Appname):
        self.LOGGING['handlers']['logfile']['filename'] = filepath
        self.LOGGING['loggers'][Appname] = {
            'handlers': ['console', 'logfile', 'mail_admins'],
            'level': 'DEBUG',
        }

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'standard': {
                'format' : "[cid: %(cid)s][%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
                'datefmt' : "%d/%b/%Y %H:%M:%S"
            },
        },
        'handlers': {
            'logfile': {
                'level':'DEBUG',
                'class':'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(BASE_DIR, 'debug.log'),
                'filters': ['correlation'],
                'maxBytes': 50000,
                'backupCount': 2,
                'formatter': 'standard',
            },
            'console': {
                'level':'INFO',
                'class':'logging.StreamHandler',
                'filters': ['correlation'],
                'formatter': 'standard'
            },
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler',
                'filters': ['require_debug_false'],
                'include_html': True,
            }
        },
        'filters': {
            'correlation': {
                '()': 'cid.log.CidContextFilter'
            },
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse',
            },
        },
        'loggers': {
            'django': {
                'handlers':['console'],
                'propagate': True,
                'level':'WARN',
            },
            'django.db.backends': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': False,
            },
        }
    }