# Item Catalog

A project that lists out categories, and items in those categories. Demonstrates basic CRUD operations. Part of the Udacity Full Stack Web Developer Nanodegree.

## Getting Started
- Clone this repository to your local machine, and change directories into it
    - ```$ git clone https://github.com/bean00/item-catalog.git```
    - ```$ cd item-catalog```
- Start up the Vagrant virtual machine (VM)
- Run `python database_setup.py`
- Run `python lotsofitems.py` (to populate database with initial data)
- Run `python application.py`
- Open `localhost:5000` in a web browser

## Interacting With the Database
- To load up the database and interact with it in the Python shell, run:
  `python -i setup_db.py`
- To see all the Category objects, run:
  `session.query(Category).all()`
- To see a single Category object, run:
  `session.query(Category).first()`
- For Item, same as above, replacing `Category` with `Item`
- To inspect a single Item, run:
  `item = session.query(Item).first()`
  - Then, you can run:
    `item.name`, `item.id`, `item.description`, etc. to see the values
    for that item

## Dependencies
- Make sure the following packages are installed
  - *Note: Version number might not need to be exactly the same
- Flask            (1.0.2)
- Flask-HTTPAuth   (3.2.3)
- Flask-SQLAlchemy (2.3.2)
- httplib2         (0.11.3)
- Jinja2           (2.10)
- oauth2client     (4.1.2)
- SQLAlchemy       (1.2.7)
