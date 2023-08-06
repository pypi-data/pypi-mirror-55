from ticts.utils import timestamp_converter


class Event(object):
    def __init__(self,
                 t,
                 value,
                 name=""):
        """
        :param value:
        :param t:
        :param name:
        """

        self.value = value

        self.t = timestamp_converter(t)
        self.name = name

    def __repr__(self):
        return "Event({}, t={}, name={})".format(
            *map(repr, [self.value, self.t, self.name])
        )
