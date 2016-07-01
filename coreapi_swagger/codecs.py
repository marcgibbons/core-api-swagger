import json

from six.moves.urllib.parse import urlparse

from coreapi.codecs import base
from coreapi.compat import force_bytes


class OpenAPICodec(base.BaseCodec):
    media_type = 'application/json'

    def dump(self, document, **kwargs):
        converter = DocumentToSwaggerConverter(document)
        return force_bytes(json.dumps(converter.convert()))


class DocumentToSwaggerConverter(object):
    def __init__(self, document):
        self.document = document

    def convert(self):
        return self._generate_swagger_object()

    def _generate_swagger_object(self):
        """
        Generates root of the Swagger spec.
        """
        parsed_url = urlparse(self.document.url)

        return {
            'swagger': '2.0',
            'info': self._get_info_object(),
            'paths': self._get_paths_object(),
            'host': parsed_url.netloc,
        }

    def _get_info_object(self):
        return {
            'title': self.document.title,
            'version': '1.0 '  # TODO: figure out how to set this req'd field
        }

    def _get_paths_object(self):
        paths = {}
        for tag, object_ in self.document.data.items():
            for link in object_.links.values():
                if link.url not in paths:
                    paths[link.url] = {}

                operation = link
                operation = {
                    'tags': [tag],
                    'description': link.description,
                    'responses': {'200': {'description': ''}},  # TODO: infer
                    'parameters': self._get_parameters(link.fields)
                }
                paths[link.url].update({link.action: operation})

        return paths

    def _get_parameters(self, fields):
        return [
            {
                'name': field.name,
                'required': field.required,
                'in': self._get_parameter_in(field.location),
                'description': field.description,
                'type': 'string'
            }
            for field in fields
        ]

    def _get_parameter_in(self, location):
        if location == 'form':
            return 'formData'

        return location
