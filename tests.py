#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest
import hashlib
import os
from D2P import *
from SWL import *


class Test(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_decompile_good_swl(self):
        SWL_stream = open("./samples/sample.swl", "rb")
        SWL = SWLFile()
        SWL.init(SWL_stream)
        SWL_stream.close()

    def test_decompile_bad_swl(self):
        SWL_stream = open("./samples/bad.swl", "rb")
        SWL = SWLFile()
        self.assertRaises(SWLInvalidFile, SWL.init, SWL_stream)
        SWL_stream.close()

    def test_build_swl(self):
        SWL_template_stream = open("./samples/sample.swl", "rb")
        SWL_template = SWLFile()
        SWL_template.init(SWL_template_stream)

        SWL_stream = open("./sample_compiled.swl", "wb")
        SWL = SWLFile()
        SWL.template = SWL_template
        SWL.SWF = SWL_template.SWF
        SWL.build(SWL_stream)

        SWL_template_stream.close()
        SWL_stream.close()

    def test_builded_swl(self):
        originalf = open("./samples/sample.swl", 'rb')
        original = hashlib.md5(originalf.read()).digest()
        originalf.close()

        buildedf = open("./sample_compiled.swl", 'rb')
        builded = hashlib.md5(buildedf.read()).digest()
        buildedf.close()
        try:
            os.remove("./sample_compiled.swl")
        except OSError:
            pass

        self.assertEqual(original, builded)

    def test_decompile_good_d2p(self):
        D2P_stream = open("./samples/sample.d2p", "rb")
        D2P = D2PFile()
        D2P.init(D2P_stream, False)
        D2P.load()
        D2P_stream.close()

    def test_decompile_bad_d2p(self):
        D2P_stream = open("./samples/bad.d2p", "rb")
        D2P = D2PFile()
        self.assertRaises(D2PInvalidFile, D2P.init, D2P_stream, False)
        self.assertRaises(Exception, D2P.load)
        D2P_stream.close()

    def test_build_d2p(self):
        D2P_template_stream = open("./samples/sample.d2p", "rb")
        D2P_template = D2PFile()
        D2P_template.init(D2P_template_stream)

        D2P_stream = open("./sample_compiled.d2p", "wb")
        D2P = D2PFile()
        D2P.template = D2P_template
        D2P.files = D2P_template.files
        D2P.build(D2P_stream)

        D2P_template_stream.close()
        D2P_stream.close()

    def test_builded_d2p(self):
        originalf = open("./samples/sample.d2p", 'rb')
        original = hashlib.md5(originalf.read()).digest()
        originalf.close()

        buildedf = open("./sample_compiled.d2p", 'rb')
        builded = hashlib.md5(buildedf.read()).digest()
        buildedf.close()
        try:
            os.remove("./sample_compiled.d2p")
        except OSError:
            pass

        self.assertEqual(original, builded)

if __name__ == '__main__':
    unittest.main()
