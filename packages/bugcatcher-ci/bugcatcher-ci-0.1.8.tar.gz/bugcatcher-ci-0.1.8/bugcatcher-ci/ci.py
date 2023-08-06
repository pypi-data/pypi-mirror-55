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
        self.severity_level = 'medium'


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
        check_creds(self.sid, project)

        print("Uploading \"%s\" code to BugCatcher..." % project)

        push = None
        try:
            push = subprocess.check_output([
                *self.build_ftl_cmd(project),
                "push",
                items
            ])
        except:
            print("Error pushing code to BugCatcher. Please check your credentials.")

        print_bytes(push)
        
        return push


    def test(self, project, severity_level):
        project = project or self.project
        severity_level = severity_level or self.severity_level
        check_creds(self.sid, project)

        print("Running tests on \"%s\" using BugCatcher..." % project)

        test = None
        try:
            test = subprocess.check_output([
                *self.build_ftl_cmd(project),
                "--json",
                "test"
            ])
        except:
            print("Error testing code with BugCatcher. Please check your credentials.")

        if not test:
            return

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
def check_creds(sid, project):
    if not sid:
        print("BugCatcher SID not found. Please go to bugcatcher.fasterthanlight.dev to get a SID.")

    if not project:
        print("BugCatcher PROJECT not found. Please specify a project name.")


def print_bytes(b):
    if not b:
        return

    p = b.decode("utf-8")
    if not p:
        return

    for row in p.split('\n'):
        print(row)

