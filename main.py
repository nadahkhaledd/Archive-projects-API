from string import Template

import pymysql
from app import app
from components.models import Project, Department, Asset
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
        hold = [data]
        newData = toJson(hold)
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
        _departmentName = _json['department']['name']
        _assetName = _json['department']['asset']['name']
        cursor.execute("SET FOREIGN_KEY_CHECKS=0")
        if _name and _departmentName and _assetName and request.method == 'POST':
            sqlQuery = "INSERT INTO archives.asset(name) VALUES(%s)"
            bindData = _assetName
            cursor.execute(sqlQuery, bindData)
            cursor.execute("SELECT archives.asset.id  FROM archives.asset WHERE archives.asset.name = %s", _assetName)
            _assetID = cursor.fetchone()
            _assetID = _assetID[0]

            sqlQuery = "INSERT INTO archives.department(name, assetID) VALUES(%s, %s)"
            bindData = (_departmentName, int(_assetID))
            cursor.execute(sqlQuery, bindData)
            cursor.execute("SELECT archives.department.id  FROM archives.department WHERE archives.department.name = %s", _departmentName)
            _departmentID = cursor.fetchone()
            _departmentID = _departmentID[0]

            sqlQuery = "INSERT INTO archives.project(name, departmentID) VALUES(%s, %s)"
            bindData = (_name, int(_departmentID))
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


@app.route('/archive/create/', methods=['POST'])
def create():

    try:
        _json = request.json
        _id = _json['id']
        return getByID(_id)

    except Exception as e:
        print(e)


@app.route('/archive/replicate/',  methods=['POST'])
def replicate():
    try:
        response = post()
        if response.status_code == 200:
            return getAll()

    except Exception as e:
        print(e)


if __name__ == "__main__":
    app.debug = True
    app.run()
