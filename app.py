from flask import Flask, render_template, session, request, send_file, Response, redirect, url_for, flash
from flask_session import Session
from flask_images import resized_img_src
from datetime import datetime

app = Flask(__name__)

app.secret_key = "hello"

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

users = []
owner = {
    "name": "John Doe",
    "phone_num": "(521) 824-2004",
    "email": "johndoe@gmail.com",
    "password": "hello123"
}
users.append(owner)

time = datetime.now()
timeStr = ""

if time.hour == 0:
    timeStr = time.strftime("%d/%m/%Y 12:%M:%S AM")
elif time.hour > 0 and time.hour < 12:
    timeStr = time.strftime("%d/%m/%Y %H:%M:%S AM")
elif time.hour == 12:
    timeStr = time.strftime("%d/%m/%Y 12:%M:%S PM")
elif time.hour >= 12 and time.hour < 24:
    hr = time.hour - 12
    timeStr = time.strftime("%d/%m/%Y " + str(hr) + ":%M PM")

requests = []
req = {
    "user": owner,
    "title": "Toliet Paper",
    "desc": "Hello, I am requesting a pack of toilet paper.",
    "date": timeStr
}
requests.append(req)
req2 = {
    "user": owner,
    "title": "Lysol Spray",
    "desc": "Hello, I am requesting 13 lysol spray bottles.",
    "date": timeStr
}
requests.append(req2)

isLoggedIn = False
currentUser = None

@app.route("/", methods=["POST", "GET"])
def index():
    global isLoggedIn
    global users
    global currentUser
    global requests

    if request.method == "POST":
        req = {
            "user": currentUser,
            "title": request.form["item_name"],
            "desc": request.form["item_desc"],
            "date": getCurrentTime()
        }
        requests.append(req)

        return render_template("index.html")
    else:
        return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    global isLoggedIn
    global users
    global currentUser
    global requests

    if request.method == "POST":
        # Get login form data

        newUser = {
            "email": request.form["em"],
            "password": request.form["pw"]
        }

        accountMatch = False

        for user in users:
            if newUser.get("email") == user.get("email") and newUser.get("password") == user.get("password"):
                currentUser = user
                accountMatch = True

        if accountMatch:
            isLoggedIn = True
            return redirect(url_for('index'))
        else:
            flash("Incorrect email or password!")
            print("Incorrect email or password!")

        return render_template("login.html")
    elif isLoggedIn:
        return redirect(url_for('index'))
    elif request.method == "GET" or not isLoggedIn:
        return render_template("login.html")

@app.route("/register", methods=["POST", "GET"])
def register():
    global isLoggedIn
    global users
    global currentUser
    global requests

    if request.method == "POST":
        # Get register form data
        
        newUser = {
            "name": request.form["nm"],
            "phone_num": request.form["ph"],
            "email": request.form["em"],
            "password": request.form["pw"]
        }

        errorList = []

        if len(newUser["name"]) == 0:
            errorList.append("name")
            #flash("Please enter your name!")
            #return render_template("register.html")
        
        if len(str(newUser["phone_num"])) == 0:
            errorList.append(("phone number"))
            #flash("Please enter your phone number!")
            #return render_template("register.html")

        if len(newUser["email"]) == 0:
            errorList.append(("email"))
            #flash("Please enter an email!")
            #return render_template("register.html")

        # bob@g.com
        if newUser["email"].find("@") == -1 or newUser["email"].find(".") == -1:
            if "email" not in errorList:
                errorList.append(("email"))
            #flash("Please enter a valid email!")
            #return render_template("register.html")

        if len(newUser["password"]) == 0:
            errorList.append("password")
            #flash("Please enter a password!")
            #return render_template("register.html")

        if len(errorList) > 0:
            errorStr = "Please enter a valid "
            for i in range(len(errorList)):
                if len(errorList) == 1:
                    errorStr += errorList[i] + "."
                    flash(errorStr)
                    return render_template("register.html")
                elif len(errorList) == 2:
                    errorStr += errorList[0] + " and " + errorList[1] + "."
                    flash(errorStr)
                    return render_template("register.html")
                else:
                    errorStr += errorList[i]

                    if i == len(errorList) - 2:
                        errorStr += ", and "
                    elif i == len(errorList) - 1:
                        errorStr += "."
                    else:
                        errorStr += ", "
            flash(errorStr)
            return render_template("register.html")

        accountExists = False

        for user in users:
            if newUser.get("email") == user.get("email"):
                accountExists = True

        if not accountExists:
            # 012 345 6789
            phoneNum = str(newUser.get("phone_num"))
            newUser["phone_num"] = "(" + phoneNum[0:3] + ") " + phoneNum[3:6] + " - " + phoneNum[6:]

            users.append(newUser)
            isLoggedIn = True
            currentUser = newUser
            return redirect(url_for('index'))
        else:
            flash("Account with that email exists!")
            return render_template("register.html")
    
    elif isLoggedIn:
        return redirect(url_for('index'))
    elif request.method == "GET" or not isLoggedIn:
        return render_template("register.html")

@app.route("/userlist")
def userlist():
    global isLoggedIn
    global users
    global currentUser
    global requests

    list = ""

    for user in users:
        list += "[Name: " + user.get("name") + ", Phone Number: " + str(user.get("phone_num")) + ", Email: " + user.get("email") + ", Password: " + user.get("password") + "] "

    return list

@app.route("/logout")
def logout():
    global isLoggedIn
    global users
    global currentUser
    global requests

    isLoggedIn = False
    currentUser = None
    return redirect(request.referrer, code=302)

@app.context_processor
def context_processor():
    global isLoggedIn
    global users
    global currentUser
    global requests

    return dict(isLoggedIn=isLoggedIn, users=users, currentUser=currentUser, requests=requests)
    #return dict(key='reeE')

def getCurrentTime():
    now = datetime.now()
    time = ""

    if now.hour == 0:
        time = now.strftime("%d/%m/%Y 12:%M:%S AM")
    elif now.hour > 0 and now.hour < 12:
        time = now.strftime("%d/%m/%Y %H:%M:%S AM")
    elif now.hour == 12:
        time = now.strftime("%d/%m/%Y 12:%M:%S PM")
    elif now.hour >= 12 and now.hour < 24:
        hr = now.hour - 12
        time = now.strftime("%d/%m/%Y " + str(hr) + ":%M PM")

    return time

if __name__ == "__main__":
    app.run(debug=True)