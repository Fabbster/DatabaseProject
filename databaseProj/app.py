import mysql.connector
from flask import Flask, render_template, request, session, g

MainPage = Flask(__name__)

app = Flask(__name__)

app.secret_key = "your_secret_key"

DATABASE_CONFIG = {
    "host": "localhost",
    "user": "test_user",
    "password": "Test123456!",
    "database": "recepie_finder",
}


def get_db_connection():
    if "db" not in g:
        g.db = mysql.connector.connect(**DATABASE_CONFIG)
    return g.db


@app.teardown_appcontext
def close_db_connection(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


@app.route("/")
def index():
    title = "Flask Website"
    app_name = "My Flask App"
    return render_template("Login.html", title=title, app_name=app_name)


@app.route("/deleteUser", methods=["POST"])
def delUser():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "DELETE FROM Users WHERE Username = %s;", (session.get("_USERNAME"),)
    )
    connection.commit()
    title = "Flask Website"
    app_name = "My Flask App"

    return render_template(
        "Login.html", title="Account deleted", app_name="My Flask App"
    )


@app.route("/findRecepies", methods=["POST"])
def getDishes():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("CALL GetAvailableDishNames(%s);", (session.get("_USERNAME"),))
    recepies = cursor.fetchall()

    return render_template("index.html", recepies=recepies)


@app.route("/getIngredientsForRecepie", methods=["POST"])
def getIngredients():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT r.DishName, r.Ingredient, CONCAT(r.Quantity, ' ', r.RecipeQuantity) as RequiredQuantity, CONCAT(p.Quantity, ' ', p.RecipeQuantity) as AvailableQuantity FROM  Recipes r LEFT JOIN  Produce p ON r.Ingredient = p.Ingredient AND p.UserName = %s WHERE r.DishName = %s;",
        (
            session.get("_USERNAME"),
            request.form["ingredients"],
        ),
    )
    ingredients = cursor.fetchall()

    return render_template("index.html", ingredients=ingredients)


@app.route("/findeExpirationDate", methods=["POST"])
def getAllExpirationDate():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT GetExpirationDate(%s, %s) as ExpirationDate ;",
        (session.get("_USERNAME"), request.form["checkIngredient"]),
    )
    expirationDate = cursor.fetchall()

    return render_template("index.html", expirationDate=expirationDate)


@app.route("/removeExpired", methods=["POST"])
def removeExpired():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("CALL DeleteExpiredIngredients(%s);", (session.get("_USERNAME"),))
    connection.commit()

    return render_template("index.html")


@app.route("/findAllAvailableProduce", methods=["POST"])
def getAllProduce():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT Ingredient, SUM(Quantity) as TotalQuantity FROM Produce GROUP BY Ingredient;"
    )
    produce = cursor.fetchall()

    return render_template("index.html", produce=produce)


@app.route("/findUsersAndProduce", methods=["POST"])
def getUsersAndProduce():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT u.UserName, p.Ingredient, p.ExpirationDate, p.Quantity FROM Users u JOIN Produce p ON u.UserName = p.UserName;"
    )
    UsersAndProduce = cursor.fetchall()

    return render_template("Login.html", UsersAndProduce=UsersAndProduce)


@app.route("/createUser", methods=["POST"])
def addUser():
    input1 = request.form["C_userName"]
    input2 = request.form["C_password"]
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Users WHERE Users.UserName = %s;", (input1,))
    results = cursor.fetchall()
    if results:
        return render_template(
            "Login.html", title="User already exists!", app_name="My Flask App"
        )

    cursor.execute(
        "INSERT INTO Users (username, password) VALUES (%s, %s)", (input1, input2)
    )
    connection.commit()
    title = "Flask Website"
    app_name = "My Flask App"

    return render_template(
        "Login.html", title="Account Created", app_name="My Flask App"
    )


@app.route("/Login", methods=["POST"])
def new_page():
    input1 = request.form["userName"]
    input2 = request.form["password"]
    # Do something with input1 and input2
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM Users WHERE Users.UserName = %s AND Users.Password = %s;",
        (input1, input2),
    )
    results = cursor.fetchall()

    if results:
        session["_USERNAME"] = input1
        return render_template(
            "index.html", title="Flask Website", app_name="My Flask App"
        )

    return render_template("Login.html", title="Login Failed", app_name="My Flask App")


@app.route("/addIngredient", methods=["POST"])
def button_clicked():
    ing = request.form["ingredient"]
    exp = request.form["expiration"]
    quant = int(request.form["quantity"])
    unit = request.form["unit"]

    connection = get_db_connection()
    cursor = connection.cursor()
    print("ING:", ing)
    print("EXP:", exp)
    print("QUANT:", quant)
    print("USERNAME", session.get("_USERNAME"))

    query = "INSERT INTO Produce (Ingredient, ExpirationDate, Quantity, RecipeQuantity, UserName) VALUES (%s, %s, %s, %s, %s)"
    values = (ing, exp, quant, unit, session.get("_USERNAME"))
    cursor.execute(query, values)
    connection.commit()

    cursor.close()
    connection.close()

    return render_template(
        "index.html",
        title="Added Ingredient",
        app_name="My Flask App",
    )


@app.route("/getProduce", methods=["POST"])
def getProduce():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT Ingredient FROM Produce WHERE UserName = %s",
        (session.get("_USERNAME"),),
    )
    results = cursor.fetchall()
    _INGREDIENTS = [row[0] for row in results]

    return render_template(
        "index.html",
        _INGREDIENTS=_INGREDIENTS,
    )


if __name__ == "__main__":
    app.run(debug=True)
