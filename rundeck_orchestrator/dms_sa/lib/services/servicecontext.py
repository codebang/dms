import logging
class ServiceContext:
    """
        No-Thread safe, in main thread , just initialize, then can read parralel
    """
    __shared_state = {}

    LOGGING_SERVICE="logging"
    QUEUE_SERVICE="queue"
    SCED_SERVICE="scheduler"

    def __init__(self):
        self.__dict__ = self.__shared_state

    def _registerService(self,serviceName,service):
        self.__shared_state[serviceName] = service

    def _getSerivceByName(self,name):
        return self.__shared_state[name]

    def registerQueueService(self,service):
        self._registerService(self.QUEUE_SERVICE,service)

    def registerSchedService(self,service):
        self._registerService(self.SCED_SERVICE,service)

    def getQueueService(self):
        return self._getSerivceByName(self.QUEUE_SERVICE)

    def getLoggingService(self):
        return self._getSerivceByName(self.LOGGING_SERVICE)

    def getSchedServcie(self):
        return self._getSerivceByName(self.SCED_SERVICE)


