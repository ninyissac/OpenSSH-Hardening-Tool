from security_hardener.config import context_config
from security_hardener.parser import *

def run(ctx, actions):

    #pl, _ = parse_template(ctx=context_config[ctx]) # parsing the context template text file, not using now since we implement only .csv file, see pt_fs below
    ps, include_paths = parse_template(ctx=context_config[ctx], parse_file="system") # parsing the system ssh config file (/etc/ssh/sshd_config)
    pt = parse_csv_template(ctx=context_config[ctx])     # parsing the context template .csv file for full keywords and values
    pt_fs = parse_csv_template_two_cols(ctx=context_config[ctx]) # parsing the context template .csv file for the first and second coloms

    print("\nps:",ps)
    print("-"*50)
    print("\npt:",pt)
    print("-"*50)
    print("\npt_fs:",pt_fs)
    print("-"*50)
    print("\n")

    applied_changes = {}
    new_keywords = {}

    for ci in pt: # get all fileds from template .csv file

        var = ci["variable"]

        # expected value , values from .csv template file
        ev = pt_fs[var]

        # projected value , current values from system ssh config file
        try:
            pv = ps[var]
        except Exception as e:
            if actions.check_cmd("man sshd_config | grep -iw {}".format(var)):
                new_keywords[var] = ev
                continue
            else:
                print("Warning: {} is not a valid keyword in sshd_config".format(var))

        ac = "y"
        if ev != pv:
            info = ci["action_false_info"].format(pv)
            print("{} {}.".format("\033[31m" + "X" + "\033[0m", info))

            action_confirm_text = ci["action_false_confirm_text"]

            if action_confirm_text == "default": # if the entry in .csv file is default, set the following as confirm text
                action_confirm_text = "Do you want to change value to {}? (Enter yes/no): "

            ac = input(action_confirm_text.format(ev))
            action = ci["action_false"] # Retrives function name from .cvs file and pass to getattr below
        
        else:
            info = ci["action_true_info"].format(pv)
            print("{} {}.".format("\033[32m(" + chr(0x2713) + ")\033[0m", info))
            action = "actionTrue" # This passes the function name to getattr to retrieve the function from actions.py


        if action != "None":
            if ac.lower() in ["y", "yes"]:
                r = getattr(actions, action)(var, ev)
                if r:
                    try:
                        applied_changes[r[0]] = r[1]
                    except Exception as e:
                        pass
        
    if applied_changes or new_keywords:

        try:
            actions.commit(ctx, applied_changes, new_keywords)

        except Exception as e:
            print("Could not commit the changes in sshd_config config due to {}".format(e))
            return False
    
        try:
            actions.restart(ctx)

        except Exception as e:
            print("Failed to restart ssh service due to {},\nFalling back to existing config".format(e))
            actions.revert_changes(ctx)
    

# Following code is for processing /etc/ssh/sshd_config.d/*.conf files, ie. for Include keyword from sshd_config
    if include_paths:

        pat_vars = r'^#?\s*([A-Za-z]+)\s+(.+)$'

        include_path_applied_changes = {}

        for path in include_paths:
            with open(path, "r") as f:
                 lines = f.readlines()

            parsed_lines = {}

            for i, line in enumerate(lines):
                m = re.match(pat_vars, line)

                if m is not None:
                    parsed_lines[m.group(1)] = m.group(2).strip()
                    print("From IP:", parsed_lines)

                print("Keys in pt_fs:", list(pt_fs.keys()))

                for key, value in parsed_lines.items():
                    stripped_key = key.strip()  # Strip any leading/trailing whitespace
                    print("Stripped key:", stripped_key)
                    ev = pt_fs.get(stripped_key)  # expected value fetched from csv template file
                    print("ev:", ev)
                    print("ev for {}: {}".format(stripped_key, ev))
                    cv = value  # current value in Include files
                    print("cv:", cv)

                    # If the key is not in the .csv template, set ev to None to preserve the current value
                    if ev is None:
                        ev = cv

                    if ev != cv:
                        r = (stripped_key, ev)
                        print("r:", r)
                        include_path_applied_changes[r[0]] = r[1]
                        if include_path_applied_changes:
                           actions.include_path_commit(path, include_path_applied_changes)
