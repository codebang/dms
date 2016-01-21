__author__ = 'feifeng'

import collections
from logger import logger
from errors import ActionNameError, JobParserError
from utils import Utils


class JobParser(object):
    def __init__(self, job_name, event_name, options=None):
        logger.info("Begin to parse job: node_name=%s, action_name: %s" % (job_name, event_name))
        Utils.log_dict(options)
        # self.node_name = node_name
        self.job_name = job_name
        self.event_name = event_name
        self.options = options
        self.actions = []
        self.job_definitions = collections.OrderedDict()

    def _get_actions(self):
        if self.event_name == 'CREATE_VM':
            self.actions.append('copy_collectd_conf')
            self.actions.append('restart_collectd_service')
        elif self.event_name == 'Update VM':
            self.actions.append("xxx")
        else:
            logger.error("Unknown event name: %s" % self.event_name)
            raise ActionNameError("Unknown event name!!")

    def _insert_node_name(self):
        pass

    def process_actions(self):
        self._get_actions()
        for action in self.actions:
            action_class_name = Utils.convert_action_to_class_name(action)
            action_class = Utils.load_class(action_class_name)(self.job_name, self.options)
            action_class.process(self.job_definitions)
        return self.job_definitions


if __name__ == '__main__':

    event_name = 'Create VM'
    job_name = '666'
    options = {"neighbors":['10.74.124.125', "xxx"], "osType":"ubuntu"}
    try:
        job_parser = JobParser(job_name, event_name, options)
        result = job_parser.process_actions()

        logger.info("Successfully parsed job_id: %s with action name: %s" % (job_name, event_name))
        logger.info("******start job definition******")
        logger.info(result)
        logger.info("******end job definition******")

        # for (k, v) in result.items():
        #     print str(k) + '__' + str(v)

    except Exception as exception:
        logger.exception("Failed to parser job_id: %s with action name: %s!!!" % (job_name, event_name))
        logger.exception(exception.message)
        raise JobParserError("Failed to parser job_id: %s with action name: %s" % (job_name, event_name))




