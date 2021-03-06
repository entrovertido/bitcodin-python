__author__ = 'Dominic Miglar <dominic.miglar@bitmovin.net>'

import unittest
from bitcodin import create_output
from bitcodin import delete_output
from bitcodin import S3Output
from bitcodin.test.settings import s3_output_config
from bitcodin.test.bitcodin_test_case import BitcodinTestCase


class CreateS3OutputTestCase(BitcodinTestCase):

    output = None

    def setUp(self):
        super(CreateS3OutputTestCase, self).setUp()
        self.s3_configuration = {
            'name': 'Python API Test Output',
            'host': s3_output_config.get('host', None),
            'access_key': s3_output_config.get('access_key', None),
            'secret_key': s3_output_config.get('secret_key', None),
            'bucket': s3_output_config.get('bucket', None),
            'prefix': s3_output_config.get('prefix', None),
            'region': s3_output_config.get('region', None),
            'make_public': False
        }
        self.output = S3Output(
            name=self.s3_configuration.get('name'),
            host=self.s3_configuration.get('host'),
            access_key=self.s3_configuration.get('access_key'),
            secret_key=self.s3_configuration.get('secret_key'),
            bucket=self.s3_configuration.get('bucket'),
            prefix=self.s3_configuration.get('prefix'),
            region=self.s3_configuration.get('region'),
            make_public=self.s3_configuration.get('make_public')
        )

    def runTest(self):
        output = S3Output(
            name=self.s3_configuration.get('name'),
            host=self.s3_configuration.get('host'),
            access_key=self.s3_configuration.get('access_key'),
            secret_key=self.s3_configuration.get('secret_key'),
            bucket=self.s3_configuration.get('bucket'),
            prefix=self.s3_configuration.get('prefix'),
            region=self.s3_configuration.get('region'),
            make_public=self.s3_configuration.get('make_public')
        )
        self.output = create_output(output)
        self.assertEquals(self.output.name, self.s3_configuration['name'])
        self.assertEquals(self.output.bucket, self.s3_configuration.get('bucket'))
        self.assertEquals(self.output.prefix, self.s3_configuration.get('prefix'))
        self.assertEquals(self.output.region, self.s3_configuration.get('region'))
        self.assertEquals(self.output.make_public, self.s3_configuration.get('make_public'))

    def tearDown(self):
        delete_output(self.output.output_id)
        super(CreateS3OutputTestCase, self).tearDown()


if __name__ == '__main__':
    unittest.main()
