from .errors import ChronologicalError
from ticts.utils import timestamp_converter


class Report(object):

    def __init__(self,
                 t0,
                 te,
                 name=""):
        """

        :param t0:
        :param te:
        :param name:
        """

        self.t0 = timestamp_converter(t0)
        self.te = timestamp_converter(te)
        self.name = name

        if self.te < self.t0:
            raise ChronologicalError("te ({}) can't be before t0! ({})"
                                     .format(self.te, self.t0))

    def __repr__(self):
        return "Report(t0={}, te={}, name={})".format(
            *map(repr, [self.t0, self.te, self.name])
        )

    @property
    def duration(self) -> float:
        if self.te is not None:
            return self.te - self.t0
        else:
            return 0

    def overlap(self, other) -> bool:
        return (self.t0 <= other.te) | (other.t0 <= self.te)
