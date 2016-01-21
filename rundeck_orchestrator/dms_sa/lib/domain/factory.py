import os
from jinja2 import FileSystemLoader,Environment


class WorkflowStep(object):
    pass

class CopyFileStep(WorkflowStep):
    def __init__(self,src,dst):
        self.src = src
        self.dst = dst

    def join(self,job):
        job.addcopyfile(self,self.src,self.dst)

class ExecuteCommandStep(WorkflowStep):
    def __init__(self,command):
        self.cmd = command

    def join(self,job):
        job.addcommand(self.cmd)

class NodeFactory:
    @classmethod
    def createfactory(cls,name):
        if name == "vrouter":
            return VRouterWFFactory()
        elif name == "firewall":
            return FirewallWFFactory()
        elif name == "vpn":
            return VPNWFFactory()
        elif name == "dns":
            return DNSWFFactory()
        return NodeWFFactory()


class NodeWFFactory(object):
    def createWFBuilder(self,type,context):
        return ServiceActivateWFBuilder(context)



class WFBuilder(object):
    def __init__(self,context):
        self.ctx = context

    DOMAIN_HOME = os.path.abspath(__file__)
    LOADER = FileSystemLoader(DOMAIN_HOME,"collectd")
    ENV = Environment(loader = LOADER)

    def initcopy(self):
        return []

    def initexecute(self):
        return []

    def getcopyfile(self):
        return []

    def _copyfiles(self):
        steps = []
        for file,destination in self.getcopyfile():
            if file.endswith("j2"):
                tp_file = self.ENV.get_template(file)
                homepath = self.ctx["internal_node_home"]
                if not os.path.exists(homepath):
                    os.makedirs(homepath)
                dest_file = file[-3:]
                dest_path = os.path.join(homepath,dest_file)
                config = tp_file.render(self.ctx)
                if os.path.exists(dest_path):
                    os.remove(dest_path)
                with open(dest_path,"w+") as f:
                    f.write(config)
                steps.append(CopyFileStep(dest_path,destination))
            else:
                src_file = os.path.join(self.DOMAIN_HOME,"scripts",file)
                steps.append(CopyFileStep(dest_path,destination))
        return steps

    def finalexecute(self):
        return []

    def buildWF(self):
        wf = []
        wf.append(self.initcopy())
        wf.append(self.initexecute())
        wf.append(self._copyfiles())
        wf.append(self.finalexecute())
        return None

class ServiceActivateWFBuilder(WFBuilder):
    def initcopy(self):
        return [CopyFileStep(os.path.join(self.DOMAIN_HOME,"scripts","init.sh"),"/tmp")]

    def initexecute(self):
        return [ExecuteCommandStep("sudo /tmp/init.sh")]

    def getcopyfile(self):
        return[("collectd.conf.j2","/tmp/sa/collectd.conf"),("fping_monitor.py.j2","/tmp/sa/fping_monitor.py"),("final.sh","/tmp/final.sh")]

    def finalexecute(self):
        return [ExecuteCommandStep("sudo /tmp/final.sh")]

class VRouterWFFactory(NodeWFFactory):
    pass

class FirewallWFFactory(NodeWFFactory):
    pass

class VPNWFFactory(NodeWFFactory):
    pass

class DNSWFFactory(NodeWFFactory):
    pass
