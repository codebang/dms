from fysom import Fysom
import lib.domain
from lib.sm import *
from sqlalchemy.sql import exists
from .. domain.model import getNodeTypeFromName
from .. domain.model import Basic
from .. domain.jobbuilder import JobBuilder
from .. rundeck.client import Rundeck
def create_svc_sm(state="init"):
    print "create"
    sm = Fysom({'initial': state,
                'events':[
                {'name':'package_activate','src':"init",'dst':'provisioning'},
                {'name':'create_vm_firewall','src':['provisioning','vpn_created','ipsec_created','vrouter_created','dns_created'],'dst':'firewall_created'},
                {'name':'create_vm_vrouter','src':['provisioning','vpn_created','ipsec_created','firewall_created','dns_created'],'dst':'vrouter_created'},
                {'name':'create_vm_ipsec','src':['provisioning','vpn_created','firewall_created','vrouter_created','dns_created'],'dst':'ipsec_created'},
                {'name':'create_vm_dns','src':['provisioning','vpn_created','ipsec_created','vrouter_created','firewall_created'],'dst':'dns_created'},
                {'name':'create_vm_done','src':['firewall_created','vrouter_created','ipsec_created','dns_created'],'dst':'monitor_cpe'},
                {'name': 'monitor_cpe_done','src': 'monitor_cpe', 'dst': 'job_schedule'}
                ],
                'callbacks': {
                 'onprovisioning': onprovisioning,
                 'onfirewall_created': onnodecreated,
                 'onvpn_created': onnodecreated,
                 'onipsec_created': onnodecreated,
                 'ondns_created': onnodecreated,
                 'onvrouter_created': onnodecreated,
                 'onmonitor_cpe': onmonitor_cpe,
                 'onjob_schedule': onjobschedule
                }})
    return sm

#prevent reenter the state when loading from db
def guard(func):
    def _handler(e):
        if e.src == "none":
            return
        else:
            func(e)
    return _handler

@guard
def onprovisioning(e):
    svc = e.service
    session = e.session

    res = session.query(lib.domain.Tenant).filter(lib.domain.Tenant.id == svc.tenantId).all()

    if len(res) == 0:
        tenant = lib.domain.Tenant()
        tenant.id = svc.tenantId
        tenant.name = "haoyan"
        session.add(tenant)
    svc.state = "provisioning"
    session.add(svc)
    session.commit()

@guard
def onnodecreated(e):
    print "enter node created"
    session = e.session
    node = e.node
    service = e.service
    status_code = getNodeTypeFromName(node.vmtype).getStatusCode()
    if service.status is None:
        service.status = status_code
    else:
        service.status = service.status | status_code
    session.add(node)
    service.state = "%s_created" % node.vmtype
    session.commit()
    if service.status == service.readystatus:
        service.getSM().trigger("create_vm_done",session = session, service = service)

def onmonitorcpe(e):
    service = e.service
    job = JobBuilder.buildmonitorcpejob(service)
    rundeck_client = Rundeck()
    runjob(rundeck_client,job)

def onjobschedule(e):
    service = e.service
    jobs = JobBuilder.buildsaenablejobs(service)
    rundeck_client = Rundeck()
    for job in jobs:
        runjob(rundeck_client,job)

def runjob(rundeck_client, job):
    rundeck_reponse = rundeck_client.import_job(job.to_xml,fmt = "xml", dupeOption = "create" , project = "dms-sa", uuidOption = "remove")
    message = rundeck_reponse.message
    uuid = ""
    rundeck_client.run_job(job)



