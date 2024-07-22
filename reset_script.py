from app import db
from models import User, Printer, NormalUserData, DSUUserData, RMScannerUserData

def reset_database(preserve_all=False):
    if preserve_all:
        users = User.query.all()
        printers = Printer.query.all()
        db.drop_all()
        db.create_all()
        for user in users:
            db.session.add(user)
        for printer in printers:
            db.session.add(printer)
    else:
        db.drop_all()
        db.create_all()
    db.session.commit()
