#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from chibi_hybrid.chibi_hybrid import Chibi_hybrid


class Dump:
    def __init__( self, value ):
        self.value = value

    @Chibi_hybrid
    def foo( cls ):
        return cls( 'cls' )

    @foo.instancemethod
    def foo( self ):
        return self.value


class Test_chibi_hybrid(unittest.TestCase):
    def test_should_work(self):
        result = Dump.foo()
        self.assertIsInstance( result, Dump )
        self.assertEqual( 'cls', result.value )
        self.assertEqual( 'cls', result.foo() )

        result = Dump( 'cosa' ).foo()
        self.assertEqual( 'cosa', result )
