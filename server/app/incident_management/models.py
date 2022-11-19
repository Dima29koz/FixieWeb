from datetime import datetime

from server.app import db


class Incident(db.Model):
    __tablename__ = 'incidents'
    id = db.Column(db.Integer(), primary_key=True)
    subject = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    priority = db.Column(db.Integer(), default=1)
    criticality = db.Column(db.Integer(), default=1)
    status_id = db.Column(db.Integer, db.ForeignKey('request_statuses.id'), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('request_types.id'), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    responsible_employee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    modified = db.Column(db.DateTime, default=datetime.utcnow)

    status = db.relationship("RequestStatus", foreign_keys=[status_id])
    type = db.relationship("RequestType", foreign_keys=[type_id])
    creator = db.relationship("User", foreign_keys=[creator_id])
    responsible_employee = db.relationship("User", foreign_keys=[responsible_employee_id])


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
