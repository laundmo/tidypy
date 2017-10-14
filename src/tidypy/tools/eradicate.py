from __future__ import absolute_import

from eradicate import commented_out_code_line_numbers

from .base import PythonTool, Issue, AccessIssue


class EradicateIssue(Issue):
    tool = 'eradicate'
    pylint_type = 'R'


class EradicateTool(PythonTool):
    @classmethod
    def get_all_codes(cls):
        return [
            ('commented', 'Commented-out code'),
        ]

    def execute(self, finder):
        issues = []

        for filepath in finder.files(self.config['filters']):
            try:
                source = finder.read_file(filepath).decode('utf-8')
            except EnvironmentError as exc:
                issues.append(AccessIssue(exc, filepath))
                continue

            for line in commented_out_code_line_numbers(source):
                issues.append(EradicateIssue(
                    'commented',
                    'Commented-out code',
                    filepath,
                    line,
                ))

        return issues

