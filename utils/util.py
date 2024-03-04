import json
import random

def success(data):
    return json.dumps({"message_code":"success","message":"request success", "data": data}), 200, {'ContentType':'application/json'}

def fail():
    return json.dumps({"message_code":"fail", "message":"Please check logs", "data": {}}), 400, {'ContentType':'application/json'}

def generate_pnr():
    return str(random.randrange(1, 10**14))

def formattrain(data):
    '''
    This method help to formate train data
    '''
    train_list = []
    for train in data:
        dt = {}
        dt["train_number"] = train.train_no
        dt["from_station"] = train.from_station
        dt["to_station"] = train.to_station
        dt["departure_time"] = str(train.departure_time)
        dt["arrival_time"] = str(train.arrival_time)
        if train.seat_count - train.book_count < 0:
            dt["available_seat"] = 0
            dt["waiting_list"] = train.book_count - train.seat_count
        else:
            dt["available_seat"] = train.seat_count - train.book_count
        train_list.append(dt)
    return train_list

def formattickets(data):
    '''
    This method help to formate tickets
    '''
    ticket_list = []
    for ticket in data:
        dt = {}
        dt["train_number"] = ticket.train_no
        dt["from_station"] = ticket.from_station
        dt["to_station"] = ticket.to_station
        dt["pnr"] = ticket.pnr
        dt["seat_no"] = ticket.seat_no
        dt["status"] = ticket.status
        dt["passenger_details"] = ticket.passenger_details
        ticket_list.append(dt)
    return ticket_list

    