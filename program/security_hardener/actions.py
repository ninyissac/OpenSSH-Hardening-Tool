from security_hardener.config import context_config
from security_hardener.backup import backup
import os
import subprocess

def actionTrue(cfg_var, ev):
    return True


def alterStandardValue(cfg_var, ev):
    return (cfg_var, ev)


def alterValue(cfg_var, ev):
    return (cfg_var, ev)


def commit(ctx, changes, new_keywords):
    import re

    ssh_system_config_file = context_config[ctx]["system_path"]

    # Taking the backup of the sshd_config file with timestamp
    backup(ssh_system_config_file)

    with open(ssh_system_config_file, "r") as orig_file:
        lines = orig_file.readlines()

    with open("/tmp/ssh_file.bkp", "w") as tf:
        os.chmod("/tmp/ssh_file.bkp",0o600)
        for i, line in enumerate(lines):
            tf.write(line)

    pat = r'^\s*#?\s*([A-Za-z0-9]+)\s+([A-Za-z0-9 ]+)\s*$'

    with open("/tmp/ssh_file_changed", "w") as tf:
        os.chmod("/tmp/ssh_file_changed",0o600)
        for i, line in enumerate(lines):

            m = re.match(pat, line)

            content = line

            if m is not None:
                cfg = m.group(1)

                if cfg in changes:

                    content = f"{cfg} {changes[cfg]}\n"
                    if content.startswith('#'):
                        content = content[1:]
                    commit_message = f"Setting {cfg} to {changes[cfg]}"
                    print(commit_message)
                    
            tf.write(content)
    
    confirm = None

    if new_keywords:
        print("New Keywords found:")
        print("-"*25)
        for k, v in new_keywords.items():
            print("\n{} {}".format(k, v))

        confirm = input("\nApply these new keywords? (Enter yes/no): ")
        confirm = confirm.lower()

        if confirm in ["yes", "y"]:
            with open("/tmp/ssh_file_changed", "a") as nkf:
                nkf.write("\n\n# Newly added keywords by the OpenSSH Hardener program, intended by the user.\n")
                for k, v in new_keywords.items():
                    nkf.write("\n{} {}\n".format(k, v))
                    new_keyword_message = f"Setting {k} to {v}"
                    print(new_keyword_message)

    os.replace("/tmp/ssh_file_changed", ssh_system_config_file)

    return True


def include_path_commit(path, changes):
    import os
    import re

    with open(path, "r") as orig_file:
        lines = orig_file.readlines()

    with open("/tmp/include_path_ssh_file.bkp", "w") as tf:
        os.chmod("/tmp/include_path_ssh_file.bkp",0o644)
        for i, line in enumerate(lines):
            tf.write(line)

    pat = r'^\s*#?\s*([A-Za-z0-9]+)\s+([A-Za-z0-9 ]+)\s*$'
    with open("/tmp/include_path_ssh_file_changed", "w") as tf:
        os.chmod("/tmp/include_path_ssh_file_changed",0o644)
        for i, line in enumerate(lines):

            m = re.match(pat, line)

            content = line

            if m is not None:
                cfg = m.group(1)

                if cfg in changes:

                    content = f"{cfg} {changes[cfg]}\n"
            tf.write(content)

    print("Reflecting changes to override file:", path)
    os.replace("/tmp/include_path_ssh_file_changed", path)
    return True


def check_cmd(cmd):
    r = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, text=True)
    if r.returncode:
        return False
    
    return True


def restart(ctx):
    cmd = context_config[ctx]["restart_cmd"].split(" ")
    subprocess.call(cmd)
    return True


def revert_changes(ctx):
    ssh_system_config_file = context_config[ctx]["system_path"]
    os.replace("/tmp/ssh_file.bkp", ssh_system_config_file)
    return True
