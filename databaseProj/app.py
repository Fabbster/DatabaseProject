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
        database='recepie_finder'
    )
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Users WHERE Username = %s;", (session.get('_USERNAME'),))
    connection.commit()
    title = 'Flask Website'
    app_name = 'My Flask App'

    return render_template('Login.html', title='Account deleted', app_name='My Flask App')


@app.route('/createUser', methods=['POST'])
def addUser():
    input1 = request.form['C_userName']
    input2 = request.form['C_password']
    connection = mysql.connector.connect(
        host='localhost',
        user='test_user',
        password='Test123456!',
        database='recepie_finder'
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
        database='recepie_finder'
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
    #This function will be implemented once Login is done. Since username needs to also be added to the table entry.
    ing = request.form['ingredient']
    exp = request.form['expiration']
    quant = request.form['quantity']
    unit = request.form['unit']
    connection = mysql.connector.connect(
        host='localhost',
        user='test_user',
        password='Test123456!',
        database='recepie_finder'
    )

    cursor = connection.cursor()
    print("ING:", ing)
    print("EXP:", exp)
    print("QUANT:", quant)
    print("USERNAME", session.get('_USERNAME'))
    cursor.execute("INSERT INTO Produce (ingredient, expirationdate, quantity,RecipeQuantity, username) VALUES ('%s "','"%s"','"%i"','"%s"','"%s );", (ing, exp, quant,unit, session.get('_USERNAME')))   
    connection.commit()
    cursor.execute("SELECT * FROM Produce WHERE Produce.username = %s", (session.get('_USERNAME'),))
    results = cursor.fetchall()

    _INGREDIENTS = [row[0] for row in results]

    return render_template('index.html', title='added Ingredient', app_name='My Flask App')

if __name__ == '__main__':
    app.run(debug=True)
