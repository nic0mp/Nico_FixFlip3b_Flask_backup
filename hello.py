from flask import Flask, render_template, flash, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# create a Flask instance
app = Flask(__name__)
#  add db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# secret key
app.config['SECRET_KEY'] = 'my secret key nobody needs to know'
# initialize the db
db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    # Create a string
    def __repr__(self):
        return '<Name %r>' % self.name

@app.route('/update/<int:id>')
def delete(id):
    user_to_delete = Users.query.get_or_404(id) 
    name = None
    form=UserForm()

    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash('User Deleted')
        our_users = Users.query.order_by(Users.date_added)
        return render_template('add_user.html',form=form,name=name,our_users=our_users)

    except:
        flash('Whoops, try again')
        return render_template('add_user.html',form=form,name=name,our_users=our_users)

# Create form class
class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit =  SubmitField('Submit')

# Update DB record
@app.route('/update/<int:id>', methods=['GET','POST']) 
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == 'POST':
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        try:
            db.session.commit()
            flash('User has been Updated')
            return render_template('update.html',
                    form=form,
                    name_to_update=name_to_update)
                    
        except:
            flash('Error, you messed up')
            return render_template('update.html',
                    form=form,name_to_update=name_to_update) 
       
    else:
        return render_template('update.html',
                    form=form,name_to_update=name_to_update,id=id) 
                    
# Create form class
class NamerForm(FlaskForm):
    name = StringField("What's your name?", validators=[DataRequired()])
    submit =  SubmitField('Submit')


# safe,capitalize,lower,upper,title,trim,striptags

@app.route('/user/add',methods=['GET','POST'])
def add_user():
    name = None
    form=UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash('User added')
    our_users = Users.query.order_by(Users.date_added)
    return render_template('add_user.html',form=form,name=name,our_users=our_users)

# create a route decorator
@app.route('/')
def index():
    first_name= 'Chunks'
    # stuff = 'This is <strong>Bold</strong> Text' ** wotks with safe and striptag
    stuff = 'This is Bold Text'

    return render_template('index.html', 
    first_name=first_name,
    stuff=stuff,
    )

# Create Name page
@app.route('/name', methods=['GET','POST'])
def name():
    name = None
    form = NamerForm()
    #Validate Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash('Form submitted successfully')
    return render_template('name.html',
    name = name,
    form = form
    )

@app.route('/', methods=['POST','GET'])
def calculateCost():
    totalCost = ''
    ltcAmount = ''
    loanDownPayment=''
    gProfit=''
    roi=''
    RefiAmt = ''
    CashFlow=''
    AnnualInc=''
    cROI=''
    if request.method== 'POST' and 'arv' in request.form and 'hprice' in request.form and 'rbudget' in request.form and 'totalRentInc' in request.form and 'totalExpenses' in request.form:
        AfterRepairVal=int(request.form.get('arv'))
        HPrice=int(request.form.get('hprice'))
        RBudget=int(request.form.get('rbudget'))
        RentalIncome=int(request.form.get('totalRentInc'))
        RentalExpenses=int(request.form.get('totalExpenses'))
        totalCost=int(HPrice + RBudget)
        ltcAmount=int(.7*totalCost)
        loanDownPayment=int(totalCost*.3)
        gProfit=int(AfterRepairVal-totalCost)
        roi = round(float((gProfit/totalCost)*100),2)
        RefiAmt = int(AfterRepairVal*.7)
        CashFlow=int(RentalIncome-RentalExpenses)
        AnnualInc=int(CashFlow*12)
        cROI=round(float((AnnualInc/totalCost)*100),2)
    return render_template('index.html',
                AfterRepairVal=AfterRepairVal,
                totalCost=totalCost, 
                ltcAmount=ltcAmount,
                loanDownPayment=loanDownPayment,
                gProfit=gProfit,
                roi=roi,
                RefiAmt=RefiAmt,
                CashFlow=CashFlow,
                AnnualInc=AnnualInc,
                cROI=cROI
                )