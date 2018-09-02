#! /usr/bin/env python
# SPDX-License-Identifier: Unlicense

import automowy

session = automowy.AutomowySession()
mower = session.login('john@doe.com', 'secret').find_mower()

print(mower.query('status'))

mower.control('start/override/period', {'period': 300})
mower.control('start')
mower.control('pause')
mower.control('park')
mower.control('park/duration/timer')
mower.set('cuttingHeight', 4)

session.logout()
