from flask import Flask, request
from apps.train import *
from utils.request_validator import *
from utils.util import *

app = Flask(__name__)
app.config.from_pyfile('./config.py')

@app.route('/train', methods = ['GET','POST'])
def train():
    if request.method == 'POST':
        is_valid_req = trainvalidator(request.data)
        if is_valid_req:
            is_train_add = TrainOperation().add_train(is_valid_req) 
            return success(is_train_add) if is_train_add else fail()
        return fail()
    else:
        train_list = TrainOperation().get_trains()
        if train_list or type(train_list) == list:
            return success(train_list)
        return fail()

@app.route('/book', methods = ['POST'])
def book():
    is_valid_req = bookvalidator(request.data)
    if is_valid_req:
        is_ticket_book = BookOperation().book_ticket(is_valid_req)
        return success(is_ticket_book) if is_ticket_book else fail()
    return fail()

@app.route('/pnr/<string:pnr>/', methods = ['GET'])
def ticket(pnr):
    book_tickets = BookOperation().get_book_ticket(pnr)
    if book_tickets:
        return success(book_tickets) if book_tickets else fail()
    return fail()

@app.route('/cancel', methods = ['PUT'])
def cancel():
    is_valid_req = cancelvalidator(request.data)
    if is_valid_req:
        is_ticket_cancel = CancelOperation().cancel_ticket(is_valid_req)
        return success(is_ticket_cancel) if is_ticket_cancel else fail()
    return fail()

@app.route('/tatkal', methods = ['POST'])
def tatkal_book():
    is_valid_req = bookvalidator(request.data)
    if is_valid_req:
        is_ticket_book = BookOperation().tatkal_book_ticket(is_valid_req)
        return success(is_ticket_book) if is_ticket_book else fail()
    return fail()

if __name__ == '__main__':
    from model.schema import init_db
    # init_db()
    db.init_app(app)
    app.run(debug=True)
