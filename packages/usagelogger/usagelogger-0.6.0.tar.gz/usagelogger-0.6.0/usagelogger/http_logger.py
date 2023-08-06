# coding: utf-8
# © 2016-2019 Resurface Labs Inc.

import json
import random
import re
from time import time
from typing import List, Optional, Pattern

from usagelogger.base_logger import BaseLogger
from usagelogger.http_message import HttpMessage
from usagelogger.http_rule import HttpRule
from usagelogger.http_rules import HttpRules


class HttpLogger(BaseLogger):
    """Usage logger for HTTP/HTTPS protocol."""

    # Agent string identifying this logger.
    AGENT: str = 'http_logger.py'

    # Always privacy by default
    __default_rules: str = HttpRules.strict_rules()

    @classmethod
    def default_rules(cls) -> str:
        return cls.__default_rules

    @classmethod
    def set_default_rules(cls, rules: str) -> None:
        cls.__default_rules: str = re.sub(r'^\s*include default\s*$', '', rules, flags=re.MULTILINE)

    __STRING_TYPES: str = (
        r'^(text/(html|plain|xml))|'
        r'(application/(json|soap|xml|x-www-form-urlencoded))')

    __STRING_TYPES_REGEX: Pattern = re.compile(__STRING_TYPES, flags=re.IGNORECASE)

    @classmethod
    def is_string_content_type(cls, s: str) -> bool:
        return s is not None and cls.__STRING_TYPES_REGEX.match(s) is not None

    def __init__(self, enabled: Optional[bool] = True,
                 queue: Optional[List[str]] = None,
                 url: Optional[str] = None,
                 skip_compression: Optional[bool] = False,
                 skip_submission: Optional[bool] = False,
                 rules: Optional[str] = None) -> None:

        super().__init__(self.AGENT, enabled=enabled, queue=queue, url=url,
                         skip_compression=skip_compression, skip_submission=skip_submission)

        # read rules from param or defaults
        if rules is not None:
            self.rules: str = re.sub(r'^\s*include default\s*$', str(self.default_rules()), rules, flags=re.MULTILINE)
            if len(self.rules.strip()) == 0: self.rules: str = self.default_rules()
        else:
            self.rules: str = self.default_rules()
        # todo rules should be immutable (Clubhouse #37)

        # parse and break rules out by verb
        prs: List[HttpRule] = HttpRules.parse(self.rules)
        self.rules_allow_http_url: bool = len([r for r in prs if 'allow_http_url' == r.verb]) > 0
        self.rules_copy_session_field: List[HttpRule] = [r for r in prs if 'copy_session_field' == r.verb]
        self.rules_remove: List[HttpRule] = [r for r in prs if 'remove' == r.verb]
        self.rules_remove_if: List[HttpRule] = [r for r in prs if 'remove_if' == r.verb]
        self.rules_remove_if_found: List[HttpRule] = [r for r in prs if 'remove_if_found' == r.verb]
        self.rules_remove_unless: List[HttpRule] = [r for r in prs if 'remove_unless' == r.verb]
        self.rules_remove_unless_found: List[HttpRule] = [r for r in prs if 'remove_unless_found' == r.verb]
        self.rules_replace: List[HttpRule] = [r for r in prs if 'replace' == r.verb]
        self.rules_sample: List[HttpRule] = [r for r in prs if 'sample' == r.verb]
        self.rules_stop: List[HttpRule] = [r for r in prs if 'stop' == r.verb]
        self.rules_stop_if: List[HttpRule] = [r for r in prs if 'stop_if' == r.verb]
        self.rules_stop_if_found: List[HttpRule] = [r for r in prs if 'stop_if_found' == r.verb]
        self.rules_stop_unless: List[HttpRule] = [r for r in prs if 'stop_unless' == r.verb]
        self.rules_stop_unless_found: List[HttpRule] = [r for r in prs if 'stop_unless_found' == r.verb]
        self.skip_compression: bool = len([r for r in prs if r.verb == 'skip_compression']) > 0
        self.skip_submission: bool = len([r for r in prs if r.verb == 'skip_submission']) > 0
        # todo parsed rules should be immutable (Clubhouse #37)

        # finish validating rules
        if len(self.rules_sample) > 1: raise SyntaxError('Multiple sample rules')
        if self._enabled and url is not None and url.startswith('http:') and not self.rules_allow_http_url:
            self._enableable = False
            self._enabled = False

    def log(self, request, response, response_body: Optional[str] = None, request_body: Optional[str] = None) -> bool:
        """Logs HTTP request and response to intended destination."""

        if self.enabled: return self.submit(self.format(request, response, response_body, request_body))
        return True

    def format(self, request, response, response_body: Optional[str] = None, request_body: Optional[str] = None,
               now: Optional[int] = None) -> str:
        """Formats HTTP request and response as JSON message."""

        details: List[List[str]] = HttpMessage.build(request, response, response_body, request_body)

        # todo copy data from session if configured (Clubhouse #151)

        # quit early based on stop rules if configured
        for r in self.rules_stop:
            for d in details:
                if r.scope.match(d[0]): return None
        for r in self.rules_stop_if_found:
            for d in details:
                if r.scope.match(d[0]) and r.param1.search(d[1]): return None
        for r in self.rules_stop_if:
            for d in details:
                if r.scope.match(d[0]) and r.param1.match(d[1]): return None
        passed = 0
        for r in self.rules_stop_unless_found:
            for d in details:
                if r.scope.match(d[0]) and r.param1.search(d[1]): passed += 1
        if passed != len(self.rules_stop_unless_found): return None
        passed = 0
        for r in self.rules_stop_unless:
            for d in details:
                if r.scope.match(d[0]) and r.param1.match(d[1]): passed += 1
        if passed != len(self.rules_stop_unless): return None

        # do sampling if configured
        if len(self.rules_sample) == 1 and random.randrange(100) >= int(self.rules_sample[0].param1): return None

        # winnow sensitive details based on remove rules if configured
        for r in self.rules_remove:
            for d in details:
                if r.scope.match(d[0]): d[1] = ''
        for r in self.rules_remove_unless_found:
            for d in details:
                if r.scope.match(d[0]) and not r.param1.search(d[1]): d[1] = ''
        for r in self.rules_remove_if_found:
            for d in details:
                if r.scope.match(d[0]) and r.param1.search(d[1]): d[1] = ''
        for r in self.rules_remove_unless:
            for d in details:
                if r.scope.match(d[0]) and not r.param1.match(d[1]): d[1] = ''
        for r in self.rules_remove_if:
            for d in details:
                if r.scope.match(d[0]) and r.param1.match(d[1]): d[1] = ''

        # remove any details with empty values
        details = [x for x in details if x[1] != '']
        if len(details) == 0: return None

        # mask sensitive details based on replace rules if configured
        for r in self.rules_replace:
            for d in details:
                if r.scope.match(d[0]): d[1] = re.sub(r.param1, r.param2, d[1])

        # remove any details with empty values
        details = [x for x in details if x[1] != '']
        if len(details) == 0: return None

        # finish message
        details.append(['now', str(now) if now is not None else str(round(time() * 1000))])
        details.append(['agent', self.AGENT])
        details.append(['host', self.host])
        details.append(['version', self.version])
        return json.dumps(details, separators=(',', ':'))
