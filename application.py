from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item

app = Flask(__name__)

engine = create_engine("sqlite:///itemcatalog.db",
        connect_args={"check_same_thread":False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# ----- Home page -----

@app.route("/")
@app.route("/home/")
def home():
    # categories = session.query(Category).all()
    return "This is the home page"
    # return render_template("restaurants.html", restaurants=restaurants)


# ----- Categories -----

@app.route("/category/new/", methods=["GET", "POST"])
def newCategory():
    if request.method == "POST":
        # category = Category(name=request.form["name"])
        # session.add(category)
        # session.commit()
        # flash("New category created!", "category")
        # return redirect(url_for("showItems"))
        return "POST request sent for newCategory"
    else:
        return "newCategory page"
        # return render_template("newCategory.html")


@app.route("/category/<int:category_id>/edit/", methods=["GET", "POST"])
def editCategory(category_id):
    # category = session.query(Category).filter_by(id=category_id).first()
    # name = category.name
    if request.method == "POST":
        # newName = request.form["name"]
        # if newName:
        #     category.name = newName
        # session.add(category)
        # session.commit()
        # flash("Category has been edited", "category")
        # return redirect(url_for("showItems"))
        return "POST request sent for editCategory"
    else:
        return "editCategory page"
        # return render_template("editCategory.html", category=category)


@app.route("/category/<int:category_id>/delete/", methods=["GET", "POST"])
def deleteCategory(category_id):
    # category = session.query(Category).filter_by(id=category_id).first()
    if request.method == "POST":
        # session.delete(category)
        # session.commit()
        # flash("Category has been deleted", "category")
        # return redirect(url_for("showItems"))
        return "POST request sent for deleteCategory"
    else:
        return "deleteCategory page"
        # return render_template("deleteCategory.html", category=category)


# ----- Items -----

@app.route("/category/<int:category_id>/item/")
def showItems(category_id):
    # category = session.query(Category).filter_by(id=category_id).first()
    # items = session.query(Item).filter_by(category_id=category_id).all()
    return "These are all the items in category %s" % category_id
    # return render_template("menu.html", category=category, items=items)


@app.route("/category/<int:category_id>/item/new/", methods=["GET", "POST"])
def newItem(category_id):
    if request.method == "POST":
        # newItem = Item(
        #         name=request.form["name"],
        #         price=request.form["price"],
        #         description=request.form["description"],
        #         course=request.form["course"],
        #         category_id=category_id)
        # session.add(newItem)
        # session.commit()
        # flash("New menu item created!", "menuItem")
        # return redirect(url_for("showMenu", category_id=category_id))
        return "POST request sent for newItem"
    else:
        return "newItem page"
        # return render_template("newMenuItem.html", category_id=category_id)


@app.route("/category/<int:category_id>/item/<int:item_id>/edit/",
        methods=["GET", "POST"])
def editItem(category_id, item_id):
    # item = session.query(Item).filter_by(id=item_id).first()
    # name = item.name
    # price = item.price
    # description = item.description
    if request.method == "POST":
        # newName = request.form["name"]
        # newPrice = request.form["price"]
        # newDescription = request.form["description"]
        # if newName:
        #     item.name = newName
        # if newPrice:
        #     item.price = newPrice
        # if newDescription:
        #     item.description = newDescription
        # session.add(item)
        # session.commit()
        # flash("Item has been edited", "item")
        # return redirect(url_for("showMenu", category_id=category_id))
        return "POST request sent for editItem"
    else:
        return "editItem page"
        # return render_template("editItem.html", category_id=category_id,
        #         item=item)


@app.route("/category/<int:category_id>/item/<int:item_id>/delete/",
        methods=["GET", "POST"])
def deleteItem(category_id, item_id):
    # item = session.query(Item).filter_by(id=item_id).first()
    if request.method == "POST":
        # session.delete(item)
        # session.commit()
        # flash("Item has been deleted", "item")
        # return redirect(url_for("showMenu", category_id=category_id))
        return "POST request sent for deleteItem"
    else:
        return "deleteItem page"
        # return render_template("deleteItem.html", item=item)


if __name__ == "__main__":
    # app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
