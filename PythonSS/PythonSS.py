import webapp2
import random
import hashlib

from google.appengine.ext import db

class Books(db.Model):
    Title = db.StringProperty()
    Author = db.StringProperty()
    ISBN = db.StringProperty()
    Summary = db.StringProperty(multiline=True)
    Year = db.DateProperty()
    Publisher = db.StringProperty()
    Genre = db.StringProperty()

class BookUsers(db.Model):
    Email = db.EmailProperty()
    PasswordHash = db.StringProperty()

class Main(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write("""I have uploaded test handlers for the script, which are described here on

Search: This is the handler for searching through the database of books and can be accessed through
comp3001teamd.appspot.com/search?querystringhere. Currently the query_string is not used except for
the title field. It returns a JSON object containing a list of books

Login: For logging users in to the app. this returns a plaintext document containing True or False
indicating whether the user was authenticated or not. This is accessed through
comp3001teamd.appspot.com/login?querystringhere. Enter password=1 for successful login or 0 for
fail login, anything else and the result will be random.

GetList: For returning a list of books the user had bookmarked. Returns a JSON object containing a
list of books. Can be accessed through comp3001teamd.appspot.com/getUserList?querystringhere

GetAll: Returns a list of all books in the library. It returns a JSON object containing a list of books.
Can be accessed through comp3001teamd.appspot.com/getAll (don't think this requires a query string)

Register: This is for registering a user. It can be accessed using the post method. It requires the user,
password and email address to exist in the query string. It returns a text/plain document as a response.
It returns 0 if the username already exists and 1 if it doesn't and has been added to the database
The url for this is comp3001teamd.appspot.com/register.

Note: comp3001teamd.appspot.com on it's own should not return anything in future, so don't use it.""")

class Search(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/javascript'
        booktitle = self.request.get('title')
        if booktitle.lower().replace(" ", "") == "harrypotter":
            self.response.write("""{ "books" : [{
                                    "title": "Harry Potter and the Philosopher's Stone",
                                    "author": "J. K. Rowling",
                                    "year": "1997",
                                    "ISBN": "111",
                                    "publisher": "Bloomsbury",
                                    "genres": "Fantasy"
                                    },
                                    {
                                    "title": "Harry Potter and the Chamber of Secrets",
                                    "author": "J. K. Rowling",
                                    "year": "1998",
                                    "ISBN": "112",
                                    "publisher": "Bloomsbury",
                                    "genres": "Fantasy"
                                    }]}
                                """)
        elif booktitle.lower().replace(" ", "") == "artemisfowl":
            self.response.write("""{ "books" : [{
                                    "title": "Artemis Fowl",
                                    "author": "Eoin Colfer",
                                    "year": "2001",
                                    "ISBN": "113",
                                    "publisher": "Viking Press",
                                    "genres": "Young-Adult Fantasy"
                                    },
                                    { "title": "Artemis Fowl: The Arctic Incident",
                                    "author": "Eoin Colfer",
                                    "year": "2002",
                                    "ISBN": "114",
                                    "publisher": "Hyperion Books"
                                    "genres": "Childrens Fantasy"
                                    }]}
                                """)
        else:
            self.response.write("""{ "books" : [{
                                    "title": "The Hobbit",
                                    "author": "J. R. R. Tolkien",
                                    "year": "1937",
                                    "ISBN": "115",
                                    "publisher": "George Allen & Unwin",
                                    "genres": "High-fantasy Adventure"
                                    },
                                    { "title": "A Study in Scarlet",
                                    "author": "Arthur Conan Doyle",
                                    "year": "1887",
                                    "ISBN": "116",
                                    "publisher": "Ward Lock & Co",
                                    "genres" : "Detective Crime Mystery Novel"
                                    }]}
                                """)

class Login(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        password = self.request.get('password')
        if password == '1':
            self.response.write('True')
        elif password == '0':
            self.response.write('False')
        else:
            num = random.randint(0, 1);
            if num == 1:
                self.response.write('True')
            else:
                self.response.write('False')

class GetList(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/javascript'
        self.response.write("""{ "books" : [{
                                    "title": "The Hobbit",
                                    "author": "J. R. R. Tolkien",
                                    "year": "1937",
                                    "ISBN": "115",
                                    "publisher": "George Allen & Unwin",
                                    "genres": "High-fantasy Adventure"
                                    },
                                    "title": "Harry Potter and the Chamber of Secrets",
                                    "author": "J. K. Rowling",
                                    "year": "1998",
                                    "ISBN": "112",
                                    "publisher": "Bloomsbury",
                                    "genres": "Fantasy"
                                    }]}
                                """)

class AddAdmin(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        e = BookUsers(key_name = "Am")
        e.Email = "am@am.am"
        e.PasswordHash = "12345"
        e.put()
        self.response.write("Done")

class Register(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        username = self.request.get('name')
        user = BookUsers.get_by_key_name(username)
        if user is None:
            password = self.request.get('password');
            email = self.request.get('email');
            e = BookUsers(key_name = username)
            e.Email = email
            e.PasswordHash = hashlib.sha1(password).hexdigest()
            e.put()
            self.response.write("1")
        else:
            self.response.write("0")

class GetAll(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/javascript'
        self.response.write("""{ "books" : [{
                                    "title": "Harry Potter and the Philosopher's Stone",
                                    "author": "J. K. Rowling",
                                    "year": "1997",
                                    "ISBN": "111",
                                    "publisher": "Bloomsbury",
                                    "genres": "Fantasy"
                                    },
                                    {
                                    "title": "Harry Potter and the Chamber of Secrets",
                                    "author": "J. K. Rowling",
                                    "year": "1998",
                                    "ISBN": "112",
                                    "publisher": "Bloomsbury",
                                    "genres": "Fantasy"
                                    },
                                    {
                                    "title": "Artemis Fowl",
                                    "author": "Eoin Colfer",
                                    "year": "2001",
                                    "ISBN": "113",
                                    "publisher": "Viking Press",
                                    "genres": "Young-Adult Fantasy"
                                    },
                                    { "title": "Artemis Fowl: The Arctic Incident",
                                    "author": "Eoin Colfer",
                                    "year": "2002",
                                    "ISBN": "114",
                                    "publisher": "Hyperion Books"
                                    "genres": "Childrens Fantasy"
                                    },{
                                    "title": "The Hobbit",
                                    "author": "J. R. R. Tolkien",
                                    "year": "1937",
                                    "ISBN": "115",
                                    "publisher": "George Allen & Unwin",
                                    "genres": "High-fantasy Adventure"
                                    },
                                    { "title": "A Study in Scarlet",
                                    "author": "Arthur Conan Doyle",
                                    "year": "1887",
                                    "ISBN": "116",
                                    "publisher": "Ward Lock & Co",
                                    "genres" : "Detective Crime Mystery Novel"
                                    }]}
                                """)

app = webapp2.WSGIApplication([('/', Main),
                               ('/search', Search),
                               ('/login', Login),
                               ('/getUserList', GetList),
                               ('/register', Register),
                               ('/addAdmin', AddAdmin),
                               ('/getAll', GetAll)],
				debug = True)

