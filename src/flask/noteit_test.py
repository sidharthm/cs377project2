import os
import index
import unittest
import tempfile
class indexTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, index.app.config['DATABASE'] = tempfile.mkstemp()
        self.app = index.app.test_client()
        index.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(index.app.config['DATABASE'])

    def test_empty_db(self):
    	#This tests whether the program has the basic components/links in it in at least plain-text form
        rv = self.app.get('/')
        assert 'Note-It' in rv.data
        assert 'Home' in rv.data
        assert 'Log-In' in rv.data
        assert 'Register' in rv.data
if __name__ == '__main__':
    unittest.main()