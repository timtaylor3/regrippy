from regrippy import BasePlugin, PluginResult, mactime
from Registry import Registry

class Plugin(BasePlugin):
    """Lists all services installed on the system"""
    __REGHIVE__ = "SYSTEM"

    def run(self):
        key = self.open_key(self.get_currentcontrolset_path() + "\\Services")
        if not key:
            return

        for v in key.subkeys():
            try:
                display_name = v.value("DisplayName").value()
            except:
                display_name = "None Found"

            try:
                description = v.value("Description").value()
            except:
                description = "None Found"

            try:
                image_path = v.value("ImagePath").value()
            except:
                image_path = "None Found"

            try:
                dll = v.subkey("Parameters").value("ServiceDll").value()
            except:
                dll = "None Found"

            try:
                if v.value("Start").value() == 0:
                    start_type = 'Boot'
                elif v.value("Start").value() == 1:
                    start_type = 'System'
                elif v.value("Start").value() == 2:
                    start_type = 'Automatic'
                elif v.value("Start").value() == 3:
                    start_type = 'Manual'
                elif v.value("Start").value() == 4:
                    start_type = 'Disable'
            except:
                start_type = "None Found"

            message = 'Service Name: {0}, Display Name: {1}, Image Path: {2}, DLL: {3}, Description: {4}, ' \
                      'Start Type: {5}'.format(v.name(), display_name, image_path, dll, description, start_type)

            res = PluginResult(key=key, value=None)
            res.custom["message"] = message
            dt = key.timestamp()
            res.custom['Last Write Time'] = dt.isoformat('T') + 'Z'
            yield res

    def display_human(self, result):
        print(result.custom["message"], result.custom['Last Write Time'])

    def display_machine(self, result):
        print(mactime(name=f"{result.key_name}\t{result.custom['message']}", mtime=result.mtime))
