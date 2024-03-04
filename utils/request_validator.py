from cerberus import Validator
from utils.req_schema import *
import json

def validator(schema, document):
    '''
    This validator help to validate request json.
    '''
    v = Validator(schema)
    if v.validate(document):
        print(f'req data is valid: {document}')
        return True
    else:

        print(f'req invalid data: {v.errors}')
        return False

def trainvalidator(document):
    '''
    This method help to validate add train api
    '''
    document = json.loads(document)
    return document if validator(train_schema,document) else False

def bookvalidator(document):
    '''
    This method help to validate ticket details
    '''
    document = json.loads(document)
    return document if validator(ticket_schema,document) else False

def cancelvalidator(document):
    '''
    This method help to validate ticket details
    '''
    document = json.loads(document)
    return document if validator(cancel_ticket_schema,document) else False


