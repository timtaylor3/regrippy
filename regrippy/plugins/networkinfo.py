# Plugin written by Tim Taylor, timtaylor3@yahoo.com
from regrippy import BasePlugin, PluginResult, mactime


class Plugin(BasePlugin):
    __REGHIVE__ = ["SOFTWARE"]

    def run(self):

        path = "Microsoft\\Windows NT\\CurrentVersion\\NetworkCards"
        key = self.open_key(path)
        if not key:
            return

        nic_list = list()
        for v in key.subkeys():
            nic_list.append(v.name())

        for nic in nic_list:
            path = "".join(["Microsoft\\Windows NT\\CurrentVersion\\NetworkCards\\", nic])
            key2 = self.open_key(path)
            if not key2:
                return

            desc = ''
            service_name = ''
            for v in key2.values():
                res = PluginResult(key=key, value=v)
                if v.name() == "Description":
                    desc = v.value()
                if v.name() == "ServiceName":
                    service_name = v.value()

                res.custom['value'] = "{}, {}".format(service_name, desc)
            yield res

    def display_human(self, result):
        print(result.custom['value'])

    def display_machine(self, result):
        print(mactime(name=result.custom['value'], mtime=result.mtime))
