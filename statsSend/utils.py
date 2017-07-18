#!/usr/bin/env python3

import traceback
import sys

def print_exception(message):
    print('{:s}\n{}'.format(message, traceback.format_exc()), file = sys.stderr)