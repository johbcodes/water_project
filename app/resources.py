from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import Project, db

class ProjectResource(Resource):
    @jwt_required()
    def get(self, project_id):
        project = Project.query.get_or_404(project_id)
        return {
            'ProjectID': project.ProjectID,
            'ProjectName': project.ProjectName,
            'County': project.county.CountyName,
            'Constituency': project.constituency.ConstituencyName,
            'Ward': project.ward.WardName,
            'ProgressPercentage': project.ProgressPercentage
        }

    @jwt_required()
    def post(self):
        data = request.get_json()
        new_project = Project(
            ProjectName=data['ProjectName'],
            CountyID=data['CountyID'],
            ConstituencyID=data['ConstituencyID'],
            WardID=data['WardID'],
            ProgressPercentage=data['ProgressPercentage']
        )
        db.session.add(new_project)
        db.session.commit()
        return {'message': 'Project created successfully'}, 201

    @jwt_required()
    def put(self, project_id):
        project = Project.query.get_or_404(project_id)
        data = request.get_json()
        project.ProjectName = data.get('ProjectName', project.ProjectName)
        project.CountyID = data.get('CountyID', project.CountyID)
        project.ConstituencyID = data.get('ConstituencyID', project.ConstituencyID)
        project.WardID = data.get('WardID', project.WardID)
        project.ProgressPercentage = data.get('ProgressPercentage', project.ProgressPercentage)
        db.session.commit()
        return {'message': 'Project updated successfully'}

    @jwt_required()
    def delete(self, project_id):
        project = Project.query.get_or_404(project_id)
        db.session.delete(project)
        db.session.commit()
        return {'message': 'Project deleted successfully'}
