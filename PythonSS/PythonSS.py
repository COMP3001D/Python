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
    Country = db.StringProperty()
    Language = db.StringProperty()

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
"comp3001teamd.appspot.com/search?title=xyz&author=xyz&year=x&ISBN=xyz&publisher=xyz&genre=xyz
&country=xyz&language=xyz&callback=xyz". Each field in the query string is optional except the callback.
An empty query string will return an empty list of books. It returns a JSONP object containing a list
of books. It is accessed using the get method

Login: For logging users in to the app. This returns a JSONP object. It has one field called "success"
containing 1 or 0 indicating whether the user was authenticated or not respectively. This is accessed
through "comp3001teamd.appspot.com/login?username=xyz&password=xyz&callback=xyz" using the post method

AddAdmin: Just for adding a user to test the app. Username: Am, email: am@am.am, password: 12345
Accessed from "comp3001teamd.appspot.com/addAdmin". In order to do this, you will need to go to
the url from your browser. Do not use it in your code as it will be removed in the final version.

GetList: For returning a list of books the user had bookmarked. Returns a JSONP object containing a
list of books. Can be accessed through "comp3001teamd.appspot.com/getUserList?username=xyz&callback=xyz"
Accessed using the get method

GetAll: Returns a list of all books in the library. It returns a JSONP object containing a list of books.
Can be accessed through "comp3001teamd.appspot.com/getAll?callback=xyz" using the get method

AddBooks: For populating the books entity. Used for testing purposes. (should only need to run once)
Can be accessed through "comp3001teamd.appspot.com/addBooks". This will also need to be run from the
browser. Do not use it as it will be removed in the final version.

Register: This is for registering a user. It can be accessed using the post method. It requires the username,
password and email address to exist in the query string. It returns a JSONP object as a response.
It contains a success field containing 0 if the username already exists and 1 if it doesn't and has been
added to the database The url for this is
"comp3001teamd.appspot.com/register?name=xyz&password=xyz&email=xyz@xyz.xyz&callback=xyz".

AddToShelf: This is for a user to be able to bookmark books and add them to their shelf. It is
accessed using the get method from the url "comp3001teamd.appspot.com/addToShelf?username=xyz&ISBN=xyz&callback=xyz"
This returns a JSONP object with the usual success field indicating 1 for success and 0 for failure

MakeFavourite: This is for changing the favourite value of a book that has been added to the shelf.
It can be accessed using the get method at "comp3001teamd.appspot.com/makeFav?username=xyz&ISBN=xyz&callback=xyz"
It returns a JSONP object containing a success field which will contain a "1" if it is successful or
"0" if the book does not exist on the shelf. If the favourite value is false, this will change it to
true and vice versa

GetSummary: This is for obtaining the summary for a particular book. It returns a JSONP object containing
the said summary. It can be accessed through "comp3001teamd,appspot.com/getSummary?ISBN=xyz&callback=xyz"

Note: In order to view/edit the contents of the datastore by hand, you will need to log into google
using our group account and go onto the dashboard for the app at "appengine.google.com"

Note: comp3001teamd.appspot.com on it's own should not return anything in future, so don't use it.

Good luck and good night.""")

class Search(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/javascript'
        title = self.request.get('title')
        author = self.request.get('author')
        year = self.request.get('year')
        ISBN = self.request.get('ISBN')
        publisher = self.request.get('publisher')
        genre = self.request.get('genre')
        country = self.request.get('country')
        language = self.request.get('language')
	callback = self.request.get('callback')
        booksquery = db.GqlQuery("SELECT * FROM Books")
        number = booksquery.count()
        books = [0] * number
        for x in range(number):
            books[x] = booksquery[x]
        scores = [0] * number
        for x in range(number):
            if title != "":
                tt = title.lower().replace(" ","").replace(".","").replace(",","").replace("-","").replace(":","")
                tc = books[x].Title.lower().replace(" ","").replace(".","").replace(",","").replace("-","").replace(":","")
                if tt == tc:
                    scores[x] += 2
                elif tc.find(tt) != -1:
                    scores[x] += 1
            if country != "":
                ct = country.lower().replace(" ","").replace(".","").replace(",","").replace("-","").replace(":","")
                cc = books[x].Country.lower().replace(" ","").replace(".","").replace(",","").replace("-","").replace(":","")
                if ct == cc:
                    scores[x] += 2
                elif cc.find(ct) != -1:
                    scores[x] += 1
            if language != "":
                lt = language.lower().replace(" ","").replace(".","").replace(",","").replace("-","").replace(":","")
                lc =books[x].Language.lower().replace(" ","").replace(".","").replace(",","").replace("-","").replace(":","")
                if lt == lc:
                    scores[x] += 2
                elif tc.find(lt) != -1:
                    scores[x] += 1
            if author != "":
                at = author.lower().replace(" ","").replace(".","").replace(",","").replace("-","").replace(":","")
                ac = books[x].Author.lower().replace(" ","").replace(".","").replace(",","").replace("-","").replace(":","")
                if at == ac:
                    scores[x] += 2
                elif ac.find(at) != -1:
                    scores[x] += 1
            if year != "":
                year = int(year)
                if year == books[x].Year:
                    scores[x] += 2
            if ISBN != "":
                if ISBN == books[x].ISBN:
                    scores[x] += 2
                elif Books[x].find(ISBN) != -1:
                    scores[x] += 1
            if publisher != "":
                pt = publisher.lower().replace(" ","").replace(".","").replace(",","").replace("-","").replace(":","")
                pc=books[x].Publisher.lower().replace(" ","").replace(".","").replace(",","").replace("-","").replace(":","")
                if pt == pc:
                    scores[x] += 2
                elif pc.find(pt) != -1:
                    scores[x] += 1
            if genre != "":
                gt = genre.lower().replace(" ","").replace(".","").replace(",","").replace("-","").replace(":","")
                gc = Books[x].Genre.lower().replace(" ","").replace(".","").replace(",","").replace("-","").replace(":","")
                if gc.find(gt) != -1:
                    scores[x] += 2
        for x in range(number):
            highest = x
            for y in range(x, number):
                if scores[y] > scores[highest]:
                    highest = y
            if highest != x:
                temp = scores[x]
                scores[x] = scores[highest]
                scores[highest] = temp
                temp = books[x]
                books[x] = books[highest]
                books[highest] = temp
        self.response.write(callback + '({ "books": [')
        c = 0;
        x = 0;
        while (x < number) and (scores[x] != 0):
            if c == 0:
                c = 1
            else:
                self.response.write(",")
            self.response.write('{"title": "' + books[x].Title + '",')
            self.response.write('"author": "' + books[x].Author + '",')
            self.response.write('"year": "' + str(books[x].Year) + '",')
            self.response.write('"ISBN": "' + books[x].key().name() + '",')
            self.response.write('"publisher": "' + books[x].Publisher + '",')
            self.response.write('"genres": "' + books[x].Genre + '",') 
            self.response.write('"country": "' + books[x].Country + '",')
            self.response.write('"language": "' + books[x].Language + '"}')
            x += 1
        self.response.write("]})")

class Login(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/javascript'
        username = self.request.get('username')
        passhash = hashlib.sha1(self.request.get('password')).hexdigest()
	callback = self.request.get('callback')
	self.response.write(callback + '({ "success": "')
        user = BookUsers.get_by_key_name(username);
        if user is None:
            self.response.write("0")
        elif passhash != user.PasswordHash:
            self.response.write("0")
        else:
            self.response.write("1")
	self.response.write('"})')

class AddToShelf(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/javascript'
        username = self.request.get('username')
	callback = self.request.get('callback')
        user = BookUsers.get_by_key_name(username)
        ISBN = self.request.get('ISBN')
        book = Books.get_by_key_name(ISBN)
	self.response.write(callback + '({ "success" : "')
        if book is None or user is None:
            self.response.write("0")
        else:
            s = Shelf(parent = user, key_name = ISBN)
            s.Favourite = False
            s.TimeStamp = datetime.today()
            s.put()
            self.response.write("1")
	self.response.write('"})')

class MakeFavourite(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/javascript'
        username = self.request.get('username')
	callback = self.request.get('callback')
        user = BookUsers.get_by_key_name(username)
        ISBN = self.request.get('ISBN')
        books = db.GqlQuery("SELECT * FROM Shelf WHERE ANCESTOR IS :1", user)
	self.response.write(callback + '({ "success": "')
        for book in books:
            if book.key().name() == ISBN:
                book.Favourite = (book.Favourite ^ True)
                book.put()
                self.response.write("1")
		self.response.write('"})')
                return
	self.response.write("0")
	self.response.write('"})')

class GetList(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/javascript'
        username = self.request.get('username')
	callback = self.request.get('callback')
        user = BookUsers.get_by_key_name(username)
        books = db.GqlQuery("SELECT * FROM Shelf WHERE ANCESTOR IS :1", user)
        c = 0;
        self.response.write(callback + '({ "books": [')
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
            self.response.write('"genres": "' + bookrec.Genre + '",')
            self.response.write('"country": "' + bookrec.Country + '",')
            self.response.write('"language": "' + bookrec.Language + '"}')
        self.response.write("]})")

class AddAdmin(webapp2.RequestHandler): # TODO test handler, delete in final
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        e = BookUsers(key_name = "Am")
        e.Email = "am@am.am"
        e.PasswordHash = hashlib.sha1("12345").hexdigest()
        e.put()
        self.response.write("Done")

class Register(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/javascript'
        username = self.request.get('name')
	callback = self.request.get('callback')
        user = BookUsers.get_by_key_name(username)
        self.response.write(callback + '({ "success": "')
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
        self.response.write('"})')

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
        b.Country = "UK"
        b.Language = "English"
        b.put()

        b = Books(key_name = "0747538492")
        b.Title = "Harry Potter and the Chamber of Secrets"
        b.Author = "J. K. Rowling"
        b.Year = 1998
        b.Publisher = "Bloomsbury"
        b.Genre = "Fantasy"
        b.Summary = "abcde"
        b.FilePath = "a/b"
        b.Country = "UK"
        b.Language = "English"
        b.put()

        b = Books(key_name = "0670899623")
        b.Title = "Artemis Fowl"
        b.Author = "Eoin Colfer"
        b.Year = 2001
        b.Publisher = "Viking Press"
        b.Genre = "Young-Adult Fantasy"
        b.Summary = "abc"
        b.FilePath = "a/c"
        b.Country = "Ireland"
        b.Language = "English"
        b.put()

        b = Books(key_name = "0786808551")
        b.Title = "Artemis Fowl: The Arctic Incident"
        b.Author = "Eoin Colfer"
        b.Year = 2002
        b.Publisher = "Hyperion Books"
        b.Genre = "Childrens Fantasy"
        b.Summary = "abc"
        b.FilePath = "a/c"
        b.Country = "Ireland"
        b.Language = "English"
        b.put() 

        b = Books(key_name = "000000000001")
        b.Title = "The Hobbit"
        b.Author = "J. R. R. Tolkien"
        b.Year = 1937
        b.Publisher = "George Allen & Unwin"
        b.Genre = "High-fantasy Adventure"
        b.Summary = "abcd"
        b.FilePath = "a/d"
        b.Country = "UK"
        b.Language = "English"
        b.put()

        b = Books(key_name = "000000000002")
        b.Title = "A Study in Scarlet"
        b.Author = "Arthur Conan Doyle"
        b.Year = 1887
        b.Publisher = "Ward Lock & Co"
        b.Genre = "Detective Crime Mystery Novel"
        b.Summary = "abcdef"
        b.FilePath = "a/e"
        b.Country = "UK"
        b.Language = "English"
        b.put()

        self.response.write("done")

class GetAll(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/javascript'
	callback = self.request.get('callback')
        self.response.write(callback + '({ "books" : [')
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
            self.response.write('"genres": "' + book.Genre + '",')
            self.response.write('"country": "' + book.Country + '",')
            self.response.write('"language": "' + book.Language + '"}')
        self.response.write(']})')

class GetSummary(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/javascript'
        ISBN = self.request.get('ISBN')
	callback = self.request.get('callback')
        book = Books.get_by_key_name(ISBN)
        self.response.write(callback + '({ "summary": "' + book.Summary + '"})')

class getBook(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/javascript'
        ISBN = self.request.get('ISBN')
        book = Books.get_by_key_name(ISBN)
        path = book.FilePath

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

