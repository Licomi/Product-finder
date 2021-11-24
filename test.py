import sqlite3
# from add_site import get_icon_site


conn = sqlite3.connect('DATABASE.db')
cursor = conn.cursor()
# cursor.execute("""PRAGMA table_info(Category)""")
# cursor.execute("""DROP TABLE Сategories""")
# cursor.execute("""CREATE TABLE Сategories (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     id_shop INTEGER,
#     name TEXT,
#     url TEXT,
#     FOREIGN KEY(id_shop) REFERENCES Shops(id)
# );""")


# cursor.execute("""UPDATE Shops SET icon = ? WHERE id = 1""", (get_icon_site('https://best.aliexpress.ru'), ))
# cursor.execute("""PRAGMA table_info(Сategories);""")
# cursor.execute("""SELECT * FROM Сategories""")
# cursor.execute("""SELECT name FROM sqlite_master WHERE type='table'""")
for i in cursor.fetchall():
    print(i)
print('-'*75)

# for i in cursor.fetchall():
#     print(i)

conn.commit()
