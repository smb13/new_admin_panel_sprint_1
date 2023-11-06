import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from split_settings.tools import include

load_dotenv()

sys.path.insert(0, os.getenv("ROOT_PATH"))

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = os.environ.get('DEBUG', False) == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(',')

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

include(
    'components/database.py',
    'components/application.py',
    'components/auth_password_validators.py',
)

LOCALE_PATHS = ['movies/locale']

INTERNAL_IPS = [
    "127.0.0.1",
]
