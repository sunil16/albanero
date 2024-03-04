train_schema = {'train_no': {'type': 'string', 'required': True,}, 'from_station': {'type': 'string', 'required': True}, 'to_station': {'type': 'string', 'required': True}, 'seat_count': {'type': 'integer', 'required': True}}
ticket_schema = {
    'train_no': {'type': 'string', 'required': True,}, 
    'from_station': {'type': 'string', 'required': True}, 
    'to_station': {'type': 'string', 'required': True},
    'passenger_details': {'type': 'dict', 'required': True, "schema": {
        "mobile": {
            "type": "integer",
            "minlength": 10,
            "maxlength": 10,
            "regex": "^0[0-9]{9}$"
        },
        "email": {
            "type": "string",
            "minlength": 8,
            "maxlength": 255,
            "required": True,
            "regex": "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$"
        },
        "names":{'type': 'list'}
    }}
    }
cancel_ticket_schema = {'pnr': {'type': 'string', 'required': True,}, 'names': {'type': 'list', 'required': True}}

   
