import mysql.connector
from flask import Flask, render_template,url_for,redirect,request,session,flash
import bcrypt

database = mysql.connector.connect(
    host='localhost',
    user='********',
    password='********',
    database='shopping_web'
)

app = Flask(__name__)
app.secret_key = 'shopping_website_lavitra'

cursor = database.cursor()


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/product', methods=['GET', 'POST'])
def product():
    query = "SELECT name, price, description, id FROM products"
    cursor.execute(query)
    data = cursor.fetchall()
    product_data = []
    for i in range(len(data)-1,-1,-1):
        product_data.append(data[i])
        print(product_data)


        # Check if the product is already in the cart for this user
    if request.method == 'POST':
        if 'user_id' in session:
            user_id = session['user_id']
            product_id = request.form.get('product_id')
            cursor.execute("SELECT * FROM cart WHERE user_id = %s AND product_id = %s", (user_id, product_id))
            existing_cart_item = cursor.fetchone()

            if existing_cart_item:
                new_quantity = existing_cart_item[3] + 1
                update_query = "UPDATE cart SET quantity = %s WHERE user_id = %s AND product_id = %s"
                cursor.execute(update_query, (new_quantity, user_id, product_id))
                database.commit()
            else:
                cursor.execute("INSERT INTO cart (user_id, product_id, quantity) VALUES (%s, %s, 1)", (user_id, product_id))
                database.commit()
                return "Product added to cart"
        else:
            flash('You are not loged in','login_error')
            return redirect(url_for('product'))
    

    return render_template('product.html', product_data=product_data)

@app.route('/cart')
def cart():
    if 'user_id' in session:
        user_id = session['user_id']
        query = "SELECT product_id , quantity FROM cart WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        cart_items = cursor.fetchall()
        products = []
        for i in cart_items:
            cursor.execute("SELECT name, price, description FROM products WHERE id = %s", (i[0],))
            items = cursor.fetchall()
            products.append(items[0] + (i[1],))
            print(products)

 
        return render_template('cart.html', products = products)

    else:
        return "User not loged in"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        action = request.form['action']
        if action == 'login':
            username = request.form['username']
            password = request.form['password']
            cursor.execute("SELECT password,user_id FROM users WHERE username = %s", (username,))
            result = cursor.fetchone()

            if result is not None:
                hashed_password = result[0]
                if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                    user_id = result[1]
                    session['user_id'] = user_id
                    session['logged_in'] = True
                    flash('Login Sucessful', 'success')
                    return redirect(url_for('home'))
                
                else:
                    flash('Incorrect Password','login_error')

            else:
                flash('User not Found','login_error')
            
        elif action == 'signup':
            username = request.form['email']
            password = request.form['password']
            password_repeat = request.form['password-repeat']
            if password == password_repeat:
                cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
                result = cursor.fetchone()
                if result is None:
                    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
                    database.commit()
                    session['logged_in'] = True
                    flash('Account Created', 'success')
                    return redirect(url_for('home'))
                    
                else:
                    flash('User already exist','signup_error')
            else:
                flash('Password Not Match','signup_error')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session['logged_in'] = False
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
