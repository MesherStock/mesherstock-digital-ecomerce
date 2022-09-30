from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.files.storage import FileSystemStorage

DEFAULT_FILE_STORAGE = getattr(settings, "DEFAULT_FILE_STORAGE", None)

if DEFAULT_FILE_STORAGE == None:
    raise ImproperlyConfigured("DEFAULT_FILE_STORAGE is not set in seetings.py")


class ProtectedStorage(FileSystemStorage):
    location = DEFAULT_FILE_STORAGE