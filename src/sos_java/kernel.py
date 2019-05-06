#!/usr/bin/env python
#
# Copyright (c) Konstantin Taletskiy
# Distributed under the terms of the MIT License.

import os
import numpy as np
import pandas as pd
import csv
import tempfile
from textwrap import dedent
from sos.utils import short_repr, env
from collections import Sequence
from IPython.core.error import UsageError
import re
import sys

def homogeneous_type(seq):
    iseq = iter(seq)
    first_type = type(next(iseq))
    if first_type in (int, float):
        return True if all(isinstance(x, (int, float)) for x in iseq) else False
    else:
        return True if all(isinstance(x, first_type) for x in iseq) else False

java_init_statements = f'''
%jars {os.path.dirname(os.path.realpath(__file__))}/helper.jar\n
%maven tech.tablesaw:tablesaw-beakerx:0.30.3\n
%maven com.jimmoores:quandl-tablesaw:2.0.0\n
import static tech.tablesaw.aggregate.AggregateFunctions.*;\n
import tech.tablesaw.api.*;\n
import tech.tablesaw.columns.*;\n
import sos.helper
'''

def stitch_cell_output(response):
    return ''.join([stream[1]['text'] for stream in response ])

def _sos_to_java_type(obj):
    ''' Returns corresponding Java data type string for provided Python object '''
    if isinstance(obj, (int, np.intc, np.intp, np.int8, np.int16, np.int32, np.int64, bool, np.bool_)):
        if isinstance(obj, (bool, np.bool_)):
            return 'Boolean', 'true' if obj==True else 'false'
        elif obj >= -2147483648 and obj <= 2147483647:
            return 'Integer', repr(obj)
        elif obj >= -9223372036854775808 and obj <= 9223372036854775807:
            return 'Long', repr(obj)+'L'
        else:
            return -1, None #Integer is out of bounds
    elif isinstance(obj, (float, np.float16, np.float32, np.float64)):
        if (obj >= -3.40282e+38 and obj <= -1.17549e-38) or (obj >= 1.17549e-38 and obj <= 3.40282e+38):
            return 'Float', repr(obj)+'f'
        elif (obj >= -1.79769e+308 and obj <= -2.22507e-308) or (obj >= 2.22507e-308 and obj <= 1.79769e+308):
            return 'Double', repr(obj)
        else:
            return -1, None
    elif isinstance(obj, str):
        return 'String', '"'+obj+'"'
    
    else:
        return -1, None

def _java_scalar_to_sos(java_type, value):
    #Convert string value to appropriate type in SoS
    integer_types = ['Byte', 'Integer', 'Short', 'Long']
    real_types = ['Float', 'Double']
    if java_type in integer_types:
        return int(value)
    elif java_type in real_types:
        if value[-1] == 'f':
            value = value[:-1]
        return float(value)
    elif java_type == 'Character':
        return value
    elif java_type == 'String':
        return value
    elif java_type == 'Boolean':
        if value == 'true':
            return True
        else:
            return False

class sos_java:
    background_color = {'Java': '#F80000'}
    supported_kernels = {'Java': ['java']}
    options = {}
    cd_command = ''

    def __init__(self, sos_kernel, kernel_name='Java'):
        self.sos_kernel = sos_kernel
        self.kernel_name = kernel_name
        self.init_statements = java_init_statements

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
            if len(obj) == 0:
                #TODO: how to deal with an empty array?
                return ''
            else:
                #convert Python dict to Java Map
                if isinstance(obj, dict): 
                    keys = obj.keys()
                    values = obj.values()
                    if homogeneous_type(keys) and homogeneous_type(values):
                        dict_value = '; '.join([f'{name}.put({ _sos_to_java_type(d[0])[1] }, { _sos_to_java_type(d[1])[1] })' for d in obj.items()])
                        return f'Map<{_sos_to_java_type(next(iter(keys)))[0]}, {_sos_to_java_type(next(iter(values)))[0]}> {name} = new HashMap<>(); {dict_value}'
                elif isinstance(obj, Sequence):
                    if homogeneous_type(obj):
                        seq_value = ', '.join([_sos_to_java_type(s)[1] for s in obj])
                        el_type = _sos_to_java_type(next(iter(obj)))[0]
                        return f'ArrayList<{el_type}> {name} = new ArrayList<{el_type}>(Arrays.asList({seq_value}));'
                    else:
                        return None
                elif isinstance(obj, pd.core.frame.DataFrame):
                    dic = tempfile.tempdir
                    os.chdir(dic)
                    obj.to_csv('df2java.csv', index=False, quoting=csv.QUOTE_NONNUMERIC, quotechar='"')
                    return f'var {name} = Table.read().csv("{dic}/df2java.csv");'

        else:
            #unsupported type
            return None

    def get_vars(self, names):
        for name in names:
            java_repr = self._Java_declare_command_string(name, env.sos_dict[name])
            if not java_repr==None:
                self.sos_kernel.run_cell(java_repr, True, False,
                 on_error=f'Failed to put variable {name} to Java')
            else:
                self.sos_kernel.warn(f'Cannot convert variable {name} to Java')

    def put_vars(self, names, to_kernel=None):
        result = {}
        for name in names:
            java_type = self.sos_kernel.get_response(f'helper.getType({name})', ('execute_result',))[0][1]['data']['text/plain']

            if java_type in ('Boolean', 'Character', 'Byte', 'Short', 'Integer', 'Long', 'Float', 'Double', 'String'):
                #do scalar conversion
                value = self.sos_kernel.get_response(f'System.out.println({name});', ('stream',))[0][1]['text']
                result[name] = _java_scalar_to_sos(java_type, value)
            elif java_type == 'HashMap':
                value = self.sos_kernel.get_response(f'helper.printMap({name});', ('execute_result',))[0][1]['data']['text/plain']
                temp_dict = dict(eval(value))
                key_java_type = self.sos_kernel.get_response(f'helper.getMapKeyType({name})', ('execute_result',))[0][1]['data']['text/plain']
                val_java_type = self.sos_kernel.get_response(f'helper.getMapValueType({name})', ('execute_result',))[0][1]['data']['text/plain']
                result[name] = dict({_java_scalar_to_sos(key_java_type, key) : _java_scalar_to_sos(val_java_type, val) for (key, val) in temp_dict.items()})
            elif java_type == 'ArrayList':
                flat_list = '[' + self.sos_kernel.get_response(f'System.out.println(helper.printArray({name}))', ('stream',))[0][1]['text'] + ']'
                el_type = self.insistent_get_response(f'helper.getType({name}.get(0))', ('execute_result',))[0][1]['data']['text/plain']
                result[name] = np.array([_java_scalar_to_sos(el_type, el) for el in eval(flat_list)])
            elif java_type == 'Table':
                dic = tempfile.tempdir
                os.chdir(dic)
                self.sos_kernel.run_cell(f'{name}.write().csv("{dic}/java2df.csv");', True, False, on_error=f'Failed to write dataframe {name} to file')
                result[name] = pd.read_csv(f'{dic}/java2df.csv')
        return result
