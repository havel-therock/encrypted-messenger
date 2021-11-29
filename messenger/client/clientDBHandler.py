import sqlite3


def scrub(query_data):
    return ''.join(chr for chr in query_data if chr.isalnum())


def connect():
    return sqlite3.connect('clientDB.db')


def setup_database():
    con = connect()
    c = con.cursor()
    c.execute('''
              CREATE TABLE IF NOT EXISTS conversations
              ([name] TEXT PRIMARY KEY, 
              [users] TEXT,
              [no_history] INTEGER )
              ''')
    con.commit()
    con.close()


def start_conversation(name, creator_id, creator_name, no_history):
    con = connect()
    c = con.cursor()
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
              ([message_id] INTEGER PRIMARY KEY AUTOINCREMENT, 
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


def delete_conversation(name):
    con = connect()
    c = con.cursor()
    name_clean = scrub(name)
    users = name_clean + "_users"
    c.execute('''
              DELETE FROM conversations
              WHERE name = ?
              ''', name_clean)
    query = '''
              DROP TABLE {}
              '''.format(name_clean)
    c.execute(query)
    query = '''
              DROP TABLE {}
              '''.format(users)
    c.execute(query)
    con.commit()
    con.close()


def add_user(name, user_id, user_name):
    con = connect()
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
    con = connect()
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
    con = connect()
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


def save_message(name, sender, time, data):
    con = connect()
    c = con.cursor()
    name_clean = scrub(name)
    query = '''
          INSERT INTO {} (sender, time, data)
          VALUES (?, ?, ?)
          '''.format(name_clean)
    c.execute(query, [sender, time, data])

    con.commit()
    con.close()


def delete_message(name, msg_id):
    con = connect()
    c = con.cursor()
    name_clean = scrub(name)
    query = '''
              DELETE FROM {} 
              WHERE message_id = ?
              '''.format(name_clean)
    c.execute(query, [msg_id])

    con.commit()
    con.close()


def get_message(name, msg_id):
    con = connect()
    c = con.cursor()
    name_clean = scrub(name)
    query = '''
              SELECT * FROM {} 
              WHERE message_id = ?
              '''.format(name_clean)
    return c.execute(query, [msg_id]).fetchone()


def get_all_messages(name):
    con = connect()
    c = con.cursor()
    name_clean = scrub(name)
    query = '''
              SELECT * FROM {} 
              '''.format(name_clean)
    return c.execute(query).fetchall()


if __name__ == "__main__":
    # con = connect()
    # c = con.cursor()
    # print(c.execute('SELECT * FROM  "t"').fetchall())

    print("--------------")
