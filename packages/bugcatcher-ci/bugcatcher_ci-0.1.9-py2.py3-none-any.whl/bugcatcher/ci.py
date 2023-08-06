"""
@title Faster Than Light - Continuous Integration through BugCatcher API
"""

import subprocess
import json


class CI:
    # Parameterized Constructor
    def __init__(self, sid, project):
        self.sid = sid
        self.project = project


    # Parameter Methods
    def get_sid(self):
        return self.sid


    def set_sid(self, sid):
        if sid:
            self.sid = sid
        print("New SID: %s" % self.sid)
        return self.sid


    def get_project(self):
        return self.project


    def set_project(self, project):
        if project:
            self.project = project
        print("New Project Name: %s" % self.project)
        return self.project


    # Main Methods
    def push(self, project, items):
        project = project or self.project

        print("Uploading \"%s\" code to BugCatcher..." % project)

        push = subprocess.check_output([
            *self.build_ftl_cmd(project),
            "push",
            items
        ])
        assert push

        print_bytes(push)
        return push


    def test(self, project, severity_level):
        project = project or self.project
        severity_level = severity_level or self.severity_level

        print("Running tests on \"%s\" using BugCatcher..." % project)

        test = subprocess.check_output([
            *self.build_ftl_cmd(project),
            "--json",
            "test"
        ])
        assert test

        print("BugCatcher results for \"%s\":" % project)

        hits = json.loads(test.decode("utf8"))

        failed = False
        for hit in hits:
            start_line = hit['start_line']
            end_line = hit['end_line']
            test_suite_test = hit['test_suite_test']
            ftl_severity = test_suite_test['ftl_severity']
            ftl_short_description = test_suite_test['ftl_short_description']
            ftl_long_description = test_suite_test['ftl_long_description']
            code_name = hit['code']['name']
            print("\nSeverity: %s ===> %s (lines %s-%s)\n\t%s - %s" % (
                ftl_severity,
                code_name,
                start_line,
                end_line,
                ftl_short_description,
                ftl_long_description
            ))
            if not self.passes_severity(ftl_severity, severity_level):
                failed = True

        did_pass = not failed
        assert did_pass

        print("\nMinimum Severity Level to FAIL tests: \"%s\"" % severity_level)
        print("PASSING! - All results are less than \"%s\" level severity." % severity_level)
        return did_pass


    # Helper functions
    def build_ftl_cmd(self, project):
        return [
            "ftl",
            "--sid",
            self.sid,
            "--project",
            project or self.project
        ]


    def passes_severity(self, severity, min_severity):
        levels = ['low', 'medium', 'high']
        if severity not in levels:
            return True
        severity = levels.index(severity)
        min_severity = levels.index(min_severity)
        return min_severity > severity



# Helpers
def print_bytes(b):
    p = b.decode("utf-8")
    assert p

    for row in p.split('\n'):
        print(row)

