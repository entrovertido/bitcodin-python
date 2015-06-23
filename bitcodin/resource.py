__author__ = 'David Moser <david.moser@bitmovin.net>'

import json
from util import convert_dict


class BitcodinObject(dict):

    def __init__(self, dictionary):
        super(BitcodinObject, self).__init__()

        dictionary = convert_dict(dictionary)
        self.__dict__.update(dictionary)
        for k, v in dictionary.items():
            if isinstance(v, dict):
                self.__dict__[k] = BitcodinObject(v)
            if isinstance(v, list):
                index = 0
                for d in v:
                    v[index] = BitcodinObject(d)
                    index += 1
                del index

    def to_json(self):
        return json.dumps(self)

    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError('No such attribute: ' + name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError('No such attribute: ' + name)


class Input(BitcodinObject):

    def __init__(self, type="url", url=None):
        """
        :param type: string: Type of the Input
        :param url: string: Url to the source
        :return: Input
        """
        self.type = type

        if url is None:
            raise ValueError('url of Input can not be None')

        self.url = url

        super(Input, self).__init__(self.__dict__)


class Job(BitcodinObject):

    def __init__(self, input_id, encoding_profile_id, manifest_types):
        self.inputId = input_id
        self.encodingProfileId = encoding_profile_id
        self.manifestTypes = manifest_types

        super(Job, self).__init__(self.__dict__)


class EncodingProfile(BitcodinObject):

    def __init__(self, name='Encoding Profile', video_stream_configs=None, audio_stream_configs=None):

        self.name = name

        if video_stream_configs is None:
            raise ValueError('videoStreamConfigs can not be None')
        self.videoStreamConfigs = video_stream_configs

        if audio_stream_configs is None:
            raise ValueError('audioStreamConfigs can not be None')
        self.audioStreamConfigs = audio_stream_configs

        super(EncodingProfile, self).__init__(self.__dict__)


class VideoStreamConfig(BitcodinObject):

    def __init__(self, default_stream_id=0, bitrate=1024000, profile='Main', preset='preset', height=480, width=640):
        self.defaultStreamId = default_stream_id
        self.bitrate = bitrate
        self.profile = profile
        self.preset = preset
        self.height = height
        self.width = width

        super(VideoStreamConfig, self).__init__(self.__dict__)


class AudioStreamConfig(BitcodinObject):

    def __init__(self, default_stream_id=0, bitrate=1024000):
        self.defaultStreamId = default_stream_id
        self.bitrate = bitrate

        super(AudioStreamConfig, self).__init__(self.__dict__)
