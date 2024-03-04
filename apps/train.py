from model.schema import *
from datetime import datetime, timedelta
from utils.util import formattrain, generate_pnr, formattickets

class TrainOperation:
    def add_train(self, data=None):
        try:
            m_obj = Train()
            m_obj.train_no = data.get("train_no")
            m_obj.from_station = data.get("from_station")
            m_obj.to_station = data.get("to_station")
            m_obj.departure_time = datetime.utcnow() + timedelta(minutes=50)
            m_obj.arrival_time = datetime.utcnow() + timedelta(hours=5)
            m_obj.seat_count = data.get("seat_count")
            m_obj.total_seat = data.get("seat_count")
            m_obj.book_count = 0
            m_obj.created_at = datetime.utcnow()
            m_obj.updated_at = datetime.utcnow()
            db.session.add(m_obj)
            db.session.commit()
            print(f"Train successfully added:{data.get('train_no')}")
            return data
        except Exception as e:
            print(f"Error in add_train method:{e}")
            return None
        finally:
            db.session.close()
    
    def get_trains(self):
        try:
            return formattrain(db.session.query(Train).filter(Train.departure_time >= datetime.utcnow()).all())
        except Exception as e:
            print(f"Error in get_trains method:{e}")
            return None
        finally:
            db.session.close()

    def get_train_by_id(self, train_no):
        try:
            return db.session.query(Train).filter(Train.train_no == train_no).first()
        except Exception as e:
            print(f"Error in get_train_by_id method:{e}")
            return None
        finally:
            db.session.close()

class BookOperation:
    def prapare_ticket(self, data):
        no_of_passenger = data.get("passenger_details").get("names")
        book_ticketlist = []
        pnr = generate_pnr()

        train_obj = TrainOperation().get_train_by_id(data.get("train_no"))
        if train_obj and (train_obj.from_station == data.get("from_station") and train_obj.to_station == data.get("to_station")):
            train_no = train_obj.train_no
            seat_no = train_obj.book_count + 1
        else:
            print("Error in prapare_ticket method, Either train not found or station not found.")
            return None

        for name in no_of_passenger:
            m_obj = Book()
            m_obj.pnr = pnr
            m_obj.train_no = train_no
            m_obj.from_station = data.get("from_station")
            m_obj.to_station = data.get("to_station")
            m_obj.seat_no = seat_no 
            m_obj.status = "booked"
            m_obj.is_confirm = True if seat_no <= train_obj.seat_count else False
            m_obj.passenger_details = {"mobile": data.get("passenger_details").get("mobile"),"email": data.get("passenger_details").get("email"),"names":[name]}
            m_obj.created_at = datetime.utcnow()
            m_obj.updated_at = datetime.utcnow()
            book_ticketlist.append(m_obj)
            seat_no += 1
        return book_ticketlist

    def book_ticket(self, data=None):
        try:
            data_obj = self.prapare_ticket(data)
            if not data_obj:
                return None
            db.session.bulk_save_objects(data_obj)
            db.session.query(Train).filter(Train.train_no == data.get("train_no")).update({'seat_count': Train.seat_count - len(data_obj),"book_count":Train.book_count + len(data_obj)})
            db.session.commit()
            print(f"Ticket successfully booked")
            return data
        except Exception as e:
            print(f"Error in book_ticket method:{e}")
            return None
        finally:
            db.session.close()
    
    def get_book_ticket(self, pnr):
        return formattickets(db.session.query(Book).filter(Book.pnr == pnr).all())
    
    def tatkal_book_ticket(self, data):
        train_obj = db.session.query(Train).filter(datetime.utcnow()-timedelta(minutes=10) <= Train.departure_time).first()
        if train_obj:
            return self.book_ticket(data)
        return None
        

class CancelOperation:
    def is_valid_pnr(self, data):
        return db.session.query(Book).filter(Book.pnr == data.get("pnr")).all()

    def cancel_ticket(self, data=None):
        try:
            ticket_list = self.is_valid_pnr(data)
            ticket_ids = []
            train_no = ""

            for ticket in ticket_list:
                train_no = ticket.train_no
                if ticket.status == 'booked' and ticket.passenger_details["names"][0] in data.get("names"):
                    ticket_ids.append(ticket.id)
            if len(ticket_ids) != len(data.get("names")):
                print("Please provide valid ticket list to cancel")
                return None

            db.session.query(Book).filter(Book.id.in_(ticket_ids)).update({'status':'cancel'})
            db.session.commit()

            current_train = TrainOperation().get_train_by_id(train_no)
            if current_train.book_count > current_train.seat_count:
                db.session.query(Train).filter(Train.train_no == train_no).update({"book_count":Train.book_count - len(ticket_ids)})
            else:
                db.session.query(Train).filter(Train.train_no == train_no).update({'seat_count': Train.seat_count + len(ticket_ids),"book_count":Train.book_count - len(ticket_ids)})
    
            db.session.commit()
            print(f"Ticket successfully cancel")
            return data
        except Exception as e:
            print(f"Error in book_ticket method:{e}")
            db.session.rollback()
            return None
        finally:
            db.session.close()