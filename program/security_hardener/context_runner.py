from security_hardener.config import context_config
from security_hardener.parser import *

def run(ctx, actions):

    #pl, _ = parse_template(ctx=context_config[ctx]) # parsing the context template text file, not using now since we implement only .csv file, see pt_fs below
    ps, include_paths = parse_template(ctx=context_config[ctx], parse_file="system") # parsing the system ssh config file (/etc/ssh/sshd_config)
    pt = parse_csv_template(ctx=context_config[ctx])     # parsing the context template .csv file for full keywords and values
    pt_fs = parse_csv_template_two_cols(ctx=context_config[ctx]) # parsing the context template .csv file for the first and second coloms


    applied_changes = {}
    new_keywords = {}

    print("")
    for ci in pt: # get all fileds from template .csv file

        var = ci["keyword"]

        if var in pt_fs:
            ev = pt_fs[var]  # expected value , values from .csv template file


        # projected value , current values from system ssh config file
        try:
            pv = ps[var]
        except Exception as e:
            if actions.check_cmd("man sshd_config 2>/dev/null | grep -iw {}".format(var)):
                new_keywords[var] = ev

                info = ci["action_true_info"].format(ev)
                print("\n{} {}.".format("\033[33m" + "?" + "\033[0m", info))

                action_confirm_text = ci["action_false_confirm_text"]

                if action_confirm_text == "default": # if the entry in .csv file is default, set the following as confirm text
                    action_confirm_text = "Are you sure to add these values {}? (Enter yes/no): "

                ac = input(action_confirm_text.format(ev))
                action = ci["action_false_function"] # Retrives function name from .cvs file and pass to getattr below

                if action != "None":
                    if ac.lower() in ["y", "yes"]:
                        r = getattr(actions, action)(var, ev)
                        if r:
                            try:
                                new_keywords[r[0]] = r[1]
                            except Exception as e:
                                pass
                continue
            else:
                print("Warning: {} is not a valid keyword in sshd_config".format(var))

        ac = "y"
        if ev != pv:
            info = ci["action_false_info"].format(pv)
            print("\n{} {}.".format("\033[31m" + "X" + "\033[0m", info))

            action_confirm_text = ci["action_false_confirm_text"]

            if action_confirm_text == "default": # if the entry in .csv file is default, set the following as confirm text
                action_confirm_text = "Do you want to change value to {}? (Enter yes/no): "

            ac = input(action_confirm_text.format(ev))
            action = ci["action_false_function"] # Retrives function name from .cvs file and pass to getattr below
        
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
        
    print("")
    if applied_changes or new_keywords:

        try:
            actions.commit(ctx, applied_changes, new_keywords)
            if actions.commit:
                print("\nChanges committed successfully.\n")


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

        pat_vars = r'^\s*#?\s*([A-Za-z0-9\-]+)\s+(.*?)\s*$'

        include_path_applied_changes = {}

        for path in include_paths:
            with open(path, "r") as f:
                 lines = f.readlines()

            parsed_lines = {}

            for i, line in enumerate(lines):
                m = re.match(pat_vars, line)

                if m is not None:
                    parsed_lines[m.group(1)] = m.group(2).strip()


                for key, value in parsed_lines.items():
                    stripped_key = key.strip()  # Strip any leading/trailing whitespace
                    ev = pt_fs.get(stripped_key)  # expected value fetched from csv template file
                    cv = value  # current value in Include files

                    # If the key is not in the .csv template, set ev to None to preserve the current value
                    if ev is None:
                        ev = cv

                    if ev != cv:
                        r = (stripped_key, ev)
                        include_path_applied_changes[r[0]] = r[1]
                        if include_path_applied_changes:
                           actions.include_path_commit(path, include_path_applied_changes)
