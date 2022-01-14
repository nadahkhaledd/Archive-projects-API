import pymysql
from app import app
from components.models import Project, Department, Asset
from config import db
from flask import jsonify
from flask import flash, request
import json


@app.route('/')
def start():
    return getAll()


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    response = jsonify(message)
    response.status_code = 404
    return response


def toJson(data):
    projects = []
    newData = []
    for archive in data:
        p = Project()
        d = Department()
        a = Asset()
        a.fromJson(archive['asset.id'], archive['asset.name'])
        d.fromJson(archive['department.id'], archive['department.name'], a)
        p.fromJson(archive['id'], archive['name'], d)
        projects.append(p)

    for pr in projects:
        newProject = dict({'id': pr.id, 'name': pr.name,
                           'department': {'id': pr.department.id, 'name': pr.department.name,
                                          'asset': {'id': pr.department.asset.id, 'name': pr.department.asset.name}}})
        newData.append(newProject)

    return newData


@app.route('/archive', methods=['GET'])
def getAll():
    connection = db.connect()
    cursor = connection.cursor()
    try:
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SET FOREIGN_KEY_CHECKS=0")
        cursor.execute("SELECT Archives.project.*, Archives.department.*, Archives.asset.*"
                       " FROM Archives.department"
                       " JOIN Archives.project ON  archives.project.departmentID = archives.department.id "
                       "JOIN Archives.asset ON archives.department.assetID = archives.asset.id")

        data = cursor.fetchall()
        newData = toJson(data)
        response = jsonify(newData)

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
        cursor.execute("SELECT Archives.project.*, Archives.department.*, Archives.asset.*"
                       " FROM Archives.department"
                       " JOIN Archives.project ON  archives.project.departmentID = archives.department.id "
                       "JOIN Archives.asset ON archives.department.assetID = archives.asset.id"
                       " WHERE archives.project.id = %s", id)

        data = cursor.fetchone()
        newData = toJson([data])
        response = jsonify(newData)

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
