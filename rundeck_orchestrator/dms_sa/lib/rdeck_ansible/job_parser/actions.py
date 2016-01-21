__author__ = 'feifeng'

import abc
from utils import Utils


class Action(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, job_name, options=None):
        self.job_name = job_name
        self.options = options

    @abc.abstractmethod
    def process(self, job_definitions):
        pass


class CopyCollectdConf(Action):
    def process(self, job_definitions):
        Utils.execute_ansible_playbook(self.job_name, 'collectd.yaml', self.options)
        files_to_copy = [{"src":"/tmp/rundeck/ansible/%s__fping_monitor.py" % self.job_name, "dst":"/home/%s/fping_monitor.py" % self.options['osType']},
            {"src":"/tmp/rundeck/ansible/%s__collectd.conf" % self.job_name, "dst":"/home/%s/collectd.conf" % self.options['osType']},
            {"src":"/tmp/rundeck/ansible/%s__killer.sh" % self.job_name, "dst":"/home/%s/killer.sh" % self.options['osType']}]
        job_definitions['copyfiles'] = files_to_copy
        print job_definitions


class RestartCollectdService(Action):
    def process(self, job_definitions):
        #commands = ["sudo ps -elf | grep collec[td] | awk '{print $4}' | xargs kill -9", "sudo /home/%s/collectd/sbin/collectd -C /home/%s/collectd/etc/collectd.conf" % (self.options['osType'], self.options['osType'])]
        commands = ["sudo chmod +x /home/%s/killer.sh" % self.options['osType'], "sudo /home/%s/killer.sh" % self.options['osType'] ]
        job_definitions['commands'] = commands
        print job_definitions

