from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Category, Base, Item

engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Items for 'Household Items'
category1 = Category(name="Household Items")
session.add(category1)
session.commit()

item1 = Item(name="Pencil", description="A writing instrument (erasable)",
        price="$2.99", category=category1)
session.add(item1)
session.commit()

item2 = Item(name="Pen", description="A writing instrument (non-erassable)",
        price="$3.50", category=category1)
session.add(item2)
session.commit()

item3 = Item(name="Tissue", description="Magical artifact with many uses",
        price="$300", category=category1)
session.add(item3)
session.commit()

item4 = Item(name="Blanket", description="Large flat sheet for warmth",
        price="$10.50", category=category1)
session.add(item4)
session.commit()


# Items for 'Sports Equipment'
category2 = Category(name="Sports Equipment")
session.add(category2)
session.commit()

item5 = Item(name="Tennis racquet", description="Thing with a head and handle to hit balls with",
        price="$85", category=category2)
session.add(item5)
session.commit()

item6 = Item(name="Basketball", description="A ball to throw into a basket",
        price="$33", category=category2)
session.add(item6)
session.commit()

item7 = Item(name="Towel", description="Wipe off perspiration",
        price="$3", category=category2)
session.add(item7)
session.commit()


print "All categories and items successfully added."
