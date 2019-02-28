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

def _sos_to_java_type(obj):
    ''' Returns corresponding C++ data type string for provided Python object '''
    if isinstance(obj, (int, np.intc, np.intp, np.int8, np.int16, np.int32, np.int64, bool, np.bool_)):
        if isinstance(obj, (bool, np.bool_)):
            return 'boolean', 'true' if obj==True else 'false'
        elif obj >= -2147483648 and obj <= 2147483647:
            return 'int', repr(obj)
        elif obj >= -9223372036854775808 and obj <= 9223372036854775807:
            return 'long', repr(obj)+'L'
        else:
            return -1, None #Integer is out of bounds
    elif isinstance(obj, (float, np.float16, np.float32, np.float64)):
        if (obj >= -3.40282e+38 and obj <= -1.17549e-38) or (obj >= 1.17549e-38 and obj <= 3.40282e+38):
            return 'float', repr(obj)+'f'
        elif (obj >= -1.79769e+308 and obj <= -2.22507e-308) or (obj >= 2.22507e-308 and obj <= 1.79769e+308):
            return 'double', repr(obj)
        else:
            return -1, None
    elif isinstance(obj, str):
        return 'String', '"'+obj+'"'
    
    else:
        return -1, None

class sos_java:
    background_color = {'Java': '#F80000'}
    supported_kernels = {'Java': ['java']}
    options = {}
    cd_command = ''

    def __init__(self, sos_kernel, kernel_name='Java'):
        self.sos_kernel = sos_kernel
        self.kernel_name = kernel_name
        self.init_statements = ''

    def insistent_get_response(self, command, stream):
        response = self.sos_kernel.get_response(command, stream)
        while response==[]:
            response = self.sos_kernel.get_response(command, stream)

        return response

    def _Java_declare_command_string(self, name, obj):
        #Check if object is scalar
        if isinstance(obj, (int, np.intc, np.intp, np.int8, np.int16, np.int32, np.int64, float, np.float16, np.float32, np.float64, np.longdouble, str, bool, np.bool_)):
            #do scalar declaration
            obj_type, obj_val = _sos_to_java_type(obj)
            if not obj_type == -1:
                return f'{obj_type} {name} = {obj_val};'
            else:
                return None
        elif isinstance(obj, (Sequence, np.ndarray, dict, pd.core.frame.DataFrame)):
            #do vector things
            return ''
        else:
            #unsupported type
            return None

    def get_vars(self, names):
        for name in names:
            # self.sos_kernel.warn(name)
            java_repr = self._Java_declare_command_string(name, env.sos_dict[name])
            if not java_repr==None:
                self.sos_kernel.run_cell(java_repr, True, False,
                 on_error=f'Failed to put variable {name} to Java')
            else:
                self.sos_kernel.warn(f'Cannot convert variable {name} to Java')

    def put_vars(self, names, to_kernel=None):
        result = {}
        for name in names:
            # name - string with variable name (in Java)
            cpp_type = self.insistent_get_response(f'{name}', ('execute_result',))[0][1]['data']['text/plain']
        return result
