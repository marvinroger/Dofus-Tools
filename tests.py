#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest
import hashlib
import os

from pydofus.d2p import D2PReader, D2PBuilder, InvalidD2PFile
from pydofus.swl import SWLReader, SWLBuilder, InvalidSWLFile


class Test(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_decompile_good_swl(self):
        stream = open("./samples/sample.swl", "rb")
        SWL = SWLReader(stream)
        stream.close()

    def test_decompile_bad_swl(self):
        stream = open("./samples/bad.swl", "rb")
        self.assertRaises(InvalidSWLFile, SWLReader, stream)
        stream.close()

    def test_build_swl(self):
        template_stream = open("./samples/sample.swl", "rb")
        template = SWLReader(template_stream)

        builded_stream = open("./sample_compiled.swl", "wb")
        builder = SWLBuilder(template, builded_stream)
        builder.SWF = template.SWF
        builder.build()

        template_stream.close()
        builded_stream.close()

    def test_builded_swl(self):
        originalf = open("./samples/sample.swl", 'rb')
        original = hashlib.md5(originalf.read()).digest()
        originalf.close()

        buildedf = open("./sample_compiled.swl", 'rb')
        builded = hashlib.md5(buildedf.read()).digest()
        buildedf.close()
        try:
            os.remove("./sample_compiled.swl")
        except OSError as e:
            print(str(e))

        self.assertEqual(original, builded)

    def test_decompile_good_d2p(self):
        stream = open("./samples/sample.d2p", "rb")
        D2P = D2PReader(stream, False)
        D2P.load()
        stream.close()

    def test_decompile_bad_d2p(self):
        stream = open("./samples/bad.d2p", "rb")
        self.assertRaises(InvalidD2PFile, D2PReader, stream, False)
        stream.close()

    def test_build_d2p(self):
        template_stream = open("./samples/sample.d2p", "rb")
        template = D2PReader(template_stream)

        builded_stream = open("./sample_compiled.d2p", "wb")
        builder = D2PBuilder(template, builded_stream)
        builder.files = template.files
        builder.build()

        template_stream.close()
        builded_stream.close()

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
