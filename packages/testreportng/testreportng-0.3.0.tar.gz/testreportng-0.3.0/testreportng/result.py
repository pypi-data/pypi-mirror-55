import typing
import json
import datetime

from testreportng.detail import NGCaseDetail
from testreportng.constants import Label


class NGResult(object):
    """ result of suite """

    def __init__(self, kls_name: str):
        self.kls_name: str = kls_name
        self.data: typing.Dict[str, NGCaseDetail] = dict()

    def set(self, cur: NGCaseDetail):
        self.data[cur.name] = cur

    def get(self, name: str) -> typing.Optional[NGCaseDetail]:
        if name not in self.data:
            return None
        return self.data[name]

    def get_data_by_label(self, label_name: str):
        summary = self.summary()
        assert label_name in summary, f"label {label_name} not in summary"
        return summary[label_name]

    @property
    def start_time(self) -> datetime.datetime:
        return min([each.start_time for each in self.data.values()])

    @property
    def end_time(self) -> datetime.datetime:
        return max([each.end_time for each in self.data.values()])

    @property
    def duration(self) -> float:
        return (self.end_time - self.start_time).total_seconds()

    def summary(self) -> dict:
        result: typing.Dict[str, int] = {
            Label.LABEL_NAME: self.kls_name,
            Label.LABEL_TOTAL: len(self.data),
            Label.LABEL_START_TIME: self.start_time,
            Label.LABEL_END_TIME: self.end_time,
            Label.LABEL_DURATION: self.duration,
            # cases
            Label.LABEL_STATUS_PASS: 0,
            Label.LABEL_STATUS_FAIL: 0,
            Label.LABEL_STATUS_ERROR: 0,
            Label.LABEL_STATUS_SKIP: 0,
        }

        for each in self.data.values():
            result[each.status] += 1
        return result

    def to_dict(self, safe_repr: bool = None) -> typing.Dict[str, dict]:
        """
        dump Result to dict, for easier usage by others

        :param safe_repr:
            bool.
            dump all the objects to string if True.
            default to False.
        :return:
        """
        r = dict()
        for name, result in self.data.items():
            r[name] = result.to_dict(safe_repr=safe_repr)
        return r

    def to_json(self) -> str:
        """
        dump Detail to json string

        :return:
        """
        r = self.to_dict(True)
        return json.dumps(r)

    def __str__(self):
        return f"<{__class__.__name__} result={self.data}>"

    __repr__ = __str__


class NGResultOperator(object):
    """ high level operator over multi Result objects """

    def __init__(self):
        self.data: typing.Set[NGResult] = set()

    def load(self, suite_dict: typing.Dict[str, NGResult]):
        for each in suite_dict.values():
            self.data.add(each)

    def add(self, new: NGResult):
        self.data.add(new)

    def remove(self, old: NGResult):
        self.data.remove(old)

    def reset(self):
        self.data = set()

    def get_start_time(self) -> datetime.datetime:
        return min([each.start_time for each in self.data])

    def get_end_time(self) -> datetime.datetime:
        return max([each.end_time for each in self.data])

    def get_duration(self) -> float:
        return (self.get_end_time() - self.get_start_time()).total_seconds()

    def summary(self) -> typing.Dict:
        result = {}
        for each_label in (
            Label.LABEL_TOTAL,
            Label.LABEL_STATUS_PASS,
            Label.LABEL_STATUS_FAIL,
            Label.LABEL_STATUS_ERROR,
            Label.LABEL_STATUS_SKIP,
        ):
            result[each_label] = self.get_case_count(each_label)
        result[Label.LABEL_START_TIME] = self.get_start_time()
        result[Label.LABEL_END_TIME] = self.get_end_time()
        result[Label.LABEL_DURATION] = self.get_duration()
        return result

    def get_case_count(self, case_type: str) -> int:
        type_list = (
            Label.LABEL_TOTAL,
            Label.LABEL_STATUS_PASS,
            Label.LABEL_STATUS_FAIL,
            Label.LABEL_STATUS_ERROR,
            Label.LABEL_STATUS_SKIP,
        )
        assert (
            case_type in type_list
        ), f"status {case_type} should be one of {type_list}"
        return sum([each.get_data_by_label(case_type) for each in self.data])
