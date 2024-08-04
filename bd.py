import sqlite3 as sq

db = sq.connect('new_db.db')
cur = db.cursor()

async def db_start():
    cur.execute("CREATE TABLE If NOT EXISTS profile(user_id TEXT PRIMARY KEY, name TEXT, age TEXT, info TEXT, sociallink TEXT)")
    db.commit()

async def create_profile(user_id):
    user = cur.execute("SELECT 1 FROM profile WHERE user_id == '{key}'".format(key=user_id)).fetchone() 
    if not user:
        cur.execute("INSERT INTO profile VALUES(?, ?, ?, ?, ?)", (user_id, '', '', '', ''))
        db.commit()

async def edit_profile(user_id, data):
    cur.execute("UPDATE profile SET name = '{}', age = '{}', info = '{}', sociallink = '{}' WHERE user_id == '{}'".format(
        data['name'], data['age'], data['info'], data['sociallink'], user_id))
    db.commit()



