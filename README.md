# CoreAPI Swagger
[![Build Status](https://travis-ci.org/marcgibbons/core-api-swagger.svg?branch=master)](https://travis-ci.org/marcgibbons/core-api-swagger)
[![codecov](https://codecov.io/gh/marcgibbons/core-api-swagger/branch/master/graph/badge.svg)](https://codecov.io/gh/marcgibbons/core-api-swagger)

## Use with CoreAPI

```python
import coreapi
from coreapi_swagger.codecs import OpenAPICodec

schema_document = coreapi.Document(title='My Schema', url='http://coreapi.org') 
coreapi.dump(schema_document, encoders=[OpenAPICodec()])
```

## Django REST Framework

This package ships with two renderer classes:

1. `OpenAPIRenderer` generates the OpenAPI (fka Swagger) JSON schema specification. This renderer will be presented if:
  -  `Content-Type: application/openapi+json` is specified in the headers.
  - `?format=openapi` is passed as query param
2. `SwaggerUIRenderer` generates the Swagger UI and requires the `OpenAPIRenderer`


### Example: DRF Schema View
```python
from coreapi_swagger.contrib.django.renderers import OpenAPIRenderer, SwaggerUIRenderer
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import response, schemas

@api_view()
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='Pastebin API')
    return response.Response(generator.get_schema(request=request))
```
