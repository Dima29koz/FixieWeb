from datetime import datetime

from server.app import db


service_relations = db.Table(
    'service_relations',
    db.Column('main_service_id', db.Integer, db.ForeignKey('services.id'), primary_key=True),
    db.Column('related_service_id', db.Integer, db.ForeignKey('services.id'), primary_key=True)
)


class Service(db.Model):
    def __init__(self,
                 name,
                 description):
        self.name = name
        self.description = description
        self.add()

    __tablename__ = 'services'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.Text(), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    modified = db.Column(db.DateTime, default=datetime.utcnow)

    main_services = db.relationship(
        "Service",
        secondary='service_relations',
        primaryjoin=id == service_relations.c.related_service_id,
        secondaryjoin=id == service_relations.c.main_service_id,
        backref=db.backref('related_services'),
        lazy=True)

    def add(self):
        """added message to DB"""
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'description': self.description,
            'timestamp': f'{self.timestamp.isoformat()}Z',
        }

    def __repr__(self):
        return self.name


def get_service_by_id(service_id: int) -> Service | None:
    return Service.query.filter_by(id=service_id).first()


def get_service_by_name(service_name: str) -> Service | None:
    return Service.query.filter_by(name=service_name).first()
