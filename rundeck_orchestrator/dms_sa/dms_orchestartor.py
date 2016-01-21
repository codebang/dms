import sys
import os

from ConfigParser import SafeConfigParser
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))
from yapsy.MultiprocessPluginManager import MultiprocessPluginManager
from yapsy.PluginManager import  PluginManagerSingleton
from yapsy.ConfigurablePluginManager import ConfigurablePluginManager
from yapsy.VersionedPluginManager import VersionedPluginManager
from lib.base.inputbase import InputBase
from lib.base.handlebase import HandleBase
from lib.services.servicecontext import ServiceContext
from Queue import Queue
from apscheduler.schedulers.background import BackgroundScheduler


class DmsOrchestrator:

    ORCH_SECTION = "Orchestrator"

    def _configInitialize(self):
        self.config = SafeConfigParser()
        config_file = os.path.join(os.path.dirname(__file__),"orchestrator.conf")
        self.config.read(config_file)

    def _mangerInitialize(self):
        PluginManagerSingleton.setBehaviour([MultiprocessPluginManager,
                                         ConfigurablePluginManager,
                                         VersionedPluginManager])
        self.manager = PluginManagerSingleton.get()

    def initializeScheduler(self):
        scheduler = BackgroundScheduler()
        connect_url = self.config.get(self.ORCH_SECTION,"sched_connect_url")
        scheduler.add_jobstore('sqlalchemy',url=connect_url)
        return scheduler

    def _serviceInitialize(self):
        ctx = ServiceContext()
        queue = Queue()
        ctx.registerQueueService(queue)
        ctx.registerSchedService(self.initializeScheduler())

    def _pluginInitialize(self):
        self.manager.setPluginPlaces(["lib/plugins"])
        self.manager.setConfigParser(self.config,None)
        self.manager.setCategoriesFilter({'Handler':HandleBase,"Input":InputBase})
        self.manager.collectPlugins()

    def _watiInputDone(self):
        plugins = self.manager.getPluginsOfCategory('Input')
        map(lambda plugin:plugin.plugin_object.proc.join(),plugins)

    def start(self):
        self._configInitialize()
        self._mangerInitialize()
        self._serviceInitialize()
        self._pluginInitialize()
        self._watiInputDone()

if __name__ == "__main__":
    from lib.utils import Logger
    Logger.basicConfig()

    app = DmsOrchestrator()
    app.start()