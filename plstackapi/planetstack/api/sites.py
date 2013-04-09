from plstackapi.openstack.client import OpenStackClient
from plstackapi.openstack.driver import OpenStackDriver
from plstackapi.planetstack.api.auth import auth_check
from plstackapi.planetstack.models import Site
 

def add_site(auth, **fields):
    driver = OpenStackDriver(client = auth_check(auth))
    site = Site(**fields)
    nova_fields = {'tenant_name': fields['login_base'],
                   'description': fields['name'],
                   'enabled': fields['enabled']}    
    tenant = driver.create_tenant(**nova_fields)
    site.tenant_id=tenant.id
    site.save()
    return role

def update_site(auth, tenant_id, **fields):
    driver = OpenStackDriver(client = auth_check(auth))
    sites = Site.objects.filter(tenant_id=tenant_id)
    if not sites:
        return

    site = Site[0]
    nova_fields = {}
    if 'description' in fields:
        nova_fields['description'] = fields['name']
    if 'enabled' in fields:
        nova_fields['enabled'] = fields['enabled']

    site.updtae(**fields)
    return site 

def delete_site(auth, filter={}):
    driver = OpenStackDriver(client = auth_check(auth))   
    sites = Site.objects.filter(**filter)
    for site in sites:
        driver.delete_tenant({'id': site.tenant_id}) 
        site.delete()
    return 1

def get_sites(auth, filter={}):
    client = auth_check(auth)
    sites = Site.objects.filter(**filter)
    return sites             
        

    