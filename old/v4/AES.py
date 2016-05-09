#!/usr/local/bin/python

####################################
# standard

####################################
# custom
import settings


class AESHandler:

    def __init__(self, config=None):
        self.config = utils.gen_config() if config is None else config

    def read(self, config=None):
        ####################################
        # config preparation
        config = self.config if config is None else config

        # aes = config['aes']

        path = config.get('path', settings.path)

        with open(path, 'r') as f:
            data = f.read()

        return data

    def write(self, data, config=None):
        ####################################
        # config preparation
        config = self.config if config is None else config

        # aes = config['aes']

        path = config.get('path', settings.path)

        with open(path, 'w') as f:
            f.write(data)
