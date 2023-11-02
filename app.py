from flask import Flask,render_template,request,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
import stripe
from flask_migrate import Migrate

stripe.api_key = 'sk_test_51O7wedSEvumAB3djPFdHAiWqvHU818MatNmk8PDmzD39YGyze3iogJBfxFJ0y2P7q9QLcyohljc5F8gGym9XcegR00q8ZVTu2O'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finalfood.db'
db = SQLAlchemy(app)
migrate=Migrate(app,db)
app.app_context().push()



class Item(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    quantity=db.Column(db.Integer(),nullable=False)
    food_name=db.Column(db.String(length=30),nullable=False)
    contact=db.Column(db.Integer(),nullable=False)
    category=db.Column(db.String(length=10),nullable=False)
    address=db.Column(db.String(length=100),nullable=False)

    def __repr__(self):
        return f'Item {self.food_name}'
    

@app.route('/pay', methods=['Get','POST'])
def pay():
    session = stripe.checkout.Session.create(
        line_items=[{
        'price_data': {
            'currency': 'usd',
            'product_data': {
            'name': 'Donate for HUNGER',
            },
            'unit_amount': 1000,
        },
        'quantity': 1,
        }],
        mode='payment',
        success_url='http://127.0.0.1:5000/sucess',
        cancel_url='http://localhost:4242/cancel',
    )
    return redirect(session.url, code=303)

@app.route('/sucess')
def sucess():
    return render_template('sucess.html')

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/delete/<int:id>')
def delete(id):
    user=Item.query.get_or_404(id)
    try:
        db.session.delete(user)
        db.session.commit()
        flash("food deleted",'info')
        return redirect(url_for('about'))
        
    except:
        flash('there was an error',category="error")


@app.route('/about',methods=['get','post'])
def about():
    items=Item.query.all()    
    return render_template("about.html",items=items)

@app.route('/contact')
def contact():
    return render_template("contact.html")

app.secret_key="gsytevagsvqw"

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        your_name=request.form.get('yname')
        email=request.form.get('email')
        contact=request.form.get('contact')
        address=request.form.get('address')
        food_name=request.form.get('food_name')
        quantity=request.form.get('quantity')
        category=request.form.get('category')

         
    
        if not your_name :
            flash("user should not be empty",category='error')
            return redirect(url_for('register'))

        else:
            flash("food added succesfully",'info')
            new_food=Item(food_name=food_name,contact=contact,address=address,category=category,quantity=quantity)
            db.session.add(new_food)
            db.session.commit()
            return redirect(url_for('register'))
    else:    
       return render_template("register.html")


if __name__ == '__main__':
    app.run(debug=True)
