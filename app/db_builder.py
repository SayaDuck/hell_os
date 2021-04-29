import sqlite3


DB_FILE = "data.db"
text_factory = str


# makes users and entries table in database if they do not exist already
def createTables():
    db = sqlite3.connect(DB_FILE)
    db.text_factory = text_factory
    c = db.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT,
              password TEXT, location TEXT, currency INTEGER, rank INTEGER, fairies INTEGER, fruits TEXT);""")
    c.execute("""CREATE TABLE IF NOT EXISTS fruitlings (fruit_id INTEGER PRIMARY KEY, user_id INTEGER, fruit_type TEXT, growth INTEGER);""")
    c.execute("""CREATE TABLE IF NOT EXISTS fruit_stats (id INTEGER PRIMARY KEY, fruit TEXT, rarity INTEGER, fun_fact TEXT);""")
    c.execute("""CREATE TABLE IF NOT EXISTS store (id INTEGER PRIMARY KEY, name TEXT, fruit_stats_ID INTEGER, cost INTEGER, rank INTEGER);""")
    db.commit()
    db.close()

createTables()

# adds user info to user table
def register(username, password, location, fruits):
    db = sqlite3.connect(DB_FILE)
    db.text_factory = text_factory
    c = db.cursor()
    command = "INSERT INTO users (username, password, location, currency, rank, fairies, fruits) VALUES (?,?,?,0,1,0,?);"
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

printDatabase()

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
    user_fruits = user_fruits + str(c.execute("SELECT COUNT(*) FROM fruitlings") - 1) + ","
    c.execute("UPDATE users SET fruits=? WHERE user_id=?;", (user_fruits, user_id))
    db.commit()
    db.close()

def list_fruits(user_id):
    db = sqlite3.connect(DB_FILE)
    db.text_factory = text_factory
    c = db.cursor()
    fruit = getInfo(getUsername(user_id), "fruits")
    for i in fruit.split(','):
        info = getFruit_Stats(i)
    db.commit()
    db.close()
    return info

#grow a fruit
def grow_fruit(fruit_id, growth):
    db = sqlite3.connect(DB_FILE)
    db.text_factory = text_factory
    c = db.cursor()
    command = ("UPDATE fruitlings SET growth=? WHERE fruit_id=?;", (growth + 1, fruit_id))
    db.commit()
    db.close()

# adds fruit to the game
def add_fruit(fruit, rarity, fact):
    db = sqlite3.connect(DB_FILE)
    db.text_factory = text_factory
    c = db.cursor()
    command = "INSERT INTO fruit_stats (fruit, rarity, fact) VALUES (?,?,?);"
    c.execute(command, (fruit, rarity, fact))
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

def getFruit_Stats(fruit_id):
    if (fruit_id <= (c.execute("SELECT COUNT(*) FROM fruitlings") - 1)):
        db = sqlite3.connect(DB_FILE)
        db.text_factory = text_factory
        c = db.cursor()
        info = c.execute("SELECT * FROM fruitlings WHERE fruit_id=?;", [fruit_id]).fetchall()
        for i in info:
            print (info[i])
        db.commit()
        db.close()
        return info
    return None

def test():
    register("DeanC", "password", "New York", "apple")
    print (getUsername(1))
    new_fruit(1, "bannana")
    grow_fruit(1, 2)
    list_fruits(1)
    printDatabase()

test()


"""
# changes a user's blog info given a new blog name and description
def updateBlogInfo(username, blogname, desc):
    if checkUsername(username):
        db = sqlite3.connect(DB_FILE)
        db.text_factory = text_factory
        c = db.cursor()
        c.execute("UPDATE users SET blogname=? WHERE username=?;", (blogname, username))
        c.execute("UPDATE users SET blogdescription=? WHERE username=?;", (desc, username))
        db.commit()
        db.close()

# converts rows in database to a dictionary
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# returns a list of dictionaries containing each blog's info
def getBlogs():
    db = sqlite3.connect(DB_FILE)
    db.text_factory = text_factory
    db.row_factory = dict_factory
    c = db.cursor()
    blogs = c.execute("SELECT * from users ORDER BY time DESC;").fetchall()
    db.commit()
    db.close()
    return blogs

# deletes all users from the database (for testing purposes)
def clearUsers():
    db = sqlite3.connect(DB_FILE)
    db.text_factory = text_factory
    c = db.cursor()
    c.execute("DELETE from users;")
    db.commit()
    db.close()

# Delete a specific user
def clearUser(username):
    db = sqlite3.connect(DB_FILE)
    db.text_factory = text_factory
    c = db.cursor()
    c.execute("DELETE from users WHERE username=?;", [username])
    db.commit()
    db.close()

#Adds an entry to the entries table
def addEntry(userID, title, post, pic):
    db = sqlite3.connect(DB_FILE)
    db.text_factory = text_factory
    c = db.cursor()
    #Gets the current date and time
    dateAndTimeTup = c.execute("SELECT datetime('now','localtime');").fetchone()
    dateAndTime = str(''.join(map(str, dateAndTimeTup)))
    command = "INSERT INTO entries (userID, time, title, post, pic) VALUES (?,?,?,?,?);"
    #Executes command
    c.execute(command, (str(userID), dateAndTime, title, post, pic))
    #New time of entry
    c.execute("UPDATE users SET time=? WHERE id=?;", (dateAndTime, str(userID)))
    db.commit()
    db.close()

#Edits a past entry based on id
def editEntry(entryID, title, post, pic):
    db = sqlite3.connect(DB_FILE)
    db.text_factory = text_factory
    c = db.cursor()
    dateAndTimeTup = c.execute("SELECT datetime('now','localtime');").fetchone()
    dateAndTime = str(''.join(map(str, dateAndTimeTup)))
    #Updates the entries
    c.execute("UPDATE entries SET title=? WHERE id=?;", (title, str(entryID)))
    c.execute("UPDATE entries SET post=? WHERE id=?;", (post, str(entryID)))
    c.execute("UPDATE entries SET time=? WHERE id=?;", (dateAndTime, str(entryID)))
    c.execute("UPDATE entries SET pic=? WHERE id=?;", (pic, str(entryID)))
    userID = c.execute("SELECT userID FROM entries WHERE id=?;", [str(entryID)]).fetchone()
    c.execute("UPDATE users SET time=? WHERE id=?;", (dateAndTime, str(userID[0])))
    db.commit()
    db.close()

#Gets all of a users entries
def getEntries(userID):
    db = sqlite3.connect(DB_FILE)
    db.text_factory = text_factory
    db.row_factory = dict_factory
    c = db.cursor()
    entries = c.execute("SELECT * FROM entries WHERE userID=? ORDER BY time DESC;", [str(userID)]).fetchall()
    db.commit()
    db.close()
    return entries

#Gets an entries information based on entryID
def getEntryInfo(entryID, col):
    db = sqlite3.connect(DB_FILE)
    db.text_factory = text_factory
    c = db.cursor()
    info = c.execute("SELECT " + col + " FROM entries WHERE id=?;", [str(entryID)]).fetchone()[0]
    db.commit()
    db.close()
    return info

#deletes an entry
def deleteEntry(entryID):
    db = sqlite3.connect(DB_FILE)
    db.text_factory = text_factory
    c = db.cursor()
    c.execute("DELETE FROM entries WHERE id=?;", [str(entryID)])
    db.commit()
    db.close()

#searches the database's entries for a specific word
def search(criteria):
    db = sqlite3.connect(DB_FILE)
    db.text_factory = text_factory
    db.row_factory = dict_factory
    c = db.cursor()
    criteria_list = ['%' + i.replace('%', '[%]') + '%' for i in criteria.split()]
    command = "SELECT * FROM entries WHERE (post LIKE ?"
    for x in criteria_list[1:]:
        command += " AND post LIKE ?"
    command += ") OR (title LIKE ?"
    for x in criteria_list[1:]:
        command += " AND title LIKE ?"
    command += ");"
    entries = c.execute(command, criteria_list + criteria_list).fetchall()
    db.commit()
    db.close()
    return entries
  

#Clears all entries, bugfixxing
def clearEntries():
    db = sqlite3.connect(DB_FILE)
    db.text_factory = text_factory
    c = db.cursor()
    c.execute("DELETE from entries;")
    db.commit()
    db.close()

# adds row to followers table if it doesn't already exist
# users with followerID follws user with userID
def addFollower(userID, followerID):
    if not checkFollower(userID, followerID):
        db = sqlite3.connect(DB_FILE)
        db.text_factory = text_factory
        c = db.cursor()
        command = "INSERT INTO followers VALUES (?,?);"
        c.execute(command, (userID, followerID))
        db.commit()
        db.close()

# removes row with specified info from followers table
def removeFollower(userID, followerID):
    db = sqlite3.connect(DB_FILE)
    db.text_factory = text_factory
    c = db.cursor()
    c.execute("DELETE FROM followers WHERE userID=? AND followerID=?;", (str(userID), str(followerID)))
    db.commit()
    db.close()

# return whether or not a user-follower pair exists
def checkFollower(userID, followerID):
    db = sqlite3.connect(DB_FILE)
    db.text_factory = text_factory
    c = db.cursor()
    found = c.execute("SELECT * FROM followers WHERE userID=? AND followerID=?;",
                      (str(userID), str(followerID))).fetchone()
    db.commit()
    db.close()
    return found is not None

# deletes everything in followers table
def clearFollowers():
    db = sqlite3.connect(DB_FILE)
    db.text_factory = text_factory
    c = db.cursor()
    c.execute("DELETE from followers;")
    db.commit()
    db.close()

# returns a list of dictionaries of blogs a user is following
def getFollowedBlogs(followerID):
    db = sqlite3.connect(DB_FILE)
    db.text_factory = text_factory
    db.row_factory = dict_factory
    c = db.cursor()
    followedUsers = c.execute("SELECT userID FROM followers WHERE followerID=?;", [str(followerID)]).fetchall()
    blogs = []
    for user in followedUsers:
        blog = c.execute("SELECT * FROM users WHERE id=?;", [str(user["userID"])]).fetchone()
        blogs.append(blog)
    db.commit()
    db.close()
    return blogs

#Clears everything
def clearAll():
    clearEntries()
    clearUsers()
    clearFollowers()

def clear():
    db = sqlite3.connect(DB_FILE)
    db.text_factory = text_factory
    c = db.cursor()
    c.execute("DROP TABLE entries;")
    db.commit()
    db.close()

"""


'''
if __name__ == "__main__":
    clearAll()
    clear()
    createTables()
    register("userA", saltString("passsssssss", salt), "my first blog", "A very cool lil blog")
    register("userB", saltString("passsssssss", salt), "I hate the other blog", "I am raging schizophrenic")
    register("userC", saltString("passsssssss", salt), "Cute Dog Pictures", "Cute dog pictures")

    addEntry("1", "Hey guys!", "Hows it going", "")
    addEntry("2", "Stop", "get off", "")
    addEntry("1", "Why are you mean :(", "You guys alright?", "")
    addEntry("3", "Dog", "imagine a dog here", "")
    addEntry("1", "oh god", "Hahah hey", "")
    deleteEntry("4")

    addFollower(1, 2)  # 2 follows 1
    addFollower(2, 1)  # 1 follows 2
    addFollower(3, 2)  # 2 follows 3
    # removeFollower(1,2)

    print(checkFollower(2, 1))
    print(checkFollower(1, 2))
    print(getFollowedBlogs(2))


printDatabase()
getBlogs()
'''
