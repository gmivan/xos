from plstackapi.openstack.client import OpenStackClient
from plstackapi.openstack.driver import OpenStackDriver
from plstackapi.core.api.auth import auth_check
from plstackapi.core.models import Key, User
 
def lookup_user(fields):
    user = None
    if 'user' in fields:
        if isinstance(fields['user'], int):
            users = User.objects.filter(id=fields['user'])
        else:
            users = User.objects.filter(email=fields['user'])
        if users:
            user = users[0]
    if not user:
        raise Exception, "No such user: %s" % fields['user']
    return user 

def add_key(auth, fields):
    driver = OpenStackDriver(client = auth_check(auth))
    user = lookup_user(fields) 
    if user: fields['user'] = user     
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
    keys = Key.objects.filter(**filter)
    for key in keys:
        driver.delete_keypair(name=key.name) 
        key.delete()
    return 1

def get_keys(auth, filter={}):
    client = auth_check(auth)
    keys = Key.objects.filter(**filter)
    return keys             
        

    
