from kazoo.client import KazooClient
from kazoo.protocol.states import KazooState
import os
from ConfigParser import SafeConfigParser
import time
from utils import logger

from utils import singleton
from domain.account import Account
from domain.account import AccountNone

from kazoo.protocol.states import EventType
from kazoo.exceptions import NoNodeError
from kazoo.recipe.watchers import DataWatch

import traceback

def makewatcher(inventory):
    def accountwatcher(event):
        path = event.path
        accountId = os.path.basename(path)
        if event.type == EventType.DELETED:
            inventory.deleteaccount(accountId)
            logger.info("account(%s) is deleted,update the cache." % accountId)
            print inventory.aimap

    return accountwatcher

@singleton
class DMSInventory(object):
    IP2USR_PATH = "/dso/Mapping/Ip2User"
    def __init__(self):
        self._initconfig()
        self.zk = KazooClient(hosts=self.config.get("default","zk_address"))
        #accounid -> account
        self.aidmap = {}
        self.watcher = makewatcher(self)

    def _initconfig(self):
        self.config = SafeConfigParser()
        config_file = os.path.join(os.path.dirname(__file__),"config.conf")
        self.config.read(config_file)
    def getusrbyip(self,accountId,ip):
        return self.getaccount(accountId).getusrbyip(ip)

    def getnamebyaid(self,accountId):
        return self.getaccount(accountId).getname()

    def getaccount(self,accountid):
        if not self.aidmap.has_key(accountid):
            logger.info("account(%s) is not in cache,just sync from zookeeper..." % accountid)
            self._syncaccount(accountid)
        return self.aidmap.get(accountid,AccountNone())


    def _syncaccount(self,accountId):
        if self.zk.state != KazooState.CONNECTED:
            self.zk.start(timeout=15)
        acc_path = os.path.join(self.IP2USR_PATH,accountId)
        try:
            value,zodestat = self.zk.get(acc_path,watch=self.watcher)
            account = Account(accountId,value,acc_path,zk_client=self.zk)
            self.aidmap[accountId] = account
        except NoNodeError:
            logger.error("node (%s) can not be found from zookeeper." % (accountId))
        print self.aidmap

    def deleteaccount(self,accountId):
        self.aidmap.pop(accountId)


    def stop(self):
        try:
            self.zk.stop()
        except Exception,e:
            logger.warn("close zookeeper occur exception....")

if __name__ == '__main__':


    inventory = DMSInventory()
    inventory.getnamebyaid("123")
    inventory.stop()
   # print inventory.getnamebyaid("07abd683-8b4b-4d1a-ae26-3552fc2b679a")
#    print inventory.getusrbyip("07abd683-8b4b-4d1a-ae26-3552fc2b679a","10.5.4.78")
    time.sleep(500)