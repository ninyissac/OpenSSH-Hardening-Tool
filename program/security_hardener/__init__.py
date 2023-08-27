from security_hardener.config import context_config, program_name, program_description
import importlib

def set_program_title():

    print("".join(["||", "="*70, "||"]))
    print("".join(["||", " "*70, "||"]))
    print(f"||{program_name: ^70}||")
    print("".join(["||", " "*70, "||"]))
    print("".join(["||", " "*70, "||"]))
    print(f"||{program_description: ^70}||")
    print("".join(["||", " "*70, "||"]))
    print("".join(["||", " "*70, "||"]))
    print("".join(["||", "="*70, "||"]))
    print("\n")

def select_context():

    import inquirer

    context_questions = [
        inquirer.List("ctx", "Please select the operational context of the server system by arrow keys, current selection -> ", choices=context_config.keys())
    ]

    ans = inquirer.prompt(context_questions)
    print("-"*70)
    return ans["ctx"]


def main():
    set_program_title()
    ctx = select_context()
    ctx_cnf = context_config[ctx]

    confirm = input("Please confirm to start hardening \"\033[31m{}\033[0m\". (Enter yes/no): ".format(ctx))

    confirm = confirm.lower()
    if confirm in ["yes", "y"]:
        ch = importlib.import_module('security_hardener.src.{}'.format(ctx))
        ch.harden()

    else:
        print("")

main()
