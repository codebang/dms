from utils import singleton
from utils import logger
from kazoo.protocol.states import KazooState
from kazoo.protocol.states import EventType
from kazoo.exceptions import NoNodeError
from user import User
import json
import os




def makewatch(account):
    def ipwatch(event):
        path = event.path
        ip = os.path.basename(path)
        accountId = os.path.basename(os.path.dirname(path))
        if event.type == EventType.DELETED:
            account.deleteip(ip)
            logger.info("account(%s)/ip(%s): is deleted,update the cache..." % (accountId,ip))
        elif event.type == EventType.CHANGED:
            logger.info("account(%s)/ip(%s): property updated, update the cache..." % (accountId,ip))
            account._syncip2usrfromzk(ip)
    return  ipwatch

class Account(object):
    def __init__(self,accountId,accountName,zk_path,zk_client):
        self.accountId = accountId
        self.accountName = accountName
        self.zkclient = zk_client
        self.zkpath = zk_path
        self.ip2user = {}
        self.watcher = makewatch(self)


    def getusrbyip(self,ip):
        """

        :param ip:
        :return:  User
        """
        if self.ip2user.has_key(ip):
            logger.debug("account(%s)/ip(%s): retrieve from cache...." % (self.accountId,ip))
            return self.ip2user(ip)
        else:
            logger.debug("account(%s)/ip(%s): retrieve from zookeeper..." % (self.accountId,ip))
            self._syncip2usrfromzk(ip)
            return self.ip2user.get(ip,None)

    def _syncip2usrfromzk(self,ip):

        if self.zkclient.state != KazooState.CONNECTED:
            self.zkclient.start()
        ip_path = os.path.join(self.zkpath,ip)
        try:
            data = self.zkclient.get(ip_path,watch=self.watcher)
            #map = json.loads(str(data))
            map = {}
            user = User(self.accountId,map)
            self.ip2user[ip] = user
        except NoNodeError:
            logger.error("account(%s)/ip(%s): miss in zookeeper,cannnot find..." % (self.accountId,ip))

    def getname(self):
        return self.accountName


    def deleteip(self,ip):
        self.ip2user.pop(ip,None)

@singleton
class AccountNone(object):

    def getusrbyip(self,ip):
        return None

    def getname(self):
        return None