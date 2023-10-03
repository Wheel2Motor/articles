获取电脑上安装的3DsMax和Maya安装路径
================================================================================

```python
import os
import re
import winreg # pip install winregistry

REG_PATH_3DSMAX = r"SOFTWARE\Autodesk\3dsMax"
REG_PATH_MAYA   = r"SOFTWARE\Autodesk\MAYA"

class RegKey:

    def __init__(self, section, *args):
        self.__section = section
        self.__path = os.path.join(*args)
        self.__key = None

    def __del__(self):
        self.unlock()

    def lock(self):
        self.unlock()
        self.__key = winreg.OpenKey(self.__section, self.__path)

    def unlock(self):
        if self.__key is not None:
            winreg.CloseKey(self.__key)
            self.__key = None

    def subkeys(self):
        ret = set()
        counter = 0
        while True:
            try:
                subkeyname = winreg.EnumKey(self.__key, counter)
                ret.add(subkeyname)
                counter += 1
            except OSError as e:
                if e.errno == 22:
                    break
                else:
                    raise e
        return ret

    def values(self):
        ret = {}
        counter = 0
        while True:
            try:
                name, value, typ = winreg.EnumValue(self.__key, counter)
                ret[name] = (value, typ)
                counter += 1
            except OSError as e:
                if e.errno == 22:
                    break
                else:
                    raise e
        return ret

    def __enter__(self):
        self.lock()
        return self

    def __exit__(self, typ, value, trace):
        if typ and value and trace:
            errmsg = ""
            errmsg += "Error Type: " + str(typ) + "\n"
            errmsg += "Error Value: " + str(value) + "\n"
            errmsg += "Error Trace: " + str(trace) + "\n"
            sys.stderr.write(errmsg)
        self.unlock()

def get_install_path_3dsmax():
    install_path = {}
    with RegKey(winreg.HKEY_LOCAL_MACHINE, REG_PATH_3DSMAX) as key:
        version_machine = list(filter(lambda item: re.match("\A[0-9]+\.[0-9]+\Z", item), key.subkeys()))
        for ver in version_machine:
            with RegKey(winreg.HKEY_LOCAL_MACHINE, REG_PATH_3DSMAX, ver) as subkey:
                name = subkey.values().get("ProductName", (None,))[0]
                path = subkey.values().get("Installdir", (None,))[0]
                if name and path:
                    target = os.path.join(path, "3dsmax.exe")
                    if os.path.exists(target):
                        install_path[name.split()[-1]] = target
    return install_path

def get_install_path_maya():
    install_path = {}
    with RegKey(winreg.HKEY_LOCAL_MACHINE, REG_PATH_MAYA) as key:
        version_machine = key.subkeys()
        version_machine = list(filter(lambda item: re.match("\A[0-9]+\Z", item), key.subkeys()))
        for ver in version_machine:
            with RegKey(winreg.HKEY_LOCAL_MACHINE, REG_PATH_MAYA, ver, "Setup", "InstallPath") as subkey:
                target = os.path.join(subkey.values().get("MAYA_INSTALL_LOCATION", (None,))[0], "bin", "maya.exe")
                if os.path.exists(target):
                    install_path[ver] = target
    return install_path

if __name__ == "__main__":
    from pprint import pprint
    pprint(get_install_path_3dsmax())
    pprint(get_install_path_maya())
```
