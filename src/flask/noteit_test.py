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

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_login_logout(self):
        rv = self.login('admin', 'default')
        assert 'You were logged in' in rv.data
        rv = self.logout()
        assert 'You were logged out' in rv.data
        rv = self.login('adminx', 'default')
        assert 'Invalid username' in rv.data
        rv = self.login('admin', 'defaultx')
        assert 'Invalid password' in rv.data
        
if __name__ == '__main__':
    unittest.main()