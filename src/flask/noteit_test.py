import os
import index
import unittest
import tempfile
class indexTestCase(unittest.TestCase):

#Testing Methods 

    def setUp(self):
        index.app.config['DATABASE'] = os.path.join(index.app.root_path,'flaskr.db')
        index.app.config['TESTING'] = True
        self.app = index.app.test_client()
        index.init_db()

    def tearDown(self):
        os.unlink(index.app.config['DATABASE'])

    def register(self,username,password, email):
        return self.app.post('/registration', data = dict(
				username = username,
				password = password,
				email = email
            ), follow_redirects=True)

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

     
    def newNotes(self,user_id,title,content,color): 
	return self.app.post('/notes/new', data=dict(
            user_id=user_id,
            title=title,
	    content=content,
		color=color,
        ), follow_redirects=True)
    #Reviewed by Sid & Jimmy 2:51 PM 4/15
    #Need to update syntax to fit Roy's planned syntax


    def deleteNotes(self,id):
        return self.app.post('/notes/delete', data=dict(
            id=id,
        ), follow_redirects=True)
    #Reviewed by Sid & Jimmy 2:51 PM 4/15
    #Need to update syntax to fit Roy's planned syntax


#Tests are listed below

    def test_empty_db(self):
    	#This tests whether the program has the basic components/links in it in at least plain-text form
        rv = self.app.get('/')
        assert 'Note-It' in rv.data
        #assert 'Home' in rv.data deprecated
        assert 'login' in rv.data
        assert 'Register' in rv.data

    def test_register(self):
        #This test ensures that new accounts can be made, and that duplicate accounts do not exist
        #Test Part 1 - create a new user in the system
        rv = self.register('admin','password', 'email')
        assert 'Account created' in rv.data
        #Test Part 2 - attempt to make a duplicate user
        rv = self.register('admin','another', 'email')
        assert 'Username taken'

    def test_invalid_login(self):
        #This test makes sure that the login function only accepts valid inputs
        #Pre-conditions
        rv = self.register('admin','password', 'email') #user exists in the system
        #Test Part 1 - invalid username
        rv = self.login('adminx', 'default')
        assert 'Invalid username/password combination' in rv.data
        #Test Part 2 - invalid password
        rv = self.login('admin', 'defaultx')
        assert 'Invalid username/password combination' in rv.data

    def test_double_login(self):
        #This test makes sure that you can't log in twice
        #Pre-conditions
        rv = self.register('admin','password', 'email') #user exists in the system
        rv = self.login('admin','password') #user is logged in 
        #Test - User attempts to log in again with invalid credentials
        rv = self.login('adminx','password')
        assert 'You are already logged in'
        #Test - User attempts to log in again with valid credentials
        rv = self.login('admin','password')
        assert 'You are already logged in'

    def test_register_login_logout(self):
        #This test simulates the user's basic interaction with the software
        #Test Part 1 - User creates an account
        rv = self.register('admin','password', 'email')
        assert 'Account created' in rv.data
        #Test Part 2 - User logs into their account
        rv = self.login('admin', 'password')
        assert 'Logged in successfully'
        #Test Part 3 - User logs out of their account
        rv = self.logout()
        assert 'Logged out successfully'

    def test_newNotes(self):
	#This test ensures a new note can be created
        #Test Part 1 - User creates an account
        rv = self.register('admin','password', 'email')
        assert 'Account created' in rv.data
        #Test Part 2 - User logs into their account
        rv = self.login('admin', 'password')
        assert 'Logged in successfully'
		#Test Part 2 - User can create a new note
        rv = self.newNotes('admin','NewNote','notecontent','yellow')
        assert 'good' in rv.data

    def test_deleteNotes(self):
	#This test ensures that the deleted note is removed from the database
        rv = self.deleteNotes('admin')
        assert 'good' in rv.data

    #Reviewed by Sid & Jimmy 2:51 PM 4/15
    #Need to roll these tests together to account for spontaneous DB generation


if __name__ == '__main__':
    unittest.main()