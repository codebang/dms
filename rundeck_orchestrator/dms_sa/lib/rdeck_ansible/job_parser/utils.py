__author__ = 'feifeng'

import subprocess
import os
import ConfigParser
import importlib
import lib.env
from errors import CmdError
from logger import logger


class Utils(object):
    # @staticmethod
    # def get_project_path():
    #     # folder_path = os.path.dirname(os.path.abspath(__file__)) + "/"
    #     folder_path = lib.env.project_path
    #     return folder_path
    #
    # @staticmethod
    # def load_config():
    #     conf_file = Utils.get_project_path() + "/scripts/dms_sa/lib/rdeck_ansible/job_parser/config.yml"
    #     conf = ConfigParser.ConfigParser()
    #     conf.read(conf_file)
    #     return conf

    # @staticmethod
    # def get_config(section, opt):
    #     conf = Utils.load_config()
    #     return conf.get(section, opt)

    @staticmethod
    def execute_ansible_playbook(job_name, playbook, args=None):
        # ansible_path = Utils.get_config("ansible", "execute_path")
        ansible_path = lib.env.ansible_execute_path
        # ansible_playbook_folder = Utils.get_config("ansible", "playbook_file_path")
        ansible_playbook_folder = lib.env.ansible_playbook_file_path
        args_str = Utils.format_ansible_args(job_name, args)
        cmd = "%s/ansible-playbook %s/%s %s " % (ansible_path, ansible_playbook_folder, playbook, args_str)
        logger.info("*****ansible cmd is: %s" % cmd)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, close_fds=True)
        (stdout, stderr) = proc.communicate()
        if stdout is None or stdout == '':
            logger.exception("Failed to run ansible command: %s!" % cmd)
            raise CmdError("command - %s runs into error state!" % cmd)
        if 'failed=0' not in stdout:
            logger.exception("Ansible command: %s runs into error!" % cmd)
            raise CmdError("failed to execute command: %s" % cmd)
        logger.info(stdout)

    @staticmethod
    def format_ansible_args(job_name, args):
        logger.info("options is: %s" % str(args))
        if args is None:
            return ' -e "JOB_NAME=%s"' % job_name
        else:
            args_lst = []
            for (k, vs) in args.items():
                key = k
                value_lst = []
                if isinstance(vs, list):
                    for value in vs:
                        if value is not None:
                            value_lst.append(value)
                else:
                    if value is not None:
                        value_lst.append(vs)
                args_lst.append("%s=%s" % (key, ",".join(value_lst)))
            args_str = ' '.join(args_lst)
            return ' -e "JOB_NAME=%s %s"' % (job_name, args_str)
#        if args is None:
#            return ' -e "JOB_NAME=%s"' % job_name
#        else:
#            args_lst = []
#            for (k, vs) in args.items():
#                key = k
#                value_lst = []
#                if isinstance(vs, str):
#		    value_lst.append(vs)
#                else:
#                    for value in vs:
#                        value_lst.append(value)
#                args_lst.append("%s=%s" % (key, ",".join(value_lst)))
#                args_str = ' '.join(args_lst)
#            return ' -e "JOB_NAME=%s %s"' % (job_name, args_str)

    @staticmethod
    def convert_action_to_class_name(action_name):
        return ''.join(action_name.title().split('_'))

    @staticmethod
    def load_class(class_name):
        action_module = importlib.import_module("lib.rdeck_ansible.job_parser.actions", class_name)
        action_class = getattr(action_module, class_name)
        return action_class

    @staticmethod
    def log_dict(dict):
        if dict is None:
            return
        for (k, v) in dict.items():
            logger.info("%s = %s" % (k, v))




if __name__ == '__main__':
    Utils.execute_ansible_playbook('44', args={"DST_HOSTS":"9.1.1.1", })
