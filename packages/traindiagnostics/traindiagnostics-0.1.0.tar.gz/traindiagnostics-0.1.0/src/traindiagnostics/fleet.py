import pytz


class DiagnosticCodes(dict):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def codes(self):
        return self.keys()

    @classmethod
    def from_statechangearrays(cls, arrays):
        lst = [(a.name, a) for a in arrays]
        return cls(lst)

    def iter_states(self, t=None):
        for c, s in self.items():
            yield c, s.state(t)

    def state(self, t=None):
        return list(self.iter_states(t))


class Train(object):

    def __init__(self, name, codes=None):
        if not isinstance(name, str):
            raise TypeError("name needs to be of instance 'str'!")
        self.name = name
        if codes:
            if not isinstance(codes, dict):
                raise TypeError("name needs to be of instance 'dict'!")
        self.codes = codes or DiagnosticCodes()

    def __repr__(self):
        return "Train({}, codes={})".format(self.name, self.codes)

    def state(self, t=None):
        return {self.name: self.codes.state(t)}


def df2statechangearrays(dataframe, train="train", code="code", start="start", end="end", filter_codes=[]):

    dataframe = dataframe.sort_values(by=[train, code, start])

    current_train = None
    current_code = None

    fleet = dict()

    for idx, row in dataframe.iterrows():
        if current_train != row[train]:
            current_train = row[train]
            fleet[current_train] = dict()

        if current_code != row[code]:
            current_code = row[code]
            fleet[current_train][current_code] = []

        r = ds.Report(t0=row[start], te=row[end], name=row[code])
        fleet[current_train][current_code].append(r)

    f = dict()
    for train, codes in fleet.items():
        t = Train(train)
        dc = DiagnosticCodes()
        for code, r in codes.items():
            array = ds.StateChangeArray.from_reports(r)
            dc[code] = array
        t.codes = dc
        f[train] = t

    return f

def utc(dt):
    return pytz.utc.localize(dt)


if __name__ == "__main__":
    import pandas as pd
    import datetime as dt

    df = pd.DataFrame(
        [dict(train='001', code='a', start=utc(dt.datetime(2019, 1, 1, 8)), end=utc(dt.datetime(2019, 1, 1, 8, 30))),
         dict(train='002', code='a', start=utc(dt.datetime(2019, 1, 1, 8)), end=utc(dt.datetime(2019, 1, 1, 8, 30))),
         dict(train='003', code='a', start=utc(dt.datetime(2019, 1, 1, 8)), end=utc(dt.datetime(2019, 1, 1, 8, 30))),
         dict(train='001', code='b', start=utc(dt.datetime(2019, 1, 1, 8, 30)), end=utc(dt.datetime(2019, 1, 1, 8, 45))),
         dict(train='001', code='a', start=utc(dt.datetime(2019, 1, 1, 9, 30)), end=utc(dt.datetime(2019, 1, 1, 9, 45))),
         dict(train='001', code='c', start=utc(dt.datetime(2019, 1, 1, 8)), end=utc(dt.datetime(2019, 1, 1, 9, 45))),
         dict(train='002', code='b', start=utc(dt.datetime(2019, 1, 1, 8, 30)), end=utc(dt.datetime(2019, 1, 1, 8, 45))),
         dict(train='001', code='a', start=utc(dt.datetime(2019, 1, 1, 12)), end=utc(dt.datetime(2019, 1, 1, 14, 30)))
         ])

    fleet = df2statechangearrays(df)

    train_001 = fleet['001']
    train_001.state()
    print(train_001.state(utc(dt.datetime(2019,1,1,8,40))))
