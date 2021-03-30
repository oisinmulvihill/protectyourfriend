import logging
import logging.config


config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        "ecs": {
            "format": (
                "%(asctime)s %(name)s.%(funcName)s %(levelname)s %(message)s"
            ),
        }
    },
    'handlers': {
        'default': {
            'level': 'NOTSET',
            'formatter': 'ecs',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout'
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True
        },
        'django': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': False
        }
    }
}


def log_setup():
    """Setup logging to console which can be shipped centrally in the env."""
    logging.config.dictConfig(config)
