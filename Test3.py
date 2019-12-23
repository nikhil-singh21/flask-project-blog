from flask import *
from flask_sqlalchemy import *
import pymysql
from flask_mail import *
import math


app = Flask(__name__)
app.secret_key = "nikhil"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/blog'
db = SQLAlchemy(app)


@app.route("/",methods=['POST','GET'])
def index():
    if request.method == 'GET':
        cat_id = request.args.get('cat_id')
        if cat_id:
            cat_id = int(cat_id)
            cat = Category.query.filter_by(id=cat_id).first()
            return render_template("blog.html", post=cat.relation, category=Category.query.all())
        else:
            cmnt = Comment(request.args.get('name'), request.args.get('comment'))
            db.session.add(cmnt)
            db.session.commit()
            post = db.session.query(Post).all()
            post_count = 3
            posts = Post.query.all()
            last = math.ceil(len(posts) / post_count)
            page = request.args.get('page')
            if not str(page).isnumeric():
                page = 1
            page = int(page)
            posts = posts[(page - 1) * post_count: (page - 1) * post_count + post_count]
            if page == 1:
                prev = "#"
                next = "/Blog?page=" + str(page + 1)
            elif page == last:
                prev = "/Blog?page=" + str(page - 1)
                next = "#"
            else:
                prev = "/Blog?page=" + str(page - 1)
                next = "/Blog?page=" + str(page + 1)
            return render_template('blog.html', post=post, posts=posts, prev=prev, next=next,
                                   category=Category.query.all(), comment=Comment.query.all())
    elif request.method == 'POST':
        try:
            post = db.session.query(Post).limit(3).all()
            return render_template('blog.html', post=post, category=Category())
        except Exception as e:
            print('error:', e)
            db.session.rollback()
            return render_template('blog.html', msg='<script>alert("error")</script>')


@app.route("/Home")
def Home():
    return render_template('home.html')

@app.route("/Blog",methods=['GET','POST'])
def Blog():
    if request.method=='GET':
        cat_id = request.args.get('cat_id')
        if cat_id:
            cat_id = int(cat_id)
            cat = Category.query.filter_by(id=cat_id).first()
            return render_template("blog.html", post=cat.relation, category=Category.query.all())
        else:
            cmnt = Comment(request.args.get('name'), request.args.get('comment'))
            db.session.add(cmnt)
            db.session.commit()
            post = db.session.query(Post).all()
            post_count = 3
            posts = Post.query.all()
            last = math.ceil(len(posts) / post_count)
            page = request.args.get('page')
            if not str(page).isnumeric():
                page = 1
            page = int(page)
            posts = posts[(page - 1) * post_count: (page - 1) * post_count + post_count]
            if page == 1:
                prev = "#"
                next = "/Blog?page=" + str(page + 1)
            elif page == last:
                prev = "/Blog?page=" + str(page - 1)
                next = "#"
            else:
                prev = "/Blog?page=" + str(page - 1)
                next = "/Blog?page=" + str(page + 1)
            return render_template('blog.html',post=post,posts=posts,prev=prev,next=next, category=Category.query.all(),comment=Comment.query.all())
    elif request.method=='POST':
        try:
            post=db.session.query(Post).limit(3).all()
            return render_template('blog.html',post=post,category=Category())
        except Exception as e:
            print('error:', e)
            db.session.rollback()
            return render_template('blog.html', msg='<script>alert("error")</script>')

@app.route("/search",methods=['GET','POST'])
def search():
    search = request.form.get('search')
    print(search)
    posts =  db.session.query(Post).filter(Post.title.like('%{}%'.format(search))).all()
    return render_template('blog.html',posts=posts,category=Category.query.all())






from models import *



app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'nikcompany8@gmail.com'
app.config['MAIL_PASSWORD'] = '**********'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
@app.route("/Contactus", methods=['POST', 'GET'])
def Contactus():
    if request.method == 'GET':
        return render_template('contact.html')
    elif request.method == 'POST':

        contact = Contact(request.form['name'], request.form['contactno'], request.form['email'], request.form['query'])
        db.session.add(contact)
        db.session.commit()
        msg = Message(request.form['email'], sender='nikcompany8@gmail.com',
                      recipients=['nikhil8271768371@gmail.com'])
        msg.body = request.form['query']
        mail.send(msg)
        return render_template("contact.html",ms='<script>alert("your query submitted compeletly")</script>')
    else:
        return render_template("contact.html",ms='<script>alert("error try again")</script>')




from models import *


@app.route("/Login", methods=['GET', 'POST'])
def Login():
        try:
            if request.method == 'POST':
                session['email']=request.form['email_id']
                session['password'] = request.form['pass_word']
                name = Admin.query.filter_by(email=session['email'], password=session['password']).first()
                if name:
                    return render_template('Admintemplate.html', msg='welcome')
                else:
                    return render_template('login.html', msg='try again')
            else:
                return render_template('login.html')
        except Exception as e:
            print('error:',e)
@app.route('/logout',methods=['POST','GET'])
def logout():
    session.pop('email')
    session.pop('password')
    return render_template('login.html')

@app.route('/category',methods=['GET','POST'])
def category():
    if 'email' in session:
        if request.method == 'GET':
            category = db.session.query(Category.name).all()
            return render_template('category.html',cat=category)
        elif request.method =='POST':
           try:
               category = db.session.query(Category.name).all()
               return render_template('category.html',cat=category)
           except:
               db.session.rollback()
               return render_template('category.html', msg='<scripts>window.alert("error")</scripts>')
    else:
        return render_template('login.html')
@app.route('/add-cat',methods=['GET','POST'])
def addcat():
    if 'email' in session:
        if request.method == 'GET':
             return render_template('addcategory.html')
        elif request.method =='POST':
           try:
                category = Category(request.form['category'])
                db.session.add(category)
                db.session.commit()
                return render_template('addcategory.html', msg='<script>window.alert("category created")</script>',cat=category)
           except:
               db.session.rollback()
               return render_template('addcategory.html', msg='<script>window.alert("error")</script>')
    else:
        return render_template('login.html')

@app.route('/post',methods=['GET','POST'])
def post():
    if 'email' in session:
        if request.method=='GET':
            post = db.session.query(Post.title).all()
            return render_template('post.html',p=post)
        elif request.method =='POST':
           try:
               post = db.session.query(Post.title).all()
               return render_template('post.html', p=post)
           except Exception as e:
               db.session.rollback()
               return render_template('post.html', msg='<script>alert("error")</script>')
    else:
        return render_template('login.html')


@app.route('/add-post',methods=['GET','POST'])
def addpost():
    if 'email' in session:
        if request.method == 'GET':
            category = db.session.query(Category.name).all()
            return render_template('addpost.html', cat=category)
        elif request.method == 'POST':
            try:
                category = Category.query.filter_by(name=request.form['category']).first()
                desc =bytes(request.form['desc'],'utf-8')
                print ('description : .......... : ',desc)

                post = Post(title=request.form['title'], author=request.form['author'], description=desc,
                            date=request.form['date'])
                db.session.add(post)
                post.blogger.append(category)
                db.session.commit()

                category = db.session.query(Category.name).all()
                suscriber = db.session.query(Suscribe).all()
                mail = Mail(app)
                with mail.connect() as con:
                    for user in suscriber:
                        message = "hello %s NS blog has posted something new you may intrested" % user.email
                        msgs = Message(recipients=[user.email], body=message, subject='New Post By Nikhil',
                                       sender='nikcompany8@gmail.com')
                        con.send(msgs)
                return render_template('addpost.html', msg='<script>window.alert("post created")</script>', cat=category)
            except Exception as e:
                print('error',e)
                db.session.rollback()
                return render_template('post.html', msg='<script>alert("error")</script>')

    else:
        return render_template('login.html')
@app.route('/readmore',methods=['POST','GET'])
def readmore():
   if request.method == 'GET':
        text=request.args.get('text')
        post=Post.query.filter_by(id=text).first()
        return  render_template('readmore.html',post=post)
   else:
       text = request.args.get('text')
       post = Post.query.filter_by(id=text).first()
       return render_template('readmore.html')


@app.route('/suscribe',methods=['POST','GET'])
def suscribe():
    if request.method=='GET':
        return render_template('contact.html')
    if request.method=='POST':
        try:
            suscribe=Suscribe(request.form['email'])
            db.session.add(suscribe)
            db.session.commit()
            msg = Message(subject='subscription email', sender='nikcompany8@gmail.com',
                          recipients=[request.form['email']])
            msg.body = 'you have suscribed to Nikhil Singh blog'
            mail.send(msg)
            return render_template('contact.html',msg='<script>alert("successfully suscribed")</script>')
        except Exception as e:
            db.session.rollback()
            return ('error:',e)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, port=80)
