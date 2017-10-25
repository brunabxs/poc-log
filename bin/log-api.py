#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

# **********************************************
# Add application directory to python path
# **********************************************

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# **********************************************
# Load app
# **********************************************
from log.app import create_app  # NOQA

application = create_app()
app_context = application.app_context()
app_context.push()


if __name__ == "__main__":
    application.run(debug=True, host='0.0.0.0', port=9000)
