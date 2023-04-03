from security_hardener.config import context_config
from security_hardener.parser import *
from security_hardener.src.backupserver import actions

def harden():

    pl = parse_template(ctx=context_config["backupserver"])
    pc = parse_compiler(ctx=context_config["backupserver"])
    ps = parse_template(ctx=context_config["backupserver"], parse_file="system")

    print("-"*50)
    print("\n")

    applied_changes = {}

    for ci in pc:

        var = ci["variable"]

        # expected value
        ev = pl[var]

        # projected value
        pv = ps[var]

        ac = "y"
        if ev != pv:
            info = ci["action_false_info"].format(pv)
            print("{} {}.".format("\033[31m" + "✕" + "\033[0m", info))

            action = ci["action_false"]
            action_confirm = ci["action_false_confirm"]
            action_confirm_text = ci["action_false_confirm_text"]

            if action_confirm_text == "default":
                action_confirm_text = "Do you want to override value to {}? (Enter yes/no): "


            if action_confirm.lower() in ["y", "yes"]:
                ac = input(action_confirm_text.format(ev))
        
        else:
            print("{} {}.".format("\033[32m" + "✓" + "\033[0m", ci["action_true_info"]))
            action = ci["action_true"]

            action_confirm = ci["action_true_confirm"]
            action_confirm_text = ci["action_true_confirm_text"]

            if action_confirm.lower() in ["y", "yes"]:
                ac = input(action_confirm_text.format(ev))

        if action != "None":
            if ac.lower() in ["y", "yes"]:
                r = getattr(actions, action)(var, ev)
                applied_changes[r[0]] = r[1]
        
    if applied_changes:

        try:
            actions.commit(applied_changes)

        except Exception as e:
            print("Could not commit the changes in ssh config due to {}".format(e))
            return False
    
        try:
            actions.restart()

        except Exception as e:
            print("Failed to restart ssh service due to {},\nFalling back to existing config".format(e))
            actions.revert_changes()
