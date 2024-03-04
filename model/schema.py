from app import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from datetime import date, datetime, timedelta

db = SQLAlchemy(app)

class Train(db.Model):
    '''
    Train class model 
    '''
    __tablename__ = 'train'
    id = db.Column(db.Integer,autoincrement=True)
    train_no = db.Column(db.String(500), primary_key=True)
    from_station = db.Column(db.String(500))
    to_station = db.Column(db.String(500))
    seat_count = db.Column(db.Integer)
    total_seat = db.Column(db.Integer)
    book_count = db.Column(db.Integer)
    departure_time = db.Column(db.DateTime, default=datetime.utcnow())
    arrival_time = db.Column(db.DateTime, default=datetime.utcnow())
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())
    book = db.relationship('Book', backref='train')

class Book(db.Model):
    '''
    Ticket book model 
    '''
    __tablename__ = 'book'
    id = db.Column(db.Integer,autoincrement=True, primary_key=True)
    pnr = db.Column(db.String(500))
    from_station = db.Column(db.String(500))
    to_station = db.Column(db.String(500))
    seat_no = db.Column(db.Integer)
    status =  db.Column(db.String(500))
    is_confirm =  db.Column(db.Boolean)
    passenger_details = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())
    train_no = db.Column(db.String, db.ForeignKey('train.train_no'))
    
def init_db():
    '''
    Creating table by model object
    '''
    with app.app_context():
        db.create_all()
    print("Database created")

def get_db_obj():
    return db