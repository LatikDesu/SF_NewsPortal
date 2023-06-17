import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

logs_dir = os.path.join(BASE_DIR, 'logs_files')
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

for logs in ['errors.log', 'general.log', 'security.log']:
    errors_log_path = os.path.join(logs_dir, logs)
    if not os.path.exists(errors_log_path):
        open(errors_log_path, 'w').close()

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console_debug_formatter': {
            '()': 'colorlog.ColoredFormatter',
            'format': '{log_color} {asctime} {levelname} {message}',
            'style': '{',
        },
        'console_warning_formatter': {
            '()': 'colorlog.ColoredFormatter',
            'format': '{log_color} {asctime} {levelname} {message} {pathname}',
            'style': '{',
        },
        'console_error_critical_formatter': {
            '()': 'colorlog.ColoredFormatter',
            'format': '{log_color} {asctime} {levelname} {message} {pathname} {exc_info}',
            'style': '{',
        },
        'info_to_file_general': {
            '()': 'colorlog.ColoredFormatter',
            'format': '{log_color} {asctime} {levelname} {module} {message}',
            'style': '{',
        }
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'debug_to_console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'console_debug_formatter'
        },
        'warning_to_console': {
            'level': 'WARNING',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'console_warning_formatter'
        },
        'error_to_console': {
            'level': 'ERROR',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'console_error_critical_formatter'
        },
        'info_to_file_general': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'logging.FileHandler',
            'formatter': 'info_to_file_general',
            'filename': 'logs_files/general.log'
        },
        'error_to_file_errors': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'formatter': 'console_error_critical_formatter',
            'filename': 'logs_files/errors.log'
        },
        'info_to_file_security': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'info_to_file_general',
            'filename': 'logs_files/security.log'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'console_debug_formatter'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['debug_to_console', 'warning_to_console', 'error_to_console', 'info_to_file_general'],
            'level': 'DEBUG',
            'propagate': True
        },
        'django.request': {
            'handlers': ['error_to_file_errors', 'mail_admins'],
            'level': 'ERROR',
            'propagate': True
        },
        'django.server': {
            'handlers': ['error_to_file_errors', 'mail_admins'],
            'level': 'ERROR',
            'propagate': True
        },
        'django.template': {
            'handlers': ['error_to_file_errors'],
            'level': 'ERROR',
            'propagate': True
        },
        'django.db.backends': {
            'handlers': ['error_to_file_errors'],
            'level': 'ERROR',
            'propagate': True
        },
        'django.security': {
            'handlers': ['info_to_file_security'],
            'level': 'INFO',
            'propagate': True
        }
    }
}
