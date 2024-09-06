from flask import Flask, request, redirect, session, render_template, Response, url_for, flash
from flask_login import current_user, LoginManager, UserMixin, login_required, login_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_cors import CORS
from configparser import ConfigParser
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import time
import sqlite3
import hashlib
import brytoria_db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)
app.secret_key = 'CHANGE ME' #CHANGE ME !! Don't share the key to anybody else.
app.config["SESSION_PERMANENT"] = True
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=5)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = u"Please log in to access this page"
login_manager.login_message_category = "warning"
Session(app)
CORS(app)
database = "database.db"


####### user_loader ########
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


## Login form sqlite3 db.
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(255),nullable=False)
    admin = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, nullable=False, default=True)


    def __init__(self, id, username, password, admin, active):
        self.id = id
        self.username = username
        self.password = password
        self.admin = admin
        self.active = active
  
    
    def is_active(self):
        self.active = True
        return True
    

    def is_authenticated(self):
        self.authenticated = True
        return True


    def is_anonymous(self):
        return False


    def get_id(self):
        user_id = str(self.id)
        return user_id


with app.app_context():
    db.create_all()    


######### Forms ##########
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()], render_kw={'placeholder':'Login'})
    password = PasswordField("Password", validators=[DataRequired()], render_kw={'placeholder':'Password'})
    submit = SubmitField("Submit")


class AddOrder(FlaskForm):
    service = StringField("Service", validators=[DataRequired()], render_kw={'placeholder':'service'})
    comment = TextAreaField("Comment", validators=[DataRequired()], default="Brak komentarza")
    username =  StringField("Username", validators=[DataRequired()])
    price =  IntegerField("Price", validators=[DataRequired()])
    phone_number =  IntegerField("Phone number", validators=[DataRequired()], render_kw={'placeholder':'+48 999 111 888'})
    submit = SubmitField("Submit")


class SearchUser(FlaskForm):
    username =  StringField("Username", validators=[DataRequired()])
    submit = SubmitField("Submit")


########### Errors handler ###########
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


###################### Pages ######################


########### Logout ###########
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


########### Admin panel ############
@app.route('/admin_panel', methods=['GET','POST'])
@login_required
def admin_panel_t():
    flash("Welcome !")
    return render_template('admin_panel.html')


############# ADD ORDER ############
@app.route('/order', methods=['GET'])
@login_required
def order_page():
    form = AddOrder()
    return render_template('order.html', form=form)


@app.route('/order', methods=['POST'])
@login_required
def order():
    form = AddOrder()
    if form.validate_on_submit():
        service = form.service.data
        comment = form.comment.data
        u_name = form.username.data.replace(" ","")
        order_date = datetime.now()
        price = form.price.data
        u_number = form.phone_number.data
        avatar = "Jest"
        table_name = brytoria_db.main()
        con = sqlite3.connect(database)
        cur = con.cursor()
        cur = cur.execute("INSERT INTO " + table_name + "(service, comment, name, date, price, number, avatar) VALUES(?, ?, ?, ?, ?, ?, ?)", (service, comment, u_name, order_date, price, u_number, avatar))
        con.commit()
        flash("Order Added Successfully!")
    return render_template("order.html", form=form) + '''Done'''


############# SHOW ORDER ############
@app.route('/show_orders', methods=['GET'])
@login_required
def show_order():
    table_name = brytoria_db.main()
    table_name = str(table_name)
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur = cur.execute("SELECT * FROM "+ table_name + "")
    rows = cur.fetchall()
    
    cur = cur.execute("SELECT price FROM "+ table_name + "")
    total_prices = cur.fetchall()
    total_amount = 0
    for total_price in total_prices:
        total_amount += total_price[0]     
   
    return render_template('show_data.html', rows=rows, total_amount=total_amount)


############# SEARCH USER ORDERS ############
@app.route('/search_by_name', methods=['GET'])
@login_required
def search_by_name_g():
    form = SearchUser()
    return render_template('search_name.html', form=form)


@app.route('/search_by_name', methods=['POST'])
@login_required
def search_query():
    form = SearchUser()
    if form.validate_on_submit():
        nickname = form.username.data
        
        search_list = []
        user_results = []
        
        con = sqlite3.connect(database)
        cur = con.cursor()
        cur = cur.execute("SELECT name FROM sqlite_master WHERE type ='table'")
        table_names = cur.fetchall()
        for name_table in table_names:
            name_table = str(name_table)
            name_table1 = name_table.replace("'", "").replace("(", "").replace(",", "").replace(")", "")
            if name_table1 == "sqlite_sequence":
                pass
            else:
                search_list.append(name_table1)

        for filtered_table_name in search_list:
           
            cur = cur.execute("SELECT * FROM " + filtered_table_name + " WHERE name ='" + nickname + "'" )
            informations = cur.fetchall()
            for information in informations:
                #information_filtered = information.replace("'", "").replace("(", "").replace(",", "").replace(")", "")
                user_results.append(information)
                    
        if user_results == []:
            flash("No orders found")
    return render_template('search_name.html', user_results=user_results, nickname=nickname, form=form)


############# index ############
@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('login_page'))


########### Login ###########
@app.route('/login', methods=['GET'])
def login_page():
    form = LoginForm()
    return render_template('index.html', form=form)


@app.route('/login', methods=['POST'])
def login(): 
    agent = request.headers.get('User-Agent')
    print(agent)
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            pass_check_werk = check_password_hash(user.password, form.password.data)
            if pass_check_werk == True: 
                login_user(user)
                flash("Logged in successfully.")
                return redirect(url_for('admin_panel_t'))
            else:
                flash("Login failed")
        else:
            flash("Login failed")
    return redirect(url_for('login_page')) 


if __name__ == "__main__":
    app.run('192.168.0.137', '9999')
    app.run(debug=True)
