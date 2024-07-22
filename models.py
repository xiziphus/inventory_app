from app import db
from flask_login import UserMixin
from datetime import datetime

# Association table for many-to-many relationship between users and printers
user_printer = db.Table('user_printer',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('printer_id', db.Integer, db.ForeignKey('printer.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    printers = db.relationship('Printer', secondary=user_printer, backref=db.backref('users', lazy=True))

class Printer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)

class NormalUserData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    barcode = db.Column(db.String(150), nullable=False)
    pallet_number = db.Column(db.String(150), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class DSUUserData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    barcode = db.Column(db.String(150), nullable=False)
    pallet_number = db.Column(db.String(150), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class RMScannerUserData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    bobbin_number = db.Column(db.String(150), nullable=False)
    bobbin_type = db.Column(db.String(150), nullable=False)
    bobbin_size = db.Column(db.String(150), nullable=False)
    cu_size = db.Column(db.String(150), nullable=False)
    drawn_bunched = db.Column(db.String(150), nullable=False)
    weight_kg = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
