from regrippy import BasePlugin, PluginResult, mactime
from Registry import Registry

class Plugin(BasePlugin):
    """Lists all services with svchost installed on the system"""
    __REGHIVE__ = "SYSTEM"

    def run(self):
        key = self.open_key(self.get_currentcontrolset_path() + "\\Services")
        if not key:
            return

        for v in key.subkeys():
            try:
                display_name = v.value("DisplayName").value()
            except Registry.RegistryValueNotFoundException:
                display_name = "N/A"

            try:
                description = v.value("Description").value()
            except Registry.RegistryValueNotFoundException:
                description = "N/A"

            try:
                image_path = v.value("ImagePath").value()
            except Registry.RegistryValueNotFoundException:
                image_path = "N/A"

            try:
                dll = v.subkey("Parameters").value("ServiceDll").value()
            except Registry.RegistryKeyNotFoundException:
                dll = "N/A"
            except Registry.RegistryValueNotFoundException:
                dll = "N/A"

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
            except Registry.RegistryValueNotFoundException:
                start_type = "N/A"

            try:
                if v.value("Type").value() == 1:
                    service_type = 'KernelDRiver'
                elif v.value("Type").value() == 2:
                    service_type = 'FileSystemDriver'
                elif v.value("Type").value() == 4:
                    service_type = 'Adapter'
                elif v.value("Type").value() == 8:
                    service_type = 'RecognizerDriver'
                elif v.value("Type").value() == 16:
                    service_type = 'Win32OwnProcess'
                elif v.value("Type").value() == 32:
                    service_type = 'Win32ShareProcess'
                elif v.value("Type").value() == 256:
                    service_type = 'InteractiveProcess'

            except Registry.RegistryValueNotFoundException:
                service_type = "N/A"

            message = 'Service Name: {0}, Display Name: {1}, Image Path: {2}, DLL: {3}, Description: {4}, ' \
                      'Start Type: {5}, Service Type: {6}'.format(v.name(), display_name, image_path, dll,
                                                                  description, start_type, service_type)
            if "svchost" in image_path:
                res = PluginResult(key=key, value=None)
                res.custom["message"] = message
                dt = key.timestamp()
                res.custom['Last Write Time'] = dt.isoformat('T') + 'Z'
                yield res

    def display_human(self, result):
        print(result.custom["message"], result.custom['Last Write Time'])

    def display_machine(self, result):
        print(mactime(name=f"{result.custom['message']}", mtime=result.mtime))
