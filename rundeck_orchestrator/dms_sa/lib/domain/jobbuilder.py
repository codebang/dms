from model import Basic
from model import getNodeTypeFromName
import factory
from job import Job

class JobBuilder:
    @classmethod
    def buildmonitorcpejob(cls,service):
        pass

    @classmethod
    def buildsaenablejobs(cls,service):
        nodes = service.nodes
        context = cls._buildcontext(nodes)
        jobs = []
        for node in nodes:
            job = Job()
            job.setName(cls._buildjobname(node,"PACKAGE_ACTIVATE"))
            job.setNodeFilter(node.manageip)
            WF= factory.NodeFactory.createfactory(node.vmtype).createWFBuilder("PACKAGE_ACTIVATE",context).buildWF()
            for step in WF:
                step.join(job)
            jobs.append(job)
        return jobs


    @classmethod
    def _buildcontext(cls,nodes):
        nodemap= {}
        ctxmap = {}
        for node in nodes:
            nodemap[node.vmtype] = node
        package = Basic()
        neighbormap = package.getNeighbor()
        for node in nodes:
            nodetype = getNodeTypeFromName(node.vmtype)
            neighbors = neighbormap[nodetype]
            neighbor = []
            for nb in neighbors:
                nbnode = nodemap[nb.type]
                neighbor.append(nbnode.manageip)
            ctx = {}
            nb = ",".join(neighbor)
            ctx["neigbhor"] = nb
            ctx["internal_node_home"] = os.path.join("/tmp/rundeck",node.accountName,node.vmtype)
            ctxmap[node.vmtype] = ctx

        return ctxmap

    @classmethod
    def _buildjobname(cls,node,event):
        return node.accountName + "@" + node.manageip + "@" + event