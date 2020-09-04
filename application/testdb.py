from db import init_db, session,engine
from model import Item, Combo
    
init_db()

raw_connection = engine.raw_connection()
c = raw_connection.cursor()
c.execute("select count(*) from items")
nrows = c.fetchall()[0][0]

print(f"number of rows in database: { nrows }")
if nrows == 0:
    print(f"Initializing rows using 'init.sql'")
    raw_connection.cursor().executescript(open("init.sql").read())
    c.execute("select count(*) from items")
    nrows = c.fetchall()[0][0]
    print(f"Inserted { nrows } in the database")
raw_connection.commit()

# print( pd.read_sql_table(
#     "items",
#     con=engine
# ))