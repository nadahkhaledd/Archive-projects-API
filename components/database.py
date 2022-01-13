import mysql.connector

connection = mysql.connector.connect(user='root', password='0000', host='127.0.0.1')

cursor = connection.cursor()

cursor.execute("DROP database IF EXISTS Archives")
q = "CREATE database Archives"
cursor.execute(q)

cursor.execute("DROP TABLE IF EXISTS archives.Asset")
q = "CREATE TABLE Archives.Asset" \
    " (id INT NOT NULL AUTO_INCREMENT, name VARCHAR(45) NULL, PRIMARY KEY (id))"
cursor.execute(q)

cursor.execute("DROP TABLE IF EXISTS Archives.Department")
q = "CREATE TABLE archives.Department" \
    " ( id INT NOT NULL AUTO_INCREMENT,name VARCHAR(45) NULL, assetID INT  NULL," \
    " PRIMARY KEY (id)," \
    " FOREIGN KEY (assetID) REFERENCES archives.asset(id))"
cursor.execute(q)

cursor.execute("DROP TABLE IF EXISTS Archives.Project")
q = "CREATE TABLE archives.Project" \
    " ( id INT NOT NULL AUTO_INCREMENT, name VARCHAR(45) NULL, departmentID INT  NULL," \
    " PRIMARY KEY (id)," \
    " FOREIGN KEY (departmentID) REFERENCES archives.department(id))"

cursor.execute(q)

connection.close()