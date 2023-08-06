import unittest

from testreportng.collector import NGCaseResult, NGCollector


class NGCase(unittest.TestCase):
    # default cls
    ng_result_cls = NGCaseResult
    ng_collector_cls = NGCollector

    # result collector
    ng_result: NGCollector

    @classmethod
    def setUpClass(cls) -> None:
        cls.ng_result: NGCollector = cls.ng_collector_cls()

    def setUp(self) -> None:
        cur = self.ng_result_cls(self._testMethodName)
        self.ng_result.set(cur)

    def tearDown(self) -> None:
        cur = self.ng_result.get(self._testMethodName)
        cur.outcome = getattr(self, "_outcome")

        self.ng_result.set(cur)
