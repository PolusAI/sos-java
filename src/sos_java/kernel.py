#!/usr/bin/env python
#
# Copyright (c) Konstantin Taletskiy
# Distributed under the terms of the MIT License.

import os
import numpy as np
import pandas as pd
from tempfile import TemporaryDirectory
from textwrap import dedent
from sos.utils import short_repr, env
from collections import Sequence
from IPython.core.error import UsageError
import re
import sys

def stitch_cell_output(response):
    return ''.join([stream[1]['text'] for stream in response ])

class sos_java:
    background_color = {'Java': '#00758F'}
    supported_kernels = {'Java': ['java']}
    options = {}
    cd_command = ''

    def __init__(self, sos_kernel, kernel_name='Java'):
        self.sos_kernel = sos_kernel
        self.kernel_name = kernel_name
        self.init_statements = cpp_init_statements

    def insistent_get_response(self, command, stream):
        response = self.sos_kernel.get_response(command, stream)
        while response==[]:
            response = self.sos_kernel.get_response(command, stream)

        return response

    def get_vars(self, names):
        for name in names:
            self.sos_kernel.warn(name)

    def put_vars(self, names, to_kernel=None):
        result = {}
        for name in names:
            # name - string with variable name (in Java)
            cpp_type = self.insistent_get_response(f'{name}', ('execute_result',))[0][1]['data']['text/plain']
        return result
