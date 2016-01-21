from .. domain import Service
from .. domain.model import Basic
from .. domain import Tenant
from .. sm.service import create_svc_sm
class EventFactory(type):

    meta_data = {}

    def __init__(cls,classname,bases,dict_):
        type.__init__(cls,classname,bases,dict_)
        if 'register' not in cls.__dict__:
            cls.meta_data[classname] = cls
        print cls.meta_data

    @classmethod
    def getEvent(cls,name,map):
        return cls.meta_data[name](map)


class_dict = dict(register=True)

Event = EventFactory("Event",(object,),class_dict)



class PACKAGE_ACTIVATE(Event):
    def __init__(self,map):
        self.topic = map["topic"]
        self.packageName = map["packageName"]
        self.accountId = map["accountId"]
        self.eventName = map["eventName"]

class CREATE_VM(Event):
    def __init__(self,map):
        meta_props = ["eventName","topic","accountId","stackId","vmType","vmManagementIP","vmPublicIP","vmServiceIP"]
        for prop in meta_props:
            setattr(self,prop,map[prop])

