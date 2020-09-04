import categories
import distibutor
import windows


from db import init_db, session, engine
from model import Item

def setConnectionParams(username, password, p, dbname, host, odbcVersion):
    pass

def connection():
    connection = engine.raw_connection()
    return connection

con = connection()
c = con.cursor()

sql = "select mods from items group by mods"
c.execute(
    sql
    )
con.commit()

def getCoulumNames():

    return Item.__table__.columns.keys()

columns = ""
lastQuery = "select * from items"


def setColumnNames():
    global columns
    columns = ", ".join(getCoulumNames())

def getDicts(items):
    itemsListOfDicts = []

    for item in items:
        itemsListOfDicts.append(getDict(item))

    return itemsListOfDicts


def getDict(item):
    dict = {}
    keys = getCoulumNames()
    for k in range(len(item)):
        key = keys[k]
        if key == "mods":
            key = "mod"
        if key.startswith("count_in_"):
            key = key[9:]

        dict[key] = item[k]

    return dict


def insertItems(params, items):
    conn = connection()
    cursor = conn.cursor()

    cursor.fast_executemany = True
    cursor.executemany(
        "insert into items(" + params + ") values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        items)
    conn.commit()


def insertItem(parameters, item):
    conn = connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "insert into items(" + parameters + ") values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            item)
        conn.commit()
        return 0
    except:
        return 1


def createCombos(items):
    conn = connection()
    cursor = conn.cursor()

    cursor.fast_executemany = True
    cursor.executemany("insert ignore into itemcombos(item1, item2) values (?, ?)", items)
    conn.commit()


def deleteItem(itemName):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE name = ?", (itemName,))
    conn.commit()


def removeCombo(items):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM itemcombos WHERE item1 = ? AND item2 = ?", items[0], items[1])
    conn.commit()


def getItemsToZero(names, itemType):
    global lastQuery
    lastQuery = "select * \
                from items \
                where type = '" + itemType + "' \
                and name in ({0})".format(', '.join('?' for _ in names))
    con = connection()
    cursor = con.cursor()
    cursor.execute(lastQuery, names)
    return cursor.fetchall()


def getType(type, subtype=None):
    global lastQuery
    lastQuery = f"select * from items where type = '{type}'"

    if subtype is not None:
        lastQuery += f" and subtype = '{subtype}'"

    lastQuery += f";"
    con = connection()
    cursor = con.cursor()
    cursor.execute(lastQuery)
    return cursor.fetchall()


def getSubtypes():
    con = connection()
    cursor = con.cursor()
    cursor.execute("SELECT subtype FROM items group by subtype")
    return [row[0] if row[0] is not None else "" for row in cursor.fetchall()]

#!##############################################
def getTraderLocs():
    con = connection()
    cursor = con.cursor()
    cursor.execute("SELECT trader_loc FROM items group by trader_loc")
    raw_results = cursor.fetchall()
    results = [row[0] if row[0] is not None else "" for row in raw_results]
    return sorted(results)

def getTraderLocsBySubtype(subtype):
    con = connection()
    cursor = con.cursor()
    query = f"SELECT trader_loc FROM items WHERE subtype = '{subtype}' group by trader_loc"
    #print("DEBUG - query", query)
    cursor.execute(query)
    raw_results = cursor.fetchall()
    #print("DEBUG - raw_results", raw_results)
    results = [row[0] if row[0] is not None else "" for row in raw_results]
    return sorted(results)
#!##############################################

def getSubtypesMods(mod):
    con = connection()
    cursor = con.cursor()
    cursor.execute("SELECT subtype, mods FROM items WHERE mods = ? group by subtype", mod)
    return [_[0] for _ in cursor.fetchall()]

def getCategory(category, subtype=None):
    global lastQuery

    lastQuery = f"select * from items where type = '{category}'"

    if subtype is not None:
        lastQuery += f" and subtype = '{subtype}'"

    lastQuery += f";"

    con = connection()
    cursor = con.cursor()
    cursor.execute(lastQuery)
    return cursor.fetchall()

# name, subtype, tradercat, buyprice, sellprice, rarity, nominal, traderexclude, mods
def getSubtypeForTrader(subtype):
    query = "select name, subtype, tradercat, buyprice, sellprice, rarity, nominal, traderexclude, mods \
                from items \
                where subtype = '" + subtype + "';"

    con = connection()
    cursor = con.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    for i in range(len(result)):
        if result[i][3] is None:
            result[i][3] = -1
        if result[i][4] is None:
            result[i][4] = -1

        result[i] = list(result[i])
    return result

def getItemDetailsByTraderLoc(subtype, trader_loc):
    query = f'SELECT name FROM items where trader_loc = {trader_loc} and subtype = "{subtype}"'
    con = connection()
    cursor = con.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    return [row[0] for row in results]

def getItemsByName(items):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE name in ({0})\
            AND rarity <> 0".format(', '.join('?' for _ in items)), items)
    return cursor.fetchall()


def setSubtypesMany(items):
    conn = connection()
    cursor = conn.cursor()
    cursor.fast_executemany = True
    cursor.executemany("UPDATE items SET subtype = ? WHERE name = ?;", items)
    conn.commit()


def setSubtypeForTrader(items):
    conn = connection()
    cursor = conn.cursor()
    cursor.fast_executemany = True
    cursor.executemany("UPDATE items SET traderCat = ?, buyprice = ?, \
        sellprice= ?, traderExclude= ?, rarity= ? WHERE name = ?;", items)
    conn.commit()


# buyprice, sellprice, tradercat, subtype, name
def setTraderValues(items):
    conn = connection()
    cursor = conn.cursor()
    cursor.fast_executemany = True
    cursor.executemany(
        "UPDATE IGNORE items SET buyprice = ?, sellprice = ?, traderCat = ?, subtype = ? WHERE name = ?;", items)
    conn.commit()


def getLinkedItems(item):
    items = set()
    con = connection()
    cursor = con.cursor()
    cursor.execute("select * from itemcombos where item1 = ? or item2 = ?", item, item)
    fetched = cursor.fetchall()
    result = []
    for r in fetched:
        result.append(r[1:])

    if result is not None:
        item1 = [row[0] for row in result]
        item2 = [row[1] for row in result]
        for item in item1 + item2:
            items.add(item)
    return items


def getLinekd(name, type):
    if type == "gun":
        return getWeaponAndCorresponding(name)
    else:
        return getWeaponsFromAccessoire(name)


def getWeaponAndCorresponding(name):
    global lastQuery
    global columns
    lastQuery = "select " + columns + " \
                from items \
                join \
                    (select item2 \
                    FROM (select name, item2 \
                            from items \
                                    join itemcombos i on items.name = i.item1 \
                            where name LIKE '%" + name + "%') as accessoire \
                    ) as item2 on name = item2.item2 \
                    group by name;"

    con = connection()
    cursor = con.cursor()
    cursor.execute(lastQuery)
    return cursor.fetchall()


def getWeaponsFromAccessoire(name):
    global lastQuery
    lastQuery = "select " + columns + " \
                from (select item1, item2, items.* \
                      from itemcombos \
                      join items on name = item1 \
                      where item2 LIKE '%" + name + "%' \
                      ) as accessoire \
                      group by name;"

    con = connection()
    cursor = con.cursor()
    cursor.execute(lastQuery)
    return cursor.fetchall()


def searchByName(name):
    global lastQuery
    lastQuery = "select * \
                from items \
                WHERE name LIKE '%" + name + "%';"

    con = connection()
    cursor = con.cursor()
    cursor.execute(lastQuery)
    return cursor.fetchall()


def searchByNameAndType(name, type):
    global lastQuery
    lastQuery = "select * \
                from items \
                where type = '" + type + "' \
                and name LIKE '%" + name + "%';"

    con = connection()
    cursor = con.cursor()
    cursor.execute(lastQuery)
    return cursor.fetchall()


def searchByNameAndCat(name, cat):
    global lastQuery
    lastQuery = "select * \
                from items \
                where category = '" + cat + "' \
                and name LIKE '%" + name + "%';"

    con = connection()
    cursor = con.cursor()
    cursor.execute(lastQuery)
    return cursor.fetchall()


def getNominalByType(t):
    con = connection()
    cursor = con.cursor()
    cursor.execute(
        "select SUM(nominal) \
        from items \
        where type = ?", (t,)
    )
    global columns
    if columns == "":
        setColumnNames()
    return cursor.fetchone()


def getNominalByUsage(usage):
    con = connection()
    cursor = con.cursor()
    cursor.execute(
        "select SUM(nominal) \
        from items \
        where ? = 1", usage.lower()
    )
    return cursor.fetchone()


def getMinByType(type):
    con = connection()
    cursor = con.cursor()   
    cursor.execute(
        "select SUM(min) \
        from items \
        where type = ?", type
    )
    return cursor.fetchone()


def updateType(itemName, type):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE items SET type = ? WHERE name = ?", (type, itemName,))
    conn.commit()


def updateDropValue(itemName, newValue, valueType):
    if valueType == "rarity":
        updateRarity(itemName, newValue)
    if valueType == "type":
        updateType(itemName, newValue)


def updateRarity(itemName, rarity):
    # todo clean this up
    rarities = distibutor.rarities9
    if rarity in rarities.values():
        for key, value in rarities.items():
            if rarity == value:
                rarity = key

    conn = connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE items SET rarity = ? WHERE name = ?", (rarity, itemName,))
    conn.commit()


def update(values):
    query = "UPDATE items SET nominal = " + str(values["nominal"]) + ", min= " + str(values["min"]) + ", \
        restock= " + str(values["restock"]) + ", lifetime= " + str(values["lifetime"]) + ", subtype= '" + str(
        values["subtype"]) + "'" \
            + ", deloot= '" + str(values["deloot"]) + "', mods= '" + str(values["mod"]) + "',"  "trader_loc = " + str(values["trader"]) + " WHERE name = '" + str(
        values["name"] + "'" )

    conn = connection()
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()

    updateFlags(values)

    try:
        updateListValues(values["usage"], values["name"], categories.usages)
    except KeyError:
        pass

    try:
        updateListValues(values["tier"], values["name"], categories.tiers)
    except KeyError:
        pass


def updateFlags(values):
    query = "UPDATE items SET count_in_cargo = ?, count_in_hoarder = ?, count_in_map = ?, count_in_player = ?\
     WHERE name = ?"

    conn = connection()
    cursor = conn.cursor()
    try:
        x = values["cargo"]

    except KeyError:
        values["cargo"] = values["count_in_cargo"]
        values["hoarder"] = values["count_in_hoarder"]
        values["map"] = values["count_in_map"]
        values["player"] = values["count_in_player"]

    cursor.execute(query, values["cargo"], values["hoarder"], values["map"], values["player"], values["name"])
    conn.commit()


def updateMany(items):
    conn = connection()
    cursor = conn.cursor()
    cursor.fast_executemany = True
    cursor.executemany("UPDATE items SET nominal = ?, min= ?, \
        restock= ?, lifetime= ?, rarity= ? WHERE name = ?;", items)


def getItemsToDistibute(type):
    con = connection()
    cursor = con.cursor()
    cursor.execute("select * from items where type = '" + type + "' and rarity <> 'undefined'")
    return cursor.fetchall()


def getAllItems(subtype=None):
    global lastQuery
    lastQuery = "select * from items"

    if subtype is not None:
        lastQuery += " WHERE subtype = '" + subtype + "'"

    con = connection()
    cursor = con.cursor()
    cursor.execute(lastQuery)
    return cursor.fetchall()


def getMods():
    con = connection()
    cursor = con.cursor()
    cursor.execute("select mods \
                    from items \
                    group by mods;")
    rows = cursor.fetchall()
    return [row[0] for row in rows]


def getItemsFromCatMods(category, mod, allItems, allMods, search=None):
    search = None if search == "" else search
    query = ""
    if search is not None:
        query += "select name from ("
    query += "select name from items "
    if category != allItems:
        query += "WHERE type = \'{}\' ".format(category)
    if mod != allMods:
        if category != allItems:
            query += "AND "
        else:
            query += "WHERE "
        query += "mods = \'{}\'".format(mod)

    if search is not None:
        query += ") as filtered WHERE name LIKE \'%{}%\';".format(search)

    con = connection()
    cursor = con.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    return [row[0] for row in rows]


def createDB(name):
    pass


def getUsages(itemName):
    con = connection()
    cursor = con.cursor()
    cursor.execute("select " + ", ".join(categories.usages) + " from items where name = '" + itemName + "'")
    return cursor.fetchall()[0]


def getTiers(itemName):
    con = connection()
    cursor = con.cursor()
    cursor.execute("select " + ", ".join(categories.tiers) + " from items where name = '" + itemName + "'")
    return cursor.fetchall()[0]


def getRarity(itemName):
    con = connection()
    cursor = con.cursor()
    cursor.execute("select rarity from items where name = ?", (itemName,))
    return cursor.fetchall()[0][0]


def getSubtype(itemName):
    con = connection()
    cursor = con.cursor()
    cursor.execute("select subtype from items where name = ?", (itemName,))
    return cursor.fetchone()


def getFlags(itemName):
    con = connection()
    cursor = con.cursor()
    cursor.execute("select count_in_cargo, count_in_hoarder, count_in_map, count_in_player, crafted, deloot \
                    from items where name = ?", (itemName,))
    return cursor.fetchall()[0]


def getModFromItem(itemName):
    con = connection()
    cursor = con.cursor()
    cursor.execute("SELECT mods FROM items WHERE name = ?", (itemName,))
    return cursor.fetchall()


def updateListValues(newValues, name, listItems):
    usages = listItems
    query = "UPDATE items SET "
    for i in range(len(usages)):
        query += usages[i] + " = " + str(newValues[i]) + ", "

    query = query[:-2]
    query += " WHERE name = '" + name + "';"

    conn = connection()
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()


def getPath():
    con = connection()
    cursor = con.cursor()
    cursor.execute("select @@basedir")
    return cursor.fetchone()


def reExecuteLastQuery():
    global lastQuery
    con = connection()
    cursor = con.cursor()
    cursor.execute(lastQuery)
    return cursor.fetchall()


def backupDatabase(file=None):
    global user
    global pwd
    global port
    global database
    global server

    if user == "":
        c = windows.readConfig()
        user = c[0]
        pwd = c[1]
        port = c[2]
        database = c[3]
        server = c[4]

    path = getPath() + "bin\\"
    cmdL1 = [path + "mysqldump", "--port=" + port, "-h" + server, "--force", "-u" + user, "-p" + pwd, database]
    p1 = Popen(cmdL1, shell=True, stdout=PIPE)
    if file is not None:
        file.write(p1.communicate()[0])
        file.close()

    if file is None:
        return p1.communicate()[0]


def addColumns():
    query = "ALTER TABLE `" + windows.readConfig()[3] + "`.`items` \
ADD COLUMN `subtype` VARCHAR(45) NULL DEFAULT NULL AFTER `mods`, \
ADD COLUMN `buyprice` INT(11) NULL DEFAULT NULL AFTER `subtype`,\
ADD COLUMN `sellprice` INT(11) NULL DEFAULT NULL AFTER `buyprice`, \
ADD COLUMN `traderCat` VARCHAR(3) NULL DEFAULT NULL AFTER `sellprice`,\
ADD COLUMN `traderExclude` TINYINT(1) UNSIGNED ZEROFILL NOT NULL DEFAULT '0' AFTER `traderCat`;"
# TODO: DB update does not seem to work
#ADD COLUMN `trader_loc` TINYINT(1) UNSIGNED ZEROFILL NOT NULL DEFAULT '0' AFTER `traderExclude`;"

    conn = connection()
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    print("comitted db")


def addNewConstraints():
    query = "ALTER TABLE `itemcombo`\
    DROP FOREIGN KEY `itemcombos_ibfk_1`;\
ALTER TABLE `itemcombo`\
DROP FOREIGN KEY `itemcombos_ibfk_2`;\
ALTER TABLE `itemcombos`\
ADD CONSTRAINT `itemcombos_ibfk_3` \
    FOREIGN KEY (`item1`) REFERENCES `items` (`name`) \
    ON DELETE CASCADE; \
ALTER TABLE `itemcombos` \
    ADD CONSTRAINT `itemcombos_ibfk_4` \
    FOREIGN KEY (`item2`) REFERENCES `items` (`name`) \
    ON DELETE CASCADE;"

    conn = connection()
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()


def dropDB():
    global database
    if database == "":
        database = windows.readConfig()[3]

    return drop_selected_DB(database)


def drop_selected_DB(database):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("DROP SCHEMA " + database)
    conn.commit()
    return database


def loadDB():
    loadDB(windows.getContent(windows.openFile("sql")))


def loadDB(content):
    global user
    global pwd
    global port
    global database
    global server

    if user == "":
        c = windows.readConfig()
        user = c[0]
        pwd = c[1]
        p = c[2]
        database = c[3]
        server = c[4]

    path = getPath() + "bin\\"

    process = Popen(
        "\"" + path + "mysql\" -u " + user + " -p" + pwd + " -h" + server + " --port " + port + " --default-character-set=utf8 " + database,
        shell=True, stdin=PIPE)
    process.stdin.write(content)
    process.stdin.close()
    process.kill()

def getOdbcVersion():
    
        return "8.0"
