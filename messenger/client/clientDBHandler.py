import sqlite3


def scrub(query_data):
    return ''.join(chr for chr in query_data if chr.isalnum())


def setup_database():
    con = sqlite3.connect('testDB.db')
    c = con.cursor()
    c.execute('''
              CREATE TABLE IF NOT EXISTS conversations
              ([name] TEXT PRIMARY KEY, 
              [users] INTEGER,
              [no_history] INTEGER )
              ''')
    con.commit()
    con.close()


def start_conversation(name, creator_id, creator_name, no_history):
    con = sqlite3.connect('testDB.db')
    c = con.cursor()
    ct = c.execute('SELECT COUNT(*) from conversations').fetchone()[0] + 1
    name_clean = scrub(name)
    creator_id_clean = int(scrub(str(creator_id)))
    creator_name_clean = scrub(creator_name)
    no_history_clean = int(scrub(str(no_history)))

    c.execute('''
              INSERT INTO conversations 
              VALUES (?, ?, ?)
              ''', [name_clean, name_clean + "_users", no_history_clean])

    query = '''
              CREATE TABLE IF NOT EXISTS {}
              ([message_id] INTEGER PRIMARY KEY, 
              [sender] INTEGER,
              [time] INTEGER,  
              [data] TEXT)
              '''.format(name_clean)
    c.execute(query)

    query = '''
              CREATE TABLE IF NOT EXISTS {}
              ([user_id] INTEGER PRIMARY KEY, 
              [name] TEXT,
              [status] INTEGER )
              '''.format(name_clean + "_users")
    c.execute(query)

    query = '''
              INSERT INTO {} 
              VALUES (?, ?, ?)
              '''.format(name_clean + "_users")
    c.execute(query, [creator_id_clean, creator_name_clean, 3])

    con.commit()
    con.close()


def add_user(name, user_id, user_name):
    con = sqlite3.connect('testDB.db')
    c = con.cursor()
    name_clean = scrub(name)
    users = name_clean + "_users"
    query = '''
              SELECT status FROM {} 
              WHERE user_id = ?
              '''.format(users)
    find_user = c.execute(query, [user_id]).fetchone()
    print(find_user)
    if find_user is not None:
        if find_user[0] == 0:
            return 2  # user banned
        else:
            return 1  # user already in conversation
    else:
        query = '''
              INSERT INTO {} 
              VALUES (?, ?, ?)
              '''.format(users)
        c.execute(query, [user_id, user_name, 1])

    con.commit()
    con.close()
    return 0


def change_status(name, user_id, new_status):
    con = sqlite3.connect('testDB.db')
    c = con.cursor()
    name_clean = scrub(name)
    users = name_clean + "_users"
    query = '''
              UPDATE {} 
              SET status = ?
              WHERE user_id = ?
              '''.format(users)
    c.execute(query, [new_status, user_id])

    con.commit()
    con.close()


def remove_user(name, user_id):
    con = sqlite3.connect('testDB.db')
    c = con.cursor()
    name_clean = scrub(name)
    users = name_clean + "_users"
    query = '''
              DELETE FROM {} 
              WHERE user_id = ?
              '''.format(users)
    c.execute(query, [user_id])

    con.commit()
    con.close()


if __name__ == "__main__":
    # setup_database()
    # start_conversation("test", 0, "nm", 0)
     print(add_user("test", 2, "nts"))
    # change_status("test", 1, 0)
    # remove_user("test", 2)
