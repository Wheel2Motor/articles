Python3动态加载模块
================================================================================

__测试版本__：Python3.10.8

### \_\_import\_\_代替import

```python
sys = __import__("sys")
print(sys.version_info)
# sys.version_info(major=3, minor=10, micro=8, releaselevel='final', serial=0)
```

### 根据输入模块路径动态加载模块

```python
import os
import importlib.util
from typing import Dict, Optional, no_type_check
from types import ModuleType

loaded_modules: Dict[str, ModuleType] = { }

@no_type_check
def import_module(path: str, name: Optional[str] = None):
    mod = None
    try:
        path = os.path.expanduser(path)
        path = os.path.expandvars(path)
        path = os.path.normpath(path)
        path = os.path.abspath(path)
        if name is None:
            name = os.path.splitext(os.path.split(path)[-1])[0]
        if os.path.isfile(path):
            spec = importlib.util.spec_from_file_location(name, path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
        elif os.path.isdir(path):
            entry = os.path.join(path, "__init__.py")
            if not os.path.exists(entry):
                raise ImportError("Entry file for module not found")
            spec = importlib.util.spec_from_file_location(name, entry)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
        else:
            raise ImportError("Module not found")
    except Exception as e:
        return None, "Exception when loading module\n{0}\n<{1}>\n".format(str(e), path)
    loaded_modules[name] = mod
    return mod, ""


if __name__ == "__main__":
    foo, err = import_module("~/Desktop/testcode/foo.py")
    bar, err = import_module("~/Desktop/testcode/bar")
    print(foo, err)
    print(bar, err)
```
