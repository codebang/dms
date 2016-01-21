#!/usr/bin/env python
#coding=utf-8

import subprocess
import socket


class FPingError(Exception):
    pass


class CmdError(FPingError):
    pass


class FPing(object):
    def __init__(self, path='/usr/bin/fping', interval=10, src_host='localhost', dst_hosts=[]):
        self.path = path
        self.interval = interval
        self.src_host = src_host
        self.dst_hosts = dst_hosts

    def _compose_cmd_line(self):
        cmd = [self.path, '-e']
        for host in self.dst_hosts:
            cmd.append(host)
        return ' '.join(cmd)

    def _run(self):
        cmd = self._compose_cmd_line()
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, close_fds=True)
        (stdout, stderr) = proc.communicate()
        if stdout is None or stdout == '':
            raise CmdError('Command: %s has no output.' % cmd)
        return stdout

    def get_elapsed_time(self):
        result = []
        output = self._run()
        elapsed_time_data = output.split('\n')
        for data in elapsed_time_data:
            if data != '':
                dst_host, elapsed_time = self._parse_elapsed_time(data)
                # dst_host = self.src_host + "_" + dst_host
                dst_host = dst_host
                print("host: %s -> time: %f" % (dst_host, elapsed_time))
                result.append([dst_host, elapsed_time])
        return result

    def _parse_elapsed_time(self, line):
        if 'unreachable' in line:
            items = line.split(' ')
            dst_host = items[0].replace("-",".")
            elapsed_time = -1.0
        else:
            items = line.split('(')
            dst_host = items[0].split(' ')[0]
            elapsed_time = float(items[1].replace(' ms)', ''))
        return (dst_host, elapsed_time)


def get_host_name():
    return socket.gethostname().replace("-", "_")

class FPingMon(object):
    def __init__(self):
        self.plugin_name = 'collectd-fping-python'
        self.fping_path = '/usr/bin/fping'
        self.src_host = get_host_name()
        self.dst_hosts = []
        self.fping_interval = 10
        self.verbose_logging = True

    def log_verbose(self, msg):
        if not self.verbose_logging:
            return
        collectd.info('%s plugin [verbose]: %s ' % (self.plugin_name, msg))

    def configure_callback(self, conf):
        for node in conf.children:
            val = str(node.values[0])

            if node.key == 'Path':
                self.fping_path = val
            elif node.key == 'Interval':
                self.fping_interval = float(val)
            elif node.key == 'PluginName':
                self.plugin_name = val
            elif node.key == 'DSTHosts':
                self.dst_hosts = val.split(',')
            elif node.key == 'Verbose':
                self.verbose_logging = val in ['True', 'true']
            else:
                collectd.warning('%s plugin: Unknown config key: %s.' % (self.plugin_name, node.key))

        self.log_verbose('Configured with plugin_name=%s, fping_path=%s, interval=%d, dsk_hosts=%s, verbose_logging=%s' %
                         (self.plugin_name, self.fping_path, self.fping_interval, str(self.dst_hosts), str(self.verbose_logging)))

    def disptach_value(self, host, type_instance, value):
        self.log_verbose('Sending value: %s-%s' % (host, str(value)))
        val = collectd.Values(type='gauge')
        val.plugin = self.plugin_name
        # val.plugin_instance = plugin_instance
        # val.type = val_type
        val.interval = self.fping_interval
        val.host = self.src_host + '__' + host
        val.type_instance = type_instance
        val.values = [value,]
        val.dispatch()

    def read_callback(self):
        try:
            self.log_verbose('Read callback called')
            fping = FPing(path=self.fping_path,
                      interval=self.fping_interval,
                      src_host=self.src_host,
                      dst_hosts=self.dst_hosts)
            data = fping.get_elapsed_time()
            self.log_verbose(data)

            for each_data in data:
                # plugin_instance = 'elapsed_time'
                # val_type = collectd.DS_TYPE_GAUGE
                host = each_data[0]
                type_instance = 'elapsed_time'
                value = each_data[1]
                self.disptach_value(host, type_instance, value)
        except Exception as exp:
            self.log_verbose("run into exception")
            self.log_verbose(exp.message)
            self.log_verbose(exp.args)


if __name__ == '__main__':
    fping = FPing(dst_hosts=['8.8.8.8', '1.1.1.1'])
    result = fping.get_elapsed_time()
    print result
else:
    import collectd
    fping_mon = FPingMon()
    collectd.register_config(fping_mon.configure_callback)
    collectd.register_read(fping_mon.read_callback)
