#!/usr/local/bin/python

####################################
# standard
import collections

####################################
# custom
import CSV
import utils


class DBManager:

    reserved = ["service", "username"]

    def __init__(self, config=None):
        self.config = utils.gen_config() if config is None else config

        self.csv     = CSV.CSVHandler(self.config)
        self.Entry   = None
        self.entries = []

    ####################################
    # reading

    def read(self, config=None):
        config = self.config if config is None else config
        return self.csv.read(config)

    def do_read(self, config=None):
        """Mutates the object!"""

        ####################################
        # config preparation
        config = self.config if config is None else config

        (Entry, rows) = self.csv.read(config)

        self.Entry      = Entry
        self.entries    = rows

    ####################################
    # writing

    def to_lists(self):
        data = []

        header = list(self.Entry._fields)
        data.append(header)

        for e in self.entries:
            data.append(list(e))

        return data

    def write(self, config=None):
        """Mutates other objects!"""

        ####################################
        # config preparation
        config = self.config if config is None else config

        data = self.to_lists()

        self.csv.write(data, config)

    ####################################
    # searching

    def search(self, params, only_exact=False):
        results = []

        comp = lambda a,b: a.lower() in b.lower()
        if only_exact:
            comp = lambda a,b: a.lower() == b.lower()

        for (i,e) in enumerate(self.entries):
            for (k,v) in params.iteritems():
                if k not in e._fields:
                    # print "k not in e"
                    break
                elif not comp(v, getattr(e, k)):
                    # print "v not in e[k]"
                    break
            else:
                # print "{} matched all!".format(e)
                results.append( (i,e) )
                continue

            # print "{} wasn't a match.".format(e)
            pass

        # print results

        return results

    def find(self, service='', username=''):
        params = {"service":service, "username":username}
        results = self.search(params)

        if len(results) != 1:
            return results

        r = results[0][1]
        return (r.service, r.username, r.old_pw)


    ####################################
    # modifying

    def gen_empty_params(self):
        return {k:'' for k in self.Entry._fields}

    def fill_params(self, params, old_params=None):
        for k in params:
            if k not in self.Entry._fields:
                raise RuntimeError("provided a field {) but not in self.Entry!".format(k))

        if old_params is None:
            old_params = self.gen_empty_params()

        return dict(old_params.items() + params.items())

    def modify(self, idx, params):
        """Mutates the object!"""
        old_params = self.entries[idx]._asdict()
        new_params = self.fill_params(params, old_params)

    def replace(self, idx, params):
        """Mutates the object!"""
        new_params = self.fill_params(params)
        self.entries[idx] = self.Entry(**new_params)

    def add(self, params):
        """Mutates the object!  Denies duplicates!"""
        new_params = self.fill_params(params)

        search_params = {k:new_params[k] for k in DBManager.reserved}
        assert not self.search(search_params, only_exact=True)

        new_entry = self.Entry(**new_params)
        self.entries.append(new_entry)
        return new_entry

    ####################################
    # debug

    # def stringify(self):
    #     headers = self.Entry._fields
    #     rows = [list(e) for e in self.entries]

    #     L = [headers] + rows

    #     return '\n'.join(','.join(r) for r in L)


if __name__ == '__main__':

    dbm = DBManager()

    dbm.do_read()
    # results = dbm.search({"service":"sk", "username":"99"})
    # print results
    # i,e = results[0]
    # print i
    # print e

    dbm.add({"service":"vime", "username":"fredflintstone", "salt":"whoops"})
    for e in dbm.to_lists():
        print e

    # dbm.write()

    ####################################
    # testing replacement
    # dbm.replace(i, {"service":"foo", "salt":"bar"})
    # print dbm.search({"service":"sk", "username":"99"})
    # print dbm.search({"service":"foo"})
