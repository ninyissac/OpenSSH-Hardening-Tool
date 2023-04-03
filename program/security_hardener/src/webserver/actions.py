from security_hardener.config import context_config
import os

def alterStandardValue(cfg_var, ev):
    return (cfg_var, ev)

def alterValue(cfg_var, ev):
    return (cfg_var, ev)

def changeLogLevel(*args):

    print("Need to apply some logic in this case before I setting the value\n")
    return args

def commit(changes):
    import re

    ssh_system_config_file = context_config["webserver"]["system_path"]

    with open(ssh_system_config_file, "r") as orig_file:
        lines = orig_file.readlines()

    with open("/tmp/ssh_file.bkp", "w") as tf:
        for i, line in enumerate(lines):
            tf.write(line)

    pat = r'^#?([a-zA-Z]+)\s+[a-zA-Z0-9 ]+\s*$'
    with open("/tmp/ssh_file_changed", "w") as tf:
        for i, line in enumerate(lines):

            m = re.match(pat, line)

            content = line

            if m is not None:
                cfg = m.group(1)

                if cfg in changes:

                    content = f"{cfg} {changes[cfg]}\n"
                    
            tf.write(content)

    os.replace("/tmp/ssh_file_changed", ssh_system_config_file)
    return True


def restart():
    import subprocess
    cmd = context_config["webserver"]["restart_cmd"].split(" ")
    subprocess.call(cmd)
    return True


def revert_changes():
    ssh_system_config_file = context_config["webserver"]["system_path"]
    os.replace("/tmp/ssh_file.bkp", ssh_system_config_file)
    return True
