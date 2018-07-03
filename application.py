from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask import flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item
from flask import make_response
from flask import session as login_session
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import json
import httplib2
import random
import string
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
        open("client_secrets.json", "r").read())["web"]["client_id"]
SECRET_KEY = json.loads(
        open("other_secrets.json", "r").read())["secret_key"]
APPLICATION_NAME = "Restaurant Menu Application"

engine = create_engine("sqlite:///itemcatalog.db",
                       connect_args={"check_same_thread": False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# ----- API Endpoints -----

@app.route("/category/<int:category_id>/JSON/")
def categoryJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).first()
    items = session.query(Item).filter_by(category_id=category_id).all()
    return jsonify(Items=[i.serialize for i in items])


@app.route("/category/<int:category_id>/item/<int:item_id>/JSON/")
def itemJSON(category_id, item_id):
    item = session.query(Item).filter_by(id=item_id).first()
    return jsonify(Item=item.serialize)


# ----- Authentication -----

# Create anti-forgery state token
@app.route("/login")
def showLogin():
    state = "".join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session["state"] = state
    return render_template("login.html", STATE=state)


# CONNECT - Validate the user and log in
@app.route("/gconnect", methods=["POST"])
def gconnect():
    # Validate state token
    if request.args.get("state") != login_session["state"]:
        response = make_response(json.dumps("Invalid state parameter."), 401)
        response.headers["Content-Type"] = "application/json"
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets("client_secrets.json", scope="")
        oauth_flow.redirect_uri = "postmessage"
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps("Failed to upgrade the authorization code."), 401)
        response.headers["Content-Type"] = "application/json"
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ("https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s"
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, "GET")[1])
    # If there was an error in the access token info, abort.
    if result.get("error") is not None:
        response = make_response(json.dumps(result.get("error")), 500)
        response.headers["Content-Type"] = "application/json"
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token["sub"]
    if result["user_id"] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers["Content-Type"] = "application/json"
        return response

    # Verify that the access token is valid for this app.
    if result["issued_to"] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers["Content-Type"] = "application/json"
        return response

    stored_access_token = login_session.get("access_token")
    stored_gplus_id = login_session.get("gplus_id")
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
                                 "Current user is already connected."), 200)
        response.headers["Content-Type"] = "application/json"
        return response

    # Store the access token in the session for later use.
    login_session["access_token"] = credentials.access_token
    login_session["gplus_id"] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {"access_token": credentials.access_token, "alt": "json"}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session["username"] = data["name"]
    login_session["picture"] = data["picture"]
    login_session["email"] = data["email"]

    output = ""
    output += "<h1>Welcome, "
    output += login_session["username"]
    output += "!</h1>"
    output += '<img src="'
    output += login_session["picture"]
    output += """ "style = "width: 300px; height: 300px;
                 border-radius: 150px;-webkit-border-radius: 150px;
                 -moz-border-radius: 150px;">"""
    flash("you are now logged in as %s" % login_session["username"])
    print "done!"
    return output


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route("/gdisconnect")
def gdisconnect():
    access_token = login_session.get("access_token")
    if access_token is None:
        print "Access Token is None"
        response = make_response(json.dumps("Current user not connected."),
                                 401)
        response.headers["Content-Type"] = "application/json"
        return response
    print "In gdisconnect access token is %s", access_token
    print "User name is: "
    print login_session["username"]
    google_oauth_url = "https://accounts.google.com/o/oauth2/revoke?token=%s"
    url = google_oauth_url % login_session["access_token"]
    h = httplib2.Http()
    result = h.request(url, "GET")[0]
    print "result is "
    print result
    if result["status"] == "200":
        del login_session["access_token"]
        del login_session["gplus_id"]
        del login_session["username"]
        del login_session["email"]
        del login_session["picture"]
        response = make_response(json.dumps("Successfully disconnected."), 200)
        response.headers["Content-Type"] = "application/json"
        return response
    else:
        response = make_response(
                json.dumps("Failed to revoke token for given user.", 400))
        response.headers["Content-Type"] = "application/json"
        return response


# ----- Home page -----

@app.route("/")
def home():
    categories = session.query(Category).all()
    return render_template("items.html", categories=categories)


# ----- Categories -----

@app.route("/category/new/", methods=["GET", "POST"])
def newCategory():
    if "username" not in login_session:
        flash("You are not logged in. Please login to create a new category.",
              "login")
        return redirect("/")
    if request.method == "POST":
        category = Category(name=request.form["name"])
        session.add(category)
        session.commit()
        return redirect(url_for("showItems", category_id=category.id))
    else:
        return render_template("newCategory.html")


@app.route("/category/<int:category_id>/edit/", methods=["GET", "POST"])
def editCategory(category_id):
    if "username" not in login_session:
        flash("You are not logged in. Please login to edit the category.",
              "login")
        return redirect("/")
    category = session.query(Category).filter_by(id=category_id).first()
    name = category.name
    if request.method == "POST":
        newName = request.form["name"]
        if newName:
            category.name = newName
        session.add(category)
        session.commit()
        return redirect(url_for("showItems", category_id=category_id))
    else:
        return render_template("editCategory.html", category=category)


@app.route("/category/<int:category_id>/delete/", methods=["GET", "POST"])
def deleteCategory(category_id):
    if "username" not in login_session:
        flash("You are not logged in. Please login to delete the category.",
              "login")
        return redirect("/")
    category = session.query(Category).filter_by(id=category_id).first()
    if request.method == "POST":
        session.delete(category)
        session.commit()
        return redirect(url_for("showItems", category_id=category_id))
    else:
        return render_template("deleteCategory.html", category=category)


# ----- Items -----

@app.route("/category/<int:category_id>/item/")
def showItems(category_id):
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(id=category_id).first()
    items = session.query(Item).filter_by(category_id=category_id).all()
    return render_template("items.html", categories=categories,
                           category=category, items=items)


@app.route("/category/<int:category_id>/item/new/", methods=["GET", "POST"])
def newItem(category_id):
    if "username" not in login_session:
        flash("You are not logged in. Please login to create a new item.",
              "login")
        return redirect("/")
    category = session.query(Category).filter_by(id=category_id).first()
    if request.method == "POST":
        newItem = Item(
                name=request.form["name"],
                description=request.form["description"],
                price=request.form["price"],
                category_id=category_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for("showItems", category_id=category_id))
    else:
        return render_template("newItem.html", category=category,
                               category_id=category_id)


@app.route("/category/<int:category_id>/item/<int:item_id>/edit/",
           methods=["GET", "POST"])
def editItem(category_id, item_id):
    if "username" not in login_session:
        flash("You are not logged in. Please login to edit the item.",
              "login")
        return redirect("/")
    category = session.query(Category).filter_by(id=category_id).first()
    item = session.query(Item).filter_by(id=item_id).first()
    name = item.name
    description = item.description
    price = item.price
    if request.method == "POST":
        newName = request.form["name"]
        newPrice = request.form["price"]
        newDescription = request.form["description"]
        if newName:
            item.name = newName
        if newPrice:
            item.price = newPrice
        if newDescription:
            item.description = newDescription
        session.add(item)
        session.commit()
        return redirect(url_for("showItems", category_id=category_id))
    else:
        return render_template("editItem.html", category=category,
                               category_id=category_id, item=item)


@app.route("/category/<int:category_id>/item/<int:item_id>/delete/",
           methods=["GET", "POST"])
def deleteItem(category_id, item_id):
    if "username" not in login_session:
        flash("You are not logged in. Please login to delete the item.",
              "login")
        return redirect("/")
    category = session.query(Category).filter_by(id=category_id).first()
    item = session.query(Item).filter_by(category_id=category_id,
                                         id=item_id).first()
    if request.method == "POST":
        session.delete(item)
        session.commit()
        return redirect(url_for("showItems", category_id=category_id))
    else:
        return render_template("deleteItem.html", category=category, item=item)


if __name__ == "__main__":
    app.secret_key = SECRET_KEY
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
