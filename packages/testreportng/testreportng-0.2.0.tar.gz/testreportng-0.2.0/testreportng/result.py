import typing
import json

from testreportng.detail import NGCaseDetail


class NGResult(object):
    LABEL_NAME: str = "name"
    LABEL_TOTAL: str = "total"
    LABEL_CASE_NAME: str = NGCaseDetail.LABEL_CASE_NAME
    LABEL_STATUS: str = NGCaseDetail.LABEL_STATUS
    LABEL_REASON: str = NGCaseDetail.LABEL_REASON
    LABEL_ERROR: str = NGCaseDetail.LABEL_ERROR
    LABEL_TRACEBACK: str = NGCaseDetail.LABEL_TRACEBACK
    LABEL_START_TIME: str = NGCaseDetail.LABEL_START_TIME
    LABEL_END_TIME: str = NGCaseDetail.LABEL_END_TIME
    LABEL_DURATION: str = NGCaseDetail.LABEL_DURATION

    def __init__(self, kls_name: str):
        self.kls_name: str = kls_name
        self.data: typing.Dict[str, NGCaseDetail] = dict()

    def set(self, cur: NGCaseDetail):
        self.data[cur.name] = cur

    def get(self, name: str) -> typing.Optional[NGCaseDetail]:
        if name not in self.data:
            return None
        return self.data[name]

    @property
    def start_time(self) -> str:
        return min([each.start_time for each in self.data.values()])

    @property
    def end_time(self) -> str:
        return max([each.end_time for each in self.data.values()])

    @property
    def duration(self) -> str:
        return str(int(self.end_time) - int(self.start_time))

    def summary(self) -> dict:
        result: typing.Dict[str, int] = {
            self.LABEL_NAME: self.kls_name,
            self.LABEL_TOTAL: len(self.data),
            self.LABEL_START_TIME: self.start_time,
            self.LABEL_END_TIME: self.end_time,
            self.LABEL_DURATION: self.duration,
            # cases
            NGCaseDetail.LABEL_STATUS_PASS: 0,
            NGCaseDetail.LABEL_STATUS_FAIL: 0,
            NGCaseDetail.LABEL_STATUS_ERROR: 0,
            NGCaseDetail.LABEL_STATUS_SKIP: 0,
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
