from django.conf import settings
from django.db.models import FileField, ImageField
from django.utils.module_loading import import_string


class ProtectedFileField(FileField):
    def __init__(self, **kwargs):
        # force protected media storage
        if 'storage' in kwargs:
            del kwargs['storage']
        super().__init__(storage=import_string(settings.PROTECTED_MEDIA_STORAGE)(), **kwargs)


class ProtectedImageField(ImageField):
    def __init__(self, **kwargs):
        # force protected media storage
        if 'storage' in kwargs:
            del kwargs['storage']
        super().__init__(storage=import_string(settings.PROTECTED_MEDIA_STORAGE)(), **kwargs)
