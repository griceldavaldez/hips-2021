#!/usr/bin/env python

import sys
import site

site.addsitedir('/var/www/hips-2021/lib/python3.6/site-packages')

sys.path.insert(0, '/var/www/hips-2021')

from app.init import app as application
