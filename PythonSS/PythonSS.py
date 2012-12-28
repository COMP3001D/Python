import webapp2
import random
import hashlib
from datetime import datetime

from google.appengine.ext import db

class Books(db.Model):
    Title = db.StringProperty()
    Author = db.StringProperty()
    Summary = db.StringProperty(multiline=True)
    Year = db.IntegerProperty()
    Publisher = db.StringProperty()
    Genre = db.StringProperty()
    FilePath = db.StringProperty()

class BookUsers(db.Model):
    Email = db.EmailProperty()
    PasswordHash = db.StringProperty()

class Shelf(db.Model):
    Favourite = db.BooleanProperty()
    TimeStamp = db.DateTimeProperty()

class Main(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write("""This page describes the handlers that have been coded so far

Search: This is the handler for searching through the database of books and can be accessed through
"comp3001teamd.appspot.com/search?querystringhere". Currently the query_string is not used except for
the title field. It returns a JSON object containing a list of books, this is still a test stub.
It is accessed using the get method

Login: For logging users in to the app. this returns a plaintext document containing 1 or 0
indicating whether the user was authenticated or not respectively. This is accessed through
"comp3001teamd.appspot.com/login?username=xyz&password=xyz" using the post method

AddAdmin: Just for adding a user to test the app. Username: Am, email: am@am.am, password: 12345
Accessed from "comp3001teamd.appspot.com/addAdmin". In order to do this, you will need to go to
the url from your browser. Do not use it in your code as it will be removed in the final version.

GetList: For returning a list of books the user had bookmarked. Returns a JSON object containing a
list of books. Can be accessed through "comp3001teamd.appspot.com/getUserList?username=xyz"
Accessed using the get method

GetAll: Returns a list of all books in the library. It returns a JSON object containing a list of books.
Can be accessed through "comp3001teamd.appspot.com/getAll" (this does not require a query string), using
the get method

AddBooks: For populating the books entity. Used for testing purposes. (should only need to run once)
Can be accessed through "comp3001teamd.appspot.com/addBooks". This will also need to be run from the
browser. Do not use it as it will be removed in the final version.

Register: This is for registering a user. It can be accessed using the post method. It requires the user,
password and email address to exist in the query string. It returns a text/plain document as a response.
It returns 0 if the username already exists and 1 if it doesn't and has been added to the database
The url for this is "comp3001teamd.appspot.com/register?name=xyz&password=xyz&email=xyz@xyz.xyz".

AddToShelf: This is for a user to be able to bookmark books and add them to their shelf. It is
accessed using the get method from the url "comp3001teamd.appspot.com/addToShelf?username=xyz&ISBN=xyz"

MakeFavourite: This is for changing the favourite value of a book that has been added to the shelf.
It can be accessed using the get method at "comp3001teamd.appspot.com/makeFav?username=xyz&ISBN=xyz"
It returns a text/plain document containing a "1" if it is successful or "0" if the book does not
exist on the shelf. If the favourite value is false, this will change it to true and vice versa

GetSummary: This is for obtaining the summary for a particular book. It returns a JSON object containing
the said summary. It can be accessed through "comp3001teamd,appspot.com/getSummary?ISBN=xyz"

Note: In order to view/edit the contents of the datastore by hand, you will need to log into google
using our group account and go onto the dashboard for the app at "appengine.google.com"

Note: comp3001teamd.appspot.com on it's own should not return anything in future, so don't use it.

Good luck and good night.""")

class Search(webapp2.RequestHandler): # TODO replace test stub
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
    def post(self):
        self.response.headers['Content-Type'] = 'text/plain'
        username = self.request.get('username')
        passhash = hashlib.sha1(self.request.get('password')).hexdigest()
        user = BookUsers.get_by_key_name(username);
        if user is None:
            self.response.write("01")
            return
        elif passhash != user.PasswordHash:
            self.response.write("02")
        else:
            self.response.write("1")

class AddToShelf(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        username = self.request.get('username')
        user = BookUsers.get_by_key_name(username)
        ISBN = self.request.get('ISBN')
        book = Books.get_by_key_name(ISBN)
        if book is None:
            self.response.write("0")
        else:
            s = Shelf(parent = user, key_name = ISBN)
            s.Favourite = False
            s.TimeStamp = datetime.today()
            s.put()
            self.response.write("1")

class MakeFavourite(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        username = self.request.get('username')
        user = BookUsers.get_by_key_name(username)
        ISBN = self.request.get('ISBN')
        books = db.GqlQuery("SELECT * FROM Shelf WHERE ANCESTOR IS :1", user)
        for book in books:
            if book.key().name() == ISBN:
                book.Favourite = (book.Favourite ^ True)
                self.response.write("1")
                book.put()
                return
	self.response.write("0")

class GetList(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/javascript'
        username = self.request.get('username')
        user = BookUsers.get_by_key_name(username)
        books = db.GqlQuery("SELECT * FROM Shelf WHERE ANCESTOR IS :1", user)
        c = 0;
        self.response.write('{ "books": [')
        for book in books:
            bookrec = Books.get_by_key_name(book.key().name())
            if c == 0:
                c = 1
            else:
                self.response.write(',')
            self.response.write('{"title": "' + bookrec.Title + '",')
            self.response.write('"author": "' + bookrec.Author + '",')
            self.response.write('"year": "' + str(bookrec.Year) + '",')
            self.response.write('"ISBN": "' + bookrec.key().name() + '",')
            self.response.write('"publisher": "' + bookrec.Publisher + '",')
            self.response.write('"genres": "' + bookrec.Genre + '"}')

class AddAdmin(webapp2.RequestHandler): # TODO test handler, delete in final
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        e = BookUsers(key_name = "Am")
        e.Email = "am@am.am"
        e.PasswordHash = hashlib.sha1("12345").hexdigest()
        e.put()
        self.response.write("Done")

class Register(webapp2.RequestHandler):
    def post(self):
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

class AddBooks(webapp2.RequestHandler): # TODO test handler, delete in final
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        b = Books(key_name = "0747532699")
        b.Title = "Harry Potter and the Philosopher's Stone"
        b.Author = "J. K. Rowling"
        b.Year = 1997
        b.Publisher = "Bloomsbury"
        b.Genre = "Fantasy"
        b.Summary = "abcde"
        b.FilePath = "a/b"
        b.put()

        b = Books(key_name = "0747538492")
        b.Title = "Harry Potter and the Chamber of Secrets"
        b.Author = "J. K. Rowling"
        b.Year = 1998
        b.Publisher = "Bloomsbury"
        b.Genre = "Fantasy"
        b.Summary = "abcde"
        b.FilePath = "a/b"
        b.put()

        b = Books(key_name = "0670899623")
        b.Title = "Artemis Fowl"
        b.Author = "Eoin Colfer"
        b.Year = 2001
        b.Publisher = "Viking Press"
        b.Genre = "Young-Adult Fantasy"
        b.Summary = "abc"
        b.FilePath = "a/c"
        b.put()

        b = Books(key_name = "0786808551")
        b.Title = "Artemis Fowl: The Arctic Incident"
        b.Author = "Eoin Colfer"
        b.Year = 2002
        b.Publisher = "Hyperion Books"
        b.Genre = "Childrens Fantasy"
        b.Summary = "abc"
        b.FilePath = "a/c"
        b.put() 

        b = Books(key_name = "000000000001")
        b.Title = "The Hobbit"
        b.Author = "J. R. R. Tolkien"
        b.Year = 1937
        b.Publisher = "George Allen & Unwin"
        b.Genre = "High-fantasy Adventure"
        b.Summary = "abcd"
        b.FilePath = "a/d"
        b.put()

        b = Books(key_name = "000000000002")
        b.Title = "A Study in Scarlet"
        b.Author = "Arthur Conan Doyle"
        b.Year = 1887
        b.Publisher = "Ward Lock & Co"
        b.Genre = "Detective Crime Mystery Novel"
        b.Summary = "abcdef"
        b.FilePath = "a/e"
        b.put()

        self.response.write("done")

class GetAll(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/javascript'
        self.response.write('{ "books" : [')
        books = db.GqlQuery("SELECT * FROM Books")
        c = 0;
        for book in books:
            if c == 0:
                c = 1
            else:
                self.response.write(",")
            self.response.write('{"title": "' + book.Title + '",')
            self.response.write('"author": "' + book.Author + '",')
            self.response.write('"year": "' + str(book.Year) + '",')
            self.response.write('"ISBN": "' + book.key().name() + '",')
            self.response.write('"publisher": "' + book.Publisher + '",')
            self.response.write('"genres": "' + book.Genre + '"}')
        self.response.write(']}')

class GetSummary(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/javascript'
        ISBN = self.request.get('ISBN')
        book = Books.get_by_key_name(ISBN)
        self.response.write('{ "Summary": "' + book.Summary + '"}')

app = webapp2.WSGIApplication([('/', Main),
                               ('/search', Search),
                               ('/login', Login),
                               ('/addToShelf', AddToShelf),
                               ('/makeFav', MakeFavourite),
                               ('/getUserList', GetList),
                               ('/register', Register),
                               ('/addAdmin', AddAdmin),
                               ('/getAll', GetAll),
                               ('/addBooks', AddBooks),
                               ('/getSummary', GetSummary)],
                                debug = True)

