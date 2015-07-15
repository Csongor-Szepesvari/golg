"""Sample unit test file.

To read about unit tests in python check for example
    http://pymotw.com/2/unittest/
    http://jeffknupp.com/blog/2013/12/09/improve-your-python-understanding-unit-testing/
    http://www.drdobbs.com/testing/unit-testing-with-python/240165163
    
or more general information for why and how to do it at all, using python:
    http://jeffknupp.com/blog/2013/12/09/improve-your-python-understanding-unit-testing/
    

"""

import unittest

class BoardTest(unittest.TestCase):

    # preparing to test
    def setUp(self):
        """ Setting up for the test """
        print "FooTest:setUp_:begin"
        ## do something...
        print "FooTest:setUp_:end"
     
    # ending the test
    def tearDown(self):
        """Cleaning up after the test"""
        print "FooTest:tearDown_:begin"
        ## do something...
        print "FooTest:tearDown_:end"
     
    # test routine A
    def testA(self):
        """Test routine A"""
        print "FooTest:testA"
     
    # test routine B
    def testB(self):
        """Test routine B"""
        print "FooTest:testB"

    def test(self):
        self.failUnless(True)

if __name__ == '__main__':
    unittest.main()
