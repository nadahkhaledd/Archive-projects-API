import pymysql
from app import app
from config import db
from flask import jsonify
from flask import flash, request

@app.route('/')
def start():
    return getAll()

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone


@app.route('/archive', methods=['GET'])
def getAll():
    connection = db.connect()
    cursor = connection.cursor()
    try:
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SET FOREIGN_KEY_CHECKS=0")
        cursor.execute("SELECT archives.project.id AS projectID, archives.project.name AS projectName,"
                       "archives.department.id AS departmentID, archives.department.name AS departmentName,"
                       " archives.department.assetID AS assetID, archives.asset.name AS assetName"
                       " FROM Archives.department"
                       " JOIN Archives.project ON  archives.project.departmentID = archives.department.id "
                       "JOIN Archives.asset ON archives.department.assetID = archives.asset.id")
        data = cursor.fetchall()
        response = jsonify(data)

        response.status_code = 200
        return response
    except Exception as e:
        print(e)

    finally:
        cursor.close()
        connection.close()


@app.route('/archive/<int:id>', methods=['GET'])
def getByID(id):
    connection = db.connect()
    cursor = connection.cursor()
    try:
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SET FOREIGN_KEY_CHECKS=0")
        cursor.execute("SELECT archives.project.id AS projectID, archives.project.name AS projectName,"
                       "archives.department.id AS departmentID, archives.department.name AS departmentName,"
                       " archives.department.assetID AS assetID, archives.asset.name AS assetName"
                       " FROM Archives.Project"
                       " JOIN Archives.department ON  archives.project.departmentID = archives.department.id "
                       "JOIN Archives.asset ON archives.department.assetID = archives.asset.id"
                       " WHERE archives.project.id = %s", id)
        data = cursor.fetchone()
        response = jsonify(data)

        response.status_code = 200
        return response
    except Exception as e:
        print(e)

    finally:
        cursor.close()
        connection.close()


@app.route('/archive/post', methods=['POST'])
def post():
    connection = db.connect()
    cursor = connection.cursor()
    try:
        _json = request.json
        _name = _json['name']
        _departmentID = _json['departmentID']
        _departmentName = _json['department']['name']
        _assetID = _json['department']['assetID']
        _assetName = _json['department']['asset']['name']
        cursor.execute("SET FOREIGN_KEY_CHECKS=0")
        if _name and _departmentID and _departmentName and _assetID and _assetName and request.method == 'POST':
            sqlQuery = "INSERT INTO archives.project(name, departmentID) VALUES(%s, %s)"
            bindData = (_name, _departmentID)
            cursor.execute(sqlQuery, bindData)

            sqlQuery = "INSERT INTO archives.department(name, assetID) VALUES(%s, %s)"
            bindData = (_departmentName, _assetID)
            cursor.execute(sqlQuery, bindData)

            sqlQuery = "INSERT INTO archives.asset(name) VALUES(%s)"
            bindData = _assetName
            cursor.execute(sqlQuery, bindData)

            connection.commit()

            response = jsonify('project added successfully!')
            response.status_code = 200
            return response
        else:
            return not_found()
    except Exception as e:
        print(e)

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    app.debug = True
    app.run()