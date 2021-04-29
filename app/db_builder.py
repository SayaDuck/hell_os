import sqlite3


DB_FILE = "data.db"
text_factory = str


# makes users and entries table in database if they do not exist already
def createTables():
    db = sqlite3.connect(DB_FILE)
    db.text_factory = text_factory
    c = db.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT,
              password TEXT, location TEXT, exp INTEGER, fruits TEXT);""")
    c.execute("""CREATE TABLE IF NOT EXISTS fruitlings (fruit_id INTEGER PRIMARY KEY, user_id INTEGER, fruit_type TEXT, growth INTEGER);""")
    c.execute("""CREATE TABLE IF NOT EXISTS fruit_stats (fruit_type TEXT, nutrition TEXT, img TEXT, xpreq INTEGER)""")
    db.commit()
    db.close()

createTables()


# adds user info to user table
def register(username, password, location, fruits):
    db = sqlite3.connect(DB_FILE)
    db.text_factory = text_factory
    c = db.cursor()
    command = "INSERT INTO users (username, password, location, exp, fruits) VALUES (?,?,?,0,?);"
    c.execute(command, (username, password, location, fruits))
    db.commit()
    db.close()


# returns whether or not username is in user table
def checkUsername(username):
    db = sqlite3.connect(DB_FILE)
    db.text_factory = text_factory
    c = db.cursor()
    found = False
    for row in c.execute("SELECT * FROM users;"):
        found = found or (username == row[1])
    db.commit()
    db.close()
    return found


# prints user table (for testing purposes)
def printDatabase():
    db = sqlite3.connect(DB_FILE)
    db.text_factory = text_factory
    c = db.cursor()
    print("--------Users Table-----------")
    for row in c.execute("SELECT * FROM users;"):
        print(row)
    print("--------Fruitling Table-------")
    for row in c.execute("SELECT * FROM fruitlings;"):
        print(row)
    print("-------Fruit Table----------")
    for row in c.execute("SELECT * FROM fruit_stats;"):
        print(row)
    db.commit()
    db.close()

#printDatabase()

# returns information about a user from the specified column
# col can be 'password', 'location', 'money', 'rank', or 'fairy'
def getInfo(username, col):
    if checkUsername(username):
        db = sqlite3.connect(DB_FILE)
        db.text_factory = text_factory
        c = db.cursor()
        #Finds the user with the correct username
        info = c.execute("SELECT " + col + " FROM users WHERE username=?;", [username]).fetchone()
        db.commit()
        db.close()
        return info
    return None

#creates a new fruitling belonging to a user
def new_fruit(user_id, fruit_type):
    db = sqlite3.connect(DB_FILE)
    db.text_factory = text_factory
    c = db.cursor()
    command = "INSERT INTO fruitlings (user_id, fruit_type, growth) VALUES (?,?,0)"
    c.execute(command, (user_id, fruit_type))
    username = getUsername(user_id)
    user_fruits = getInfo(username, "fruits")
    c.execute("SELECT COUNT(*) FROM fruitlings")
    user_fruits = user_fruits[0] + str(int(c.fetchone()[0])) + ","
    c.execute("UPDATE users SET fruits=? WHERE id=?;", (user_fruits, user_id))
    db.commit()
    db.close()

#list fruitlings
def list_fruits(user_id):
    db = sqlite3.connect(DB_FILE)
    db.text_factory = text_factory
    c = db.cursor()
    fruit = getInfo(getUsername(user_id), "fruits")
    splitfruit = fruit[0][:-1].split(',')
    for i in splitfruit:
        info = getFruit_Stats(int(i))
    db.commit()
    db.close()
    return info

#grow a fruitling
def grow_fruit(fruit_id, growth):
    db = sqlite3.connect(DB_FILE)
    db.text_factory = text_factory
    c = db.cursor()
    grew = c.execute("SELECT growth FROM fruitlings WHERE fruit_id=?", [fruit_id]).fetchone()
    c.execute("UPDATE fruitlings SET growth=? WHERE fruit_id=?;", (growth + grew[0], fruit_id))
    db.commit()
    db.close()

# adds fruit to the game
def add_fruit(fruit, nutrition, img, xp):
    db = sqlite3.connect(DB_FILE)
    db.text_factory = text_factory
    c = db.cursor()
    command = "INSERT INTO fruit_stats (fruit_type, nutrition, img, xpreq) VALUES (?,?,?,?);"
    c.execute(command, (fruit, nutrition, img, xp))
    db.commit()
    db.close()


#Gets a username based on a user id
def getUsername(userID):
    db = sqlite3.connect(DB_FILE)
    db.text_factory = text_factory
    c = db.cursor()
    info = c.execute("SELECT username FROM users WHERE id=?;", [userID]).fetchone()
    db.commit()
    db.close()
    if info is None:
        return info
    return info[0]

#gain exp from trivia (lose exp with negative gain)
def expUp(user_id, gain):
    db = sqlite3.connect(DB_FILE)
    db.text_factory = text_factory
    c = db.cursor()
    grew = c.execute("SELECT exp FROM users WHERE user_id=?", [user_id]).fetchone()[0]
    c.execute("UPDATE users SET exp=? WHERE user_id=?;", (grew + gain, user_id))
    db.commit()
    db.close()

#fruitling info, either "img", "nutrition", or "xp"
def getFruit_Stats(fruit_id, requesttype):
    db = sqlite3.connect(DB_FILE)
    db.text_factory = text_factory
    c = db.cursor()
    c.execute("SELECT COUNT(*) FROM fruitlings")
    if (int(fruit_id) <= (int(c.fetchone()[0]))):
        db = sqlite3.connect(DB_FILE)
        db.text_factory = text_factory
        c = db.cursor()
        info = c.execute("SELECT * FROM fruitlings WHERE fruit_id=?;", [fruit_id]).fetchall()[0]
        print ("Fruit " + str(info[0]) + ": \n" + "  Type: " + str(info[2]) + "\n  Growth: " + str(info[3]))
        if requesttype == "nutrition":
            nutrition = c.execute("SELECT nutrition FROM fruit_stats WHERE fruit_type=?", [info[2].capitalize()]).fetchone()
            nutrition = nutrition[0]
            return nutrition
            db.commit()
            db.close()
        if requesttype == "img":
            img = c.execute("SELECT img FROM fruit_stats WHERE fruit_type=?", [info[2].capitalize()]).fetchone()
            return img
            db.commit()
            db.close()
        if requesttype == "xp":
            xp = c.execute("SELECT xpreq FROM fruit_stats WHERE fruit_type=?"), [info[2]].fetchone()
            return xp
            db.commit()
            db.close()
        db.commit()
        db.close()
        
        
    return None

# deletes all users from the database (for testing purposes)
def clearUsers():
    db = sqlite3.connect(DB_FILE)
    db.text_factory = text_factory
    c = db.cursor()
    c.execute("DELETE from users;")
    db.commit()
    db.close()

def clearFruits():
    db = sqlite3.connect(DB_FILE)
    db.text_factory = text_factory
    c = db.cursor()
    c.execute("DELETE from fruitlings;")
    db.commit()
    db.close()

#woo.