import numpy
import os
import factory
from lib.utils import singleton

from ostruct import OpenStruct


class Package(object):

    def getVMList(self):
        return self.vmlist

    #{vm:[vm,vm]}
    def getNeighbor(self):
        return None

    def getreadystatus(self):
        vmlist = self.getVMList()
        temp = 1
        for vm in vmlist:
            temp = temp | vm.getStatusCode()
        return temp

    def change(self,package):
        newvmlist = package.getVMList()
        newneighbors = package.getNeighbor()

        origvmlist = self.getVMList()
        origneighbors = self.getNeighbor()

        ret = {}
        for vm in origvmlist:
            #vm deleted
            if not newneighbors.has_key(vm):
                ret[vm] = {"state": "delete"}
            elif numpy.array_equal(origneighbors[vm],newneighbors[vm]):
                ret[vm] = {'state':'unchange'}
            else:
                ret[vm] = {'state':'change','neighbor':newneighbors[vm]}

        for vm in newvmlist:
            if not ret.has_key(vm):
                ret[vm] = {'state':'new','neighbor':newneighbors[vm]}

        return ret







@singleton
class Firewall(object):
    def __init__(self):
        self.type = "firewall"
        self.os = "fedora"

    def getStatusCode(self):
        return 1;


@singleton
class VRouter(object):

    def __init__(self):
        self.type = "vrouter"
        self.os = "centos"

    def getStatusCode(self):
        return 2;

@singleton
class IPsec(object):
    def __init__(self):
        self.type = "ipsec"
        self.os = "ubuntu"
    def getStatusCode(self):
        return 4;

@singleton
class DNS(object):
    def __init__(self):
        self.type = "dns"
        self.os = "ubuntu"

    def getStatusCode(self):
        return 8;

def getNodeTypeFromName(name):
    return {
        "vrouter": VRouter(),
        "firewall": Firewall(),
        "ipsec": IPsec(),
        "dns": DNS()
    }[name]

class Basic(Package):

    def __init__(self):
        self.vmlist = []
        self.fw = Firewall()
        self.vr = VRouter()
        self.ipsec = IPsec()
        self.vmlist.append(self.fw)
        self.vmlist.append(self.vr)
        self.vmlist.append(self.ipsec)

    def getNeighbor(self):
        """

        :rtype: object
        """
        return {
            self.vr: [self.fw,self.ipsec],
            self.fw: [self.vr],
            self.ipsec: [self.vr]
        }

class BasicVPN(Basic):
    def __init__(self):
        Basic.__init__()
        self.vpn = DNS()

    def getNeighbor(self):
        return {
            self.vr: [self.fw,self.ipsec],
            self.fw: [self.vr],
            self.ipsec: [self.vr],
            self.vpn: [self.vr]
        }


if __name__ == '__main__':
    serivce = OpenStruct()
    nodes = []
    fakes = [("firewall","10.74.125.196"),("vrouter","10.74.124.195"),("ipsec","10.74.125.194")]
    for data in fakes:
        node = OpenStruct()
        node.vmtype = data[0]
        node.manageip = data[1]
        node.accountName = "haoyan"
        nodes.append(node)
    serivce.nodes = nodes