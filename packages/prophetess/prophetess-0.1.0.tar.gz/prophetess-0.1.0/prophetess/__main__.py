#!/usr/bin/env python

import asyncio
from prophetess import app

loop = asyncio.get_event_loop()
loop.run_until_complete(app.run())
