from types import StringTypes
from plstackapi.openstack.client import OpenStackClient
from plstackapi.openstack.driver import OpenStackDriver
from plstackapi.core.api.auth import auth_check
from plstackapi.core.models import Key, User
from plstackapi.core.api.users import _get_users


def _get_keys(filter):
    if isinstance(filter, StringTypes) and filter.isdigit():
        filter = int(filter)
    if isinstance(filter, int):
        keys = Key.objects.filter(id=filter)
    elif isinstance(filter, StringTypes):
        keys = Key.objects.filter(name=filter)
    elif isinstance(filter, dict):
        keys = Key.objects.filter(**filter)
    else:
        keys = []
    return keys 

def add_key(auth, fields):
    driver = OpenStackDriver(client = auth_check(auth))
    users = _get_users(fields.get('user')) 
    if users: fields['user'] = users[0]    
    key = Key(**fields)
    nova_fields = {'name': key.name,
                   'key': key.key} 
    nova_key = driver.create_keypair(**nova_fields)
    key.save()
    return key

def update_key(auth, id, **fields):
    return  

def delete_key(auth, filter={}):
    driver = OpenStackDriver(client = auth_check(auth))   
    keys = _get_keys(filter)
    for key in keys:
        driver.delete_keypair(name=key.name) 
        key.delete()
    return 1

def get_keys(auth, filter={}):
    client = auth_check(auth)
    keys = _get_keys(filter)
    return keys             
        

    