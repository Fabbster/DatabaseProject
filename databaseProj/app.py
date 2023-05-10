from flask import Flask
import mysql.connector
from flask import Flask, render_template

MainPage = Flask(__name__)

# @MainPage.route('/')
# def index():
#     title = 'Flask Website'
#     app_name = 'My Flask App'
#     return render_template('index.html', title=title, app_name=app_name)

app = Flask(__name__)

@app.route('/')
def index():
    connection = mysql.connector.connect(
        host='localhost',
        user='test_user',
        password='Test123456!',
        database='recepie_finder'
    )
    
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM users')
    results = cursor.fetchall()

    return str(results)

if __name__ == '__main__':
    app.run(debug=True)
