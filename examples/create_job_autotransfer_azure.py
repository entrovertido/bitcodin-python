#!/usr/bin/env python
from time import sleep

import bitcodin

bitcodin.api_key = 'YOUR API KEY'

input_obj = bitcodin.Input(url='http://bitbucketireland.s3.amazonaws.com/Sintel-original-short.mkv')
input_result = bitcodin.create_input(input_obj)

video_configs = list()

video_configs.append(bitcodin.VideoStreamConfig(
    default_stream_id=0,
    bitrate=1024000,
    profile='Main',
    preset='premium',
    height=768,
    width=1024
))
video_configs.append(bitcodin.VideoStreamConfig(
    default_stream_id=1,
    bitrate=512000,
    profile='Main',
    preset='premium',
    height=480,
    width=640
))

audio_configs = [bitcodin.AudioStreamConfig(default_stream_id=0, bitrate=192000)]

encoding_profile_obj = bitcodin.EncodingProfile('API Test Profile', video_configs, audio_configs)
encoding_profile_result = bitcodin.create_encoding_profile(encoding_profile_obj)

manifests = ['mpd', 'm3u8']

output_obj = bitcodin.AzureOutput(
    name='Azure Test Output Python',
    account_name='yourAzureAccountName',
    account_key='yourAzureAccountKey',
    container='yourAzureContainer',
    prefix='yourDesiredPrefixInsideTheContainer'
)

output_result = bitcodin.create_output(output_obj)

# Simply give a output_id to the job configuration to which the results should be copied when the job is finished.
job = bitcodin.Job(
    input_id=input_result.input_id,
    encoding_profile_id=encoding_profile_result.encoding_profile_id,
    manifest_types=manifests,
    output_id=output_result.output_id
)
job_result = bitcodin.create_job(job)

while job_result.status != 'Finished' and job_result.status != 'Error':
    job_result = bitcodin.get_job(job_result.job_id)
    print(job_result.to_json())
    sleep(5)

print(job_result.to_json())
print("Job Finished!")
