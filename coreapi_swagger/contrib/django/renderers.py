from django.template import loader
from rest_framework.renderers import BaseRenderer

from ...codecs import OpenAPICodec


class OpenAPIRenderer(BaseRenderer):
    media_type = 'application/openapi+json'
    charset = None
    format = 'openapi'

    def render(self, data, *args, **kwargs):
        codec = OpenAPICodec()
        return codec.dump(data)


class SwaggerUIRenderer(BaseRenderer):
    media_type = 'text/html'
    format = 'swagger'
    template = 'coreapi_swagger/index.html'
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        template = loader.get_template(self.template)
        return template.render()
