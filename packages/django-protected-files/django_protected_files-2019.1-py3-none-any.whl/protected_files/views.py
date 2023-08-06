import os

from django.views import View
from django.conf import settings
from django.http import HttpResponse
from django.views.static import serve
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@method_decorator(login_required, name='dispatch')
class NginxProtectedView(View):
    @property
    def _internal_prefix(self):
        raise NotImplementedError

    def get(self, request, path):
        if self._internal_prefix is None:
            raise Exception

        response = HttpResponse()
        response['X-Accel-Redirect'] = os.path.join(self._internal_prefix, path)

        return response


class NginxProtectedMediaView(NginxProtectedView):
    default_internal_prefix = '/protected_media_internal/'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nginx_prefix = getattr(settings,
                                    'PROTECTED_MEDIA_NGINX_INTERNAL_PREFIX',
                                    self.default_internal_prefix)

    @property
    def _internal_prefix(self):
        return self.nginx_prefix


class NginxProtectedStaticView(NginxProtectedView):
    default_internal_prefix = '/protected_static_internal/'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nginx_prefix = getattr(settings,
                                    'PROTECTED_STATIC_NGINX_INTERNAL_PREFIX',
                                    self.default_internal_prefix)

    @property
    def _internal_prefix(self):
        return self.nginx_prefix


@method_decorator(login_required, name='dispatch')
class DebugProtectedView(View):
    @property
    def _root(self):
        raise NotImplementedError

    def get(self, request, path):
        return serve(request, path, document_root=self._root)


class DebugProtectedMediaView(DebugProtectedView):
    @property
    def _root(self):
        return settings.PROTECTED_MEDIA_ROOT


class DebugProtectedStaticView(DebugProtectedView):
    @property
    def _root(self):
        return settings.PROTECTED_STATIC_ROOT
