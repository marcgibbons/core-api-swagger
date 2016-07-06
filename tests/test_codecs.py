import uuid
from unittest import TestCase

import coreapi
from coreapi_swagger import codecs

from .compat import mock


class TestGetInfoObject(TestCase):
    def setUp(self):
        self.document = coreapi.Document(title='Example API')
        converter = codecs.DocumentToSwaggerConverter(self.document)
        self.sut = converter._get_info_object()

    def test_title(self):
        self.assertDictContainsSubset({'title': self.document.title}, self.sut)

    def test_version(self):
        """
        Ensures that the version is provided since it is a required field.
        """
        self.assertDictContainsSubset({'version': ''}, self.sut)


class TestGetParameters(TestCase):
    def setUp(self):
        self.field = coreapi.Field(
            name='email',
            required='true',
            location='query',
            description='A valid email address.'
        )
        patcher = mock.patch.object(
            codecs.DocumentToSwaggerConverter,
            '_convert_location_to_in'
        )
        self.location_mock = patcher.start()
        self.addCleanup(patcher.stop)

        self.sut = codecs.DocumentToSwaggerConverter \
            ._get_parameters([self.field])[0]

    def test_expected_fields(self):
        self.assertDictContainsSubset(
            {
                'name': self.field.name,
                'required': self.field.required,
                'in': self.location_mock.return_value,
                'description': self.field.description,
                'type': 'string'  # Everything is a string for now.
            },
            self.sut
        )


class TestConvertLocationToIn(TestCase):
    def setUp(self):
        self.sut = codecs.DocumentToSwaggerConverter._convert_location_to_in

    def test_form_is_converted_to_formdata(self):
        self.assertEqual('formData', self.sut('form'))

    def test_random_string_is_returned_as_is(self):
        """
        Asserts that any input (other than form) is returned as-is,
        since the Swagger Parameter object `in` property maps 1:1 with
        the Field.location property,
        """
        expected = str(uuid.uuid4())
        self.assertEqual(expected, self.sut(expected))
