from datetime import datetime

from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

from server.app import db
from ..main.models import get_user_by_id, get_client_by_id


class Incident(db.Model):
    __tablename__ = 'incidents'
    id = db.Column(db.Integer(), primary_key=True)
    subject = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    priority = db.Column(db.Integer(), default=1)
    criticality = db.Column(db.Integer(), default=1)
    status_id = db.Column(db.Integer, db.ForeignKey('request_statuses.id'), nullable=False, default=1)
    type_id = db.Column(db.Integer, db.ForeignKey('request_types.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    responsible_employee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, default=1)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    modified = db.Column(db.DateTime, default=datetime.utcnow)

    status = db.relationship("RequestStatus", foreign_keys=[status_id])
    type = db.relationship("RequestType", foreign_keys=[type_id])
    responsible_employee = db.relationship("User", foreign_keys=[responsible_employee_id])

    @hybrid_property
    def creator_id(self):
        return self.employee_id or self.client_id

    @hybrid_property
    def creator(self):
        if self.employee_id:
            return get_user_by_id(self.employee_id)
        return get_client_by_id(self.client_id)

    def add(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()


class RequestStatus(db.Model):
    __tablename__ = 'request_statuses'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)

    def __repr__(self):
        return self.name


class RequestType(db.Model):
    __tablename__ = 'request_types'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)

    def __repr__(self):
        return self.name
