from Test3 import db
class Admin(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(30))
    password = db.Column(db.String(30))

    def __int__(self,email="",password=""):
        self.email = email
        self.password = password

class Contact(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name= db.Column(db.String(30))
    contactno = db.Column(db.String(11))
    email = db.Column(db.String(30))
    query = db.Column(db.String(500))

    def __init__(self,name="",contactno="",email="",query=""):
        self.name = name
        self.contactno = contactno
        self.email = email
        self.query = query


blog = db.Table('blog',
       db.Column('cat_id',db.Integer,db.ForeignKey('category.id')),
       db.Column('post_id',db.Integer,db.ForeignKey('post.id'))
                )


class Category(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30),unique=True)
    relation = db.relationship('Post',secondary=blog,backref=db.backref('blogger',lazy='dynamic'))

    def __init__(self,name=""):
        self.name = name

class Suscribe(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(30))

    def __init__(self, email=""):
        self.email = email


class Post(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(100),unique=True)
    author = db.Column(db.String(50))
    description = db.Column(db.Text)
    date = db.Column(db.String(20))


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    comment = db.Column(db.Text)

    def __init__(self,name="",comment=""):
        self.name=name
        self.comment=comment
