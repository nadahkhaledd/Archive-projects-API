import mysql.connector

connection = mysql.connector.connect(user='root', password='0000', host='127.0.0.1')

cursor = connection.cursor()

cursor.execute("DROP database IF EXISTS Archives")
q = "CREATE database Archives"
cursor.execute(q)

cursor.execute("DROP TABLE IF EXISTS archives.Asset")
q = "CREATE TABLE Archives.Asset" \
    " (id INT NOT NULL, name VARCHAR(45) NULL, PRIMARY KEY (id))"
cursor.execute(q)

cursor.execute("DROP TABLE IF EXISTS Archives.Department")
q = "CREATE TABLE archives.Department" \
    " ( id INT NOT NULL,name VARCHAR(45) NULL,assets INT NULL,PRIMARY KEY (id)," \
    "FOREIGN KEY (assets) REFERENCES Asset(id) " \
    "ON DELETE CASCADE" \
    " ON UPDATE CASCADE)"
cursor.execute(q)

cursor.execute("DROP TABLE IF EXISTS Archives.Project")
q = "CREATE TABLE archives.Project" \
    " ( id INT NOT NULL,name VARCHAR(45) NULL,departments INT NULL,PRIMARY KEY (id)," \
    "FOREIGN KEY (departments) REFERENCES Department(id) " \
    "ON DELETE CASCADE" \
    " ON UPDATE CASCADE)"
cursor.execute(q)

connection.close()