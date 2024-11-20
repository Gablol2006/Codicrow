import sqlite3

try:
    conn = sqlite3.connect('registro_usuarios.db')
    print("Opened database successfully")

    conn.execute('CREATE TABLE Usuarios (name TEXT, mail TEXT, city TEXT, pin TEXT)')
    print("Table created successfully")
    conn.close()
    
except Exception as ex:
    print(ex)