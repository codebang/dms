from lib.base.handlebase import HandleBase
from pydispatch import dispatcher
from lib.services.servicecontext import ServiceContext
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from lib.domain import Service
from lib.domain import Node
from lib.utils import register
from lib.domain.model import Basic

class ServiceHandler(HandleBase):
    def getPluginName(self):
        return "service_handler"

    def run(self):
        self._initializeSession()
        ctx = ServiceContext()
        queue = ctx.getQueueService()
        while(True):
            event = queue.get()
            print event.eventName
            dispatcher.send(signal=event.eventName,sender=event,session=self.session)


    def _initializeSession(self):
        db_url = self.connect_url
        engine = create_engine(db_url)
        self.sessionmaker = sessionmaker(bind=engine)
        self.session = self.sessionmaker()

@register
def handleCreate_VM(*args,**kwargs):
    event = kwargs["sender"]
    session = kwargs["session"]
    service = session.query(Service).filter(Service.tenantId == event.accountId).one()
    print service
    node = Node()
    node.stackid = event.stackId
    node.vmtype = event.vmType
    node.manageip = event.vmManagementIP
    node.publicip = event.vmPublicIP
    node.serviceip = event.vmServiceIP
    node.serviceid = service.id
    node.hostname = "just for test"
    print "create_vm_%s" % node.vmtype
    print service.getSM().current
    service.getSM().trigger("create_vm_%s" % node.vmtype, node = node, service = service,session = session)

@register
def handlePackage_Activate(*args,**kwargs):
    event = kwargs["sender"]
    session = kwargs["session"]
    service = Service()
    package = None
    if len(event.packageName) == 1 and event.packageName[0] == "basic":
        package = Basic()
    service.packageName = str(event.packageName)
    service.packageId = 1
    service.state = "init"
    service.readystatus = package.getreadystatus()
    service.tenantId = event.accountId
    service.getSM().package_activate(session=session,service=service)

