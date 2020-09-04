from db import init_db, session,engine
from model import Item, Combo
import pandas as pd
if True:
    init_db()
    # for cat in range(3):
    #     item = Item(
    #         name =  "Gun"+str(cat),
    #         nominal =22,
    #         min_val = 22,
    #         lifetime = 231,
    #         weapon_type = "revolver",
    #         mod = "one",
    #         subtype = cat,
    #         buyprice = 22,
    #         sellprice = 100,
    #         trader_loc = 2,
    #         count_in_cargo = 2,
    #         count_in_hoarder =  3,
    #         count_in_map = 11,
    #         count_in_player = 23
    #         )
    #     session.add(item)
    # session.commit()

# print(session.query(Item).all())

# for class_instance in session.query(Item).all():
#     print(vars(class_instance))

# print([x[0] for x in session.query(Item.__table__.c["subtype"]).distinct().all()])

if True:
    raw_connection = engine.raw_connection()
    # raw_connection.cursor().executescript(open("init.sql").read())
    c = raw_connection.cursor()
    c.execute("select count(*) from items")
    print(c.fetchall())
    raw_connection.commit()

print( pd.read_sql_table(
    "items",
    con=engine
))