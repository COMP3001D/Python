import webapp2

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
    Name = db.StringProperty()
    ID = db.StringProperty()
    Email = db.EmailProperty()
    PasswordHash = db.StringProperty()

class Search(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'application/javascript'
		self.response.write('{"Message":"Hello"}');

app = webapp2.WSGIApplication([('/Search', Search)],
				debug = True)

