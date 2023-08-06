'''
Created on Nov 5, 2019

@author: reynolds
'''

import unittest
from wrtdk.data.buffer.buffer import ring_buffer
from sympy.physics.units.dimensions import length

class test_ring_buffer(unittest.TestCase):
    '''
    classdocs
    '''
    
    def test_length(self):
        length = 100
        b = ring_buffer(length)
        self.assertEqual(b.get_length(),length)
        
    def test_set_length(self):
        length = 10
        b = ring_buffer()
        b.set_length(length)
        self.assertEqual(b.get_length(),length,length)
        
    def test_is_full(self):
        length = 1
        b = ring_buffer(length)
        before = b.is_full()
        b.append(0)
        self.assertNotEqual(before,b.is_full())
        
    def test_append(self):
        x = 10
        b = ring_buffer()
        b.append(x)
if __name__ == '__main__':
    unittest.main()
        