from jinja2 import Template
import typing

from testreportng.result import NGResult, NGResultOperator
from testreportng.constants import Label

COLOR_DICT = {
    Label.LABEL_STATUS_PASS: "#dff0d8",
    Label.LABEL_STATUS_FAIL: "#fcf8e3",
    Label.LABEL_STATUS_ERROR: "#f2dede",
    Label.LABEL_STATUS_SKIP: "#ffffff",
    Label.LABEL_STATUS_INIT: "#ffffff",
}

TEMPLATE = r"""
<!DOCTYPE html>
<html>
<head>
<title>{{ test_name }}</title>

<style>
table, th, td {
  border: 1px solid black;
  border-collapse: collapse;
}
th, td {
  padding: 5px;
}
th {
  text-align: left;
}
</style>
</head>

<body>
<h1>{{ test_name }}</h1>

<h2>Summary</h2>
<table style="width:90%">
  <tr>
    {% for title, count in summary.items() %}
      <th>{{ title }}</th>
    {% endfor %}
  </tr>

  <tr">
    {% for title, count in summary.items() %}
      <td>{{ count }}</td>
    {% endfor %}
  </tr>
  
</table>

<h2>Result</h2>
<table style="width:90%">
  <tr>
    <th>suite</th>
    <th>case</th>
    <th>status</th>
    <th>traceback</th>
  </tr>

  {% for suite_name, each in test_result.items() %}
    {% for each_case_name, each_case in each.to_dict(safe_repr=True).items() %}
        <tr style="background-color: {{ color_dict[each_case.status] }}">
          <td>{{ suite_name }}</td>
          <td>{{ each_case_name }}</td>
          <td>{{ each_case.status }}</td>
          <td>{{ each_case.traceback }}</td>
        </tr>
    {% endfor %}
  {% endfor %}
</table>

</body>
</html>
"""


class HtmlReporter(object):
    _template = TEMPLATE
    _default_test_name = "default"

    @classmethod
    def render(
        cls, test_name: str, result: typing.Union[typing.Dict[str, NGResult], NGResult]
    ) -> str:
        html_template = Template(TEMPLATE)
        # re-format
        if isinstance(result, NGResult):
            result = {cls._default_test_name: result}

        result_operator = NGResultOperator()
        result_operator.load(result)
        summary = result_operator.summary()

        return html_template.render(
            test_name=test_name,
            summary=summary,
            test_result=result,
            color_dict=COLOR_DICT,
        )
