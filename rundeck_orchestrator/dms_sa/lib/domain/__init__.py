from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Column, Integer, String, DateTime,ForeignKey
from sqlalchemy import func
from sqlalchemy.orm import relationship
from sqlalchemy import Sequence
from sqlalchemy import create_engine
import lib.sm.service
Base = declarative_base()

class TableNameConvention(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

class TimestampMixin(object):
    created_at = Column(DateTime, default=func.now())


class Tenant(TableNameConvention,Base):
    """
        Tenant - Service: one - to many
    """
    id = Column(String(100),primary_key=True)
    name = Column(String(100))

    services = relationship("Service",back_populates="tenant")




class Service(TableNameConvention,TimestampMixin,Base):
    """
        service - node: one - to - many
        service - package: one - to - many
    """
    id = Column(Integer, Sequence('service_id_seq'), primary_key=True)
    tenantId = Column(String(100),ForeignKey('tenant.id'))
    packageId = Column(String(100))
    packageName = Column(String(20))
    state = Column(String(20))
    status = Column(Integer)
    readystatus = Column(Integer)
    updatetime  = Column(DateTime)

    nodes = relationship("Node",back_populates="service")
    tenant = relationship("Tenant",back_populates="services")

    def getSM(self):
        if not hasattr(self,"sm"):
           self.sm = lib.sm.service.create_svc_sm(state=self.state)
        return self.sm


class Node(TableNameConvention,TimestampMixin,Base):
    serviceid = Column(Integer,ForeignKey('service.id'))
    stackid = Column(String(100),primary_key=True)
    hostname = Column(String(100))
    vmtype = Column(String(50))
    manageip = Column(String(30))
    serviceip = Column(String(30),nullable=True)
    publicip = Column(String(30))
    updatetime = Column(DateTime)

    service = relationship("Service",back_populates="nodes")









#Local Test
if __name__ == '__main__':
  print 'hello'
  print Tenant.__table__

  connect_url = "mysql+mysqldb://root:cisco123@127.0.0.1/dms"
  engine = create_engine(connect_url)

  Base.metadata.create_all(engine)
