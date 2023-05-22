import mysql.connector
from flask import Flask, render_template, request, session

MainPage = Flask(__name__)

app = Flask(__name__)

app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    title = 'Flask Website'
    app_name = 'My Flask App'
    return render_template('Login.html', title=title, app_name=app_name)

@app.route('/deleteUser', methods=['POST'])
def delUser():

    connection = mysql.connector.connect(
        host='localhost',
        user='test_user',
        password='Test123456!',
        database='recepiefinder'
    )
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Users WHERE Username = %s;", (session.get('_USERNAME'),))
    connection.commit()
    title = 'Flask Website'
    app_name = 'My Flask App'

    return render_template('Login.html', title='Account deleted', app_name='My Flask App')

@app.route('/findRecepies', methods=['POST'])
def getDishes():
    connection = mysql.connector.connect(
        host='localhost',
        user='test_user',
        password='Test123456!',
        database='recepiefinder'
    )
    cursor = connection.cursor()
    cursor.execute("CALL GetAvailableDishNames(%s);", (session.get('_USERNAME'),))
    recepies = cursor.fetchall()

    return render_template('index.html', recepies=recepies)



@app.route('/createUser', methods=['POST'])
def addUser():
    input1 = request.form['C_userName']
    input2 = request.form['C_password']
    connection = mysql.connector.connect(
        host='localhost',
        user='test_user',
        password='Test123456!',
        database='recepiefinder'
    )
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Users WHERE Users.UserName = %s;", (input1,))
    results = cursor.fetchall()
    if results:
        return render_template('Login.html', title='User already exists!', app_name='My Flask App')

    cursor.execute("INSERT INTO Users (username, password) VALUES (%s, %s)", (input1, input2))
    connection.commit()
    title = 'Flask Website'
    app_name = 'My Flask App'

    return render_template('Login.html', title='Account Created', app_name='My Flask App')


@app.route('/Login', methods=['POST'])
def new_page():
    input1 = request.form['userName']
    input2 = request.form['password']
    # Do something with input1 and input2

    connection = mysql.connector.connect(
        host='localhost',
        user='test_user',
        password='Test123456!',
        database='recepiefinder'
    )
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Users WHERE Users.UserName = %s AND Users.Password = %s;", (input1, input2))
    results = cursor.fetchall()

    title = 'Flask Website'
    app_name = 'My Flask App'

    if results:

        session['_USERNAME'] = input1
        return render_template('index.html', title='Flask Website', app_name='My Flask App')

    return render_template('Login.html', title='Login Failed', app_name='My Flask App')


@app.route('/addIngredient', methods=['POST'])
def button_clicked():
    ing = request.form['ingredient']
    exp = request.form['expiration']
    quant = int(request.form['quantity'])
    unit = request.form['unit']
    
    # Connect to the MySQL database
    connection = mysql.connector.connect(
        host='localhost',
        user='test_user',
        password='Test123456!',
        database='recepiefinder'
    )

    cursor = connection.cursor()
    print("ING:", ing)
    print("EXP:", exp)
    print("QUANT:", quant)
    print("USERNAME", session.get('_USERNAME'))
    
    # Insert the ingredient into the Produce table
    query = "INSERT INTO Produce (Ingredient, ExpirationDate, Quantity, RecipeQuantity, UserName) VALUES (%s, %s, %s, %s, %s)"
    values = (ing, exp, quant, unit, session.get('_USERNAME'))
    cursor.execute(query, values)
    connection.commit()

    # Fetch all ingredients for the current user from the Produce table
    cursor.execute("SELECT Ingredient FROM Produce WHERE UserName = %s", (session.get('_USERNAME'),))
    results = cursor.fetchall()
    _INGREDIENTS = [row[0] for row in results]

    # Close the database connection
    cursor.close()
    connection.close()

    return render_template('index.html', title='Added Ingredient', app_name='My Flask App', _INGREDIENTS=_INGREDIENTS)

if __name__ == '__main__':
    app.run(debug=True)
