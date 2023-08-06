import traceback


class NGCaseResult(object):
    STATUS_INIT: str = "init"
    STATUS_PASS: str = "pass"
    STATUS_FAIL: str = "fail"
    STATUS_ERROR: str = "error"
    STATUS_SKIP: str = "skip"

    def __init__(self, name: str, status: str = None):
        if not status:
            status = self.STATUS_INIT
        self.name: str = name
        self.status: str = status

        # data
        self._outcome = None

        # error
        self.error = None
        self.traceback = None

    def to_json_dict(self) -> dict:
        return {
            "name": self.name,
            "status": self.status,
            "error": repr(self.error) if self.error else "",
            "traceback": traceback.format_tb(self.traceback) if self.traceback else "",
        }

    @property
    def outcome(self):
        return self._outcome

    @outcome.setter
    def outcome(self, value):
        error = value.errors[1][1]

        # no error happened
        if not error:
            self.status = self.STATUS_PASS
            return

        # error or fail
        if error[0] is AssertionError:
            self.status = self.STATUS_FAIL
        else:
            self.status = self.STATUS_ERROR

        self.error = error[1]
        self.traceback = error[2]

    def __str__(self):
        return f"<{__class__.__name__} name={self.name} status={self.status}>"

    __repr__ = __str__
