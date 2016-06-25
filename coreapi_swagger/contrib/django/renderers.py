from rest_framework.renderers import BaseRenderer

from ...codecs import OpenAPICodec


class SwaggerRenderer(BaseRenderer):
    media_type = 'application/vnd.swagger+json'
    charset = None
    format = 'swagger'

    def render(self, data, *args, **kwargs):
        codec = OpenAPICodec()
        return codec.dump(data)
