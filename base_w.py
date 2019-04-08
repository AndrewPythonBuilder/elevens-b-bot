import sqlite3

def init(id, name):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (id, username, money) VALUES (?, ?, ?)', (id, name, 2))
    conn.commit()
    cursor.close()
    conn.close()

def id():
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM users ')
    write = cursor.fetchall()

    conn.commit()
    cursor.close()
    conn.close()
    wr = []
    for i in write:
        wr.append(i[0])
    return wr

def names():
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()

    cursor.execute('SELECT username FROM users ')
    write = cursor.fetchall()

    conn.commit()
    cursor.close()
    conn.close()
    wr = []
    for i in write:
        wr.append(str(i[0]))
    return wr

def stat_():
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()

    cursor.execute('SELECT username, money FROM users ')
    write = cursor.fetchall()

    conn.commit()
    cursor.close()
    conn.close()
    wr = ''
    for i in write:
        wr += str(i[0])+ ': ' + str(i[1]) + '\n'
    return wr

def add(name, money):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('SELECT money FROM users WHERE username=:username', {'username':name})
    write = cursor.fetchone()
    money = write[0]+money
    cursor.execute('UPDATE users SET money=:money WHERE username=:username', {'username':name, 'money':money})
    conn.commit()
    cursor.close()
    conn.close()

def stole(name, money):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('SELECT money FROM users WHERE username=:username', {'username':name})
    write = cursor.fetchone()
    money = write[0]-money
    cursor.execute('UPDATE users SET money=:money WHERE username=:username', {'username':name, 'money':money})
    conn.commit()
    cursor.close()
    conn.close()

def money(id):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('SELECT money FROM users WHERE id=:id', {'id': id})
    write = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    return str(write[0])