# -*- coding: utf-8 -*-
"""Jenkins class file."""

from __future__ import absolute_import

import jenkins


class Jenkins(object):
    """Jenkins class."""

    def __init__(self, url, username, password):
        """Initialize an Jenkins class instance."""
        self.url = url
        self.username = username
        self.password = password

        # connect to jenkins
        self.jenkins = jenkins.Jenkins(url, username=username, password=password)
