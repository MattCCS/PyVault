#!/usr/local/bin/python

####################################
# standard
import csv
from StringIO       import StringIO
from collections    import namedtuple

####################################
# custom
import AES
import utils

def generic_csv_reader(csv_data, _b16_elems=True):
    tablereader = csv.reader(StringIO(csv_data), delimiter=',')

    headers = next(tablereader)
    if _b16_elems:
        headers = map(utils.unhexed, headers)
    headers = map(lambda s:s.lower(), headers)

    assert headers[0] == 'service'
    assert headers[1] == 'username'
    assert len(headers) > 2

    Entry = namedtuple("Entry", headers) # DEFINE CLASS!

    rows = []

    for row in tablereader:
        if _b16_elems:
            row = map(utils.unhexed, row)
        row = Entry._make(row)
        rows.append(row)

    return (Entry, rows)


class CSVHandler:

    def __init__(self, config=None):
        self.config = utils.gen_config() if config is None else config

        self.aes = AES.AESHandler(self.config)

    def read(self, config=None):
        ####################################
        # config preparation
        config = self.config if config is None else config

        ####################################
        # read data
        data = self.aes.read(config)

        return generic_csv_reader(data, config.get('b16_elems', False))

    def write(self, data, config=None):
        ####################################
        # config preparation
        config = self.config if config is None else config

        s = '\n'.join(
                ','.join( (map(utils.hexed, row) if config.get('b16_elems', False) else row) )
            for row in data)

        self.aes.write(s, config)


if __name__ == '__main__':
    csv_h = CSVHandler()
    (entry, rows) = csv_h.read()

    print entry

    for r in rows:
        print r