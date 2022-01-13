from flask import Flask, jsonify, request
from components.models import Project, Department, Asset, db
from components.schemas import ProjectSchema, DepartmentSchema, AssetSchema


def get(id=None):
    """
    get Projects
    """
    try:
        if id is None:
            project = Project.query.filter().all()
            projectSchema = ProjectSchema(many=True)
            return projectSchema.jsonify(project)
        else:
            project = Project.query.filter_by(id=id).first()
            projectSchema = ProjectSchema()
            return projectSchema.jsonify(project)

    except Exception as e:
        jsonify({"error": "There was an error connecting to database"})


def post():
    """
    Add project
    """
    data = request.get_json()
    try:
        project = Project(**data)
        projectSchema = ProjectSchema()
        db.session.add(project)
        db.session.commit()
        return projectSchema.jsonify(project)
    except Exception as e:
        print(e)
        jsonify({"error": "There was an error connecting to database"})


def put(id):
    """
    Update project
    """
    try:

        data = request.get_json()
        project = Project.query.filter_by(id=id).first()
        project = Project.query.filter_by(id=id)
        project.update(data)
        db.session.commit()

        return jsonify(data)
    except Exception as e:
        jsonify({"error": "There was an error connecting to database"})


def delete(id):
    """
    Delete project
    """
    try:

        data = request.get_json()
        project = Project.query.filter_by(id=id).first()
        project = Project.query.filter_by(id=id)
        project.delete(data)
        db.session.commit()

        return jsonify(data)
    except Exception as e:
        jsonify({"error": "There was an error connecting to database"})
