import typing
import enum

from .condition import Condition


class FeatureGlobalStatus(enum.Enum):
    """ Describes the global status of a feature. If the global status is 
    FeatureGlobalStatus.OFF, the evaluation can be short circuited. A status of
    OFF implies that the kill-switch is engaged. """
    ON = 'on'
    OFF = 'off'


class FeatureDefinition(object):
    """ Encapsulates the definition of a feature on the server. Provides methods
    to aid evaluation. The segment values are merely segment_ids. """

    def __init__(
        self, 
        _id, 
        global_status,
        enabled_for_segments=[],
        suppressed_for_segments=[]
    ):
        self.id = _id
        self.global_status = global_status
        self.enabled_for_segments = enabled_for_segments
        self.suppressed_for_segments = suppressed_for_segments

    @classmethod
    def from_encoding(
            cls,
            gs:str=None,
            _id:str=None,
            es:typing.List[typing.Dict]=[],
            ss:typing.List[typing.Dict]=[]
        ):
        global_status = gs == 'ON' and FeatureGlobalStatus.ON or FeatureGlobalStatus.OFF
        return cls(
            _id, global_status,
            enabled_for_segments=list(map(Condition.from_encoding, es)),
            suppressed_for_segments=list(map(Condition.from_encoding, ss))
        )