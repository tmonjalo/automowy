#! /usr/bin/env python
# SPDX-License-Identifier: Unlicense

import automowy

session = automowy.AutomowySession()
session.login('john@doe.com', 'secret')

session.logout()
