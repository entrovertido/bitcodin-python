__author__ = 'Dominic Miglar <dominic.miglar@bitmovin.net>'

import unittest
from time import sleep, time
from bitcodin import create_job, get_job_status
from bitcodin import create_input
from bitcodin import create_encoding_profile
from bitcodin import delete_input
from bitcodin import delete_encoding_profile
from bitcodin import transfer_job
from bitcodin import Job
from bitcodin import Input
from bitcodin import AudioStreamConfig
from bitcodin import VideoStreamConfig
from bitcodin import EncodingProfile
from bitcodin.exceptions import BitcodinNotFoundError, BitcodinError
from bitcodin.test.config import test_video_url
from bitcodin.test.bitcodin_test_case import BitcodinTestCase


class TransferJobToNonExistentOutputTestCase(BitcodinTestCase):
    def setUp(self):
        super(TransferJobToNonExistentOutputTestCase, self).setUp()
        self.maxDiff = None

        input_url = test_video_url
        input = Input(input_url)
        self.input = create_input(input)
        audio_stream_config = AudioStreamConfig(default_stream_id=0, bitrate=192000)
        video_stream_config = VideoStreamConfig(default_stream_id=0, bitrate=512000,
                                                profile='Main', preset='premium', height=480, width=640)
        encoding_profile = EncodingProfile('API Test Profile', [video_stream_config], [audio_stream_config])
        self.encoding_profile = create_encoding_profile(encoding_profile)
        self.manifests = ['m3u8', 'mpd']
        job = Job(
            input_id=self.input.input_id,
            encoding_profile_id=self.encoding_profile.encoding_profile_id,
            manifest_types=self.manifests
        )
        self.job = create_job(job)

    def runTest(self):
        start_time = time()
        time_limit = 1200

        while True:
            job_status = get_job_status(self.job.job_id)
            if job_status.status.lower() == 'finished':
                break
            elif job_status.status.lower() == 'error':
                raise BitcodinError('An error occured while waiting for job to be FINISHED', 'Job status changed to ERROR!')
            elif time() - start_time > time_limit:
                raise BitcodinError('Timeout of job duration exceeded!', 'Job took too long!')
            sleep(2)

        with self.assertRaises(BitcodinNotFoundError):
            transfer = transfer_job(self.job.job_id, 0)

    def tearDown(self):
        delete_input(self.input.input_id)
        delete_encoding_profile(self.encoding_profile.encoding_profile_id)
        super(TransferJobToNonExistentOutputTestCase, self).tearDown()


if __name__ == '__main__':
    unittest.main()
