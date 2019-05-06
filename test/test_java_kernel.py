#!/usr/bin/env javascript
#
# Copyright (c) Konstantin Taletskiy
# Distributed under the terms of the MIT License.

import os
import unittest
from ipykernel.tests.utils import assemble_output, execute, wait_for_idle
from sos_notebook.test_utils import sos_kernel, get_result, get_display_data, clear_channels
from time import sleep

class TestJavaKernel(unittest.TestCase):

    def setUp(self):
        self.olddir = os.getcwd()
        if os.path.dirname(__file__):
            os.chdir(os.path.dirname(__file__))

    def tearDown(self):
        os.chdir(self.olddir)

    def testPythonToJavaScalars(self):
        with sos_kernel() as kc:
            iopub = kc.iopub_channel
            execute(kc=kc, code = '''
                import numpy as np
                int1 = 10
                int2 = 1000000000000000000
                int4 = np.intc(20)
                float1 = 0.1
                float2 = 1e+50
                string1 = 'abc'
                bool1 = True
                ''')
            wait_for_idle(kc)

            execute(kc=kc, code='%use Java')
            wait_for_idle(kc)

            execute(kc=kc, code='%get int1 int2 int4 float1 float2 string1 bool1')
            wait_for_idle(kc)

            #Test int1
            execute(kc=kc, code='System.out.println(int1);')
            stdout, _ = assemble_output(iopub)
            self.assertEqual(stdout.strip(),'10')

            #Test int2
            execute(kc=kc, code='System.out.println(int2);')
            stdout, _ = assemble_output(iopub)
            self.assertEqual(stdout.strip(),'1000000000000000000')

            #Test int4
            execute(kc=kc, code='System.out.println(int4);')
            stdout, _ = assemble_output(iopub)
            self.assertEqual(stdout.strip(),'20')

            #Test float1
            execute(kc=kc, code='System.out.println(float1);')
            stdout, _ = assemble_output(iopub)
            self.assertEqual(stdout.strip()[:3],'0.1')

            #Test float2
            execute(kc=kc, code='System.out.println(float2);')
            stdout, _ = assemble_output(iopub)
            self.assertEqual(stdout.strip(),'1.0E50')

            #Test string1
            execute(kc=kc, code='System.out.println(string1);')
            stdout, _ = assemble_output(iopub)
            self.assertEqual(stdout.strip(),'abc')

            #Test bool1
            execute(kc=kc, code='System.out.println(bool1);')
            stdout, _ = assemble_output(iopub)
            self.assertEqual(stdout.strip(),'true')

            execute(kc=kc, code="%use sos")
            wait_for_idle(kc)

    def testPythonToJavaDataframe(self):
        with sos_kernel() as kc:
            iopub = kc.iopub_channel
            execute(kc=kc, code = '''
                import numpy as np
                import pandas as pd
                dataframe = pd.DataFrame(np.random.randn(1000,4), columns=list('ABCD'))
                ''')

            wait_for_idle(kc)
            execute(kc=kc, code='%use Java')
            wait_for_idle(kc)
            execute(kc=kc, code='%get dataframe')
            wait_for_idle(kc)

            execute(kc=kc, code='System.out.println(dataframe.rowCount() * dataframe.columnCount());')
            stdout, _ = assemble_output(iopub)
            self.assertEqual(stdout.strip(),'4000')

            execute(kc=kc, code="%use sos")
            wait_for_idle(kc)

    def testJavatoPythonScalars(self):
        with sos_kernel() as kc:
            iopub = kc.iopub_channel

            execute(kc=kc, code='%use Java')
            wait_for_idle(kc)
            execute(kc=kc, code='''
                int i = 1;
                short si = 32;
                long li = 2000000000;
                float f = 0.1f;
                double d = 1e+300;
                boolean b = true;
                char c = '*';

                Map<String, String> m1 = new HashMap<>();
                m1.put(\"USA\", \"Washington\");
                m1.put(\"United Kingdom\", \"London\");
                m1.put(\"India\", \"New Delhi\");

                Map<Integer, Boolean> m2 = new HashMap<>();
                m2.put(1, true);
                m2.put(2, false);
                m2.put(3, true);

                ArrayList<Integer> l = new ArrayList<Integer>(Arrays.asList(1,2,3));    
                ''')
            wait_for_idle(kc)
            execute(kc=kc, code='%put i si li f d b c m1 m2 l')
            wait_for_idle(kc)
            execute(kc=kc, code='%use sos')
            wait_for_idle(kc)

            execute(kc=kc, code='print(i)')
            stdout, _ = assemble_output(iopub)
            self.assertEqual(stdout.strip(),'1')

            execute(kc=kc, code='print(si)')
            stdout, _ = assemble_output(iopub)
            self.assertEqual(stdout.strip(),'32')

            execute(kc=kc, code='print(li)')
            stdout, _ = assemble_output(iopub)
            self.assertEqual(stdout.strip(),'2000000000')

            execute(kc=kc, code='print(f)')
            stdout, _ = assemble_output(iopub)
            self.assertEqual(stdout.strip(),'0.1')

            execute(kc=kc, code='print(d)')
            stdout, _ = assemble_output(iopub)
            self.assertEqual(stdout.strip(),'1e+300')

            execute(kc=kc, code='print(b)')
            stdout, _ = assemble_output(iopub)
            self.assertEqual(stdout.strip(),'True')

            execute(kc=kc, code='print(c)')
            stdout, _ = assemble_output(iopub)
            self.assertEqual(stdout.strip(),'*')

            execute(kc=kc, code='print(m1["USA"])')
            stdout, _ = assemble_output(iopub)
            self.assertEqual(stdout.strip(),'Washington')

            execute(kc=kc, code='print(m2[2])')
            stdout, _ = assemble_output(iopub)
            self.assertEqual(stdout.strip(),'False')

            execute(kc=kc, code='print(l)')
            stdout, _ = assemble_output(iopub)
            self.assertEqual(stdout.strip(),'[1 2 3]')

    def testJavaToPythonDataframe(self):
        with sos_kernel() as kc:
            iopub = kc.iopub_channel

            execute(kc=kc, code='%use Java')
            wait_for_idle(kc)
            execute(kc=kc, code='''
                String[] animals = {"bear", "cat", "giraffe"};
                double[] cuteness = {90.1, 84.3, 99.7};
                Table cuteAnimals = Table.create("Cute Animals").addColumns(
                    StringColumn.create("Animal types", animals), DoubleColumn.create("rating", cuteness));     
                ''')
            wait_for_idle(kc)
            execute(kc=kc, code='%put cuteAnimals')
            wait_for_idle(kc)
            execute(kc=kc, code='%use sos')
            wait_for_idle(kc)

            execute(kc=kc, code='print(cuteAnimals["rating"][2])')
            stdout, _ = assemble_output(iopub)
            self.assertEqual(stdout.strip(),'99.7')

if __name__ == '__main__':
    unittest.main()