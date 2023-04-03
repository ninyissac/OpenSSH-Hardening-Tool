from security_hardener.config import context_config, program_name, program_description
import importlib

def set_program_title():

    print("".join(["|", "="*70, "|"]))
    print("".join(["|", " "*70, "|"]))
    print(f"|{program_name: ^70}|")
    print("".join(["|", " "*70, "|"]))
    print("".join(["|", " "*70, "|"]))
    print(f"|{program_description: ^70}|")
    print("".join(["|", " "*70, "|"]))
    print("".join(["|", " "*70, "|"]))
    print("".join(["|", "="*70, "|"]))
    print("\n")

def select_context():

    import inquirer

    context_questions = [
        inquirer.List("ctx", "On which context you need to harden?", choices=context_config.keys())
    ]

    ans = inquirer.prompt(context_questions)
    return ans["ctx"]


def main():
    set_program_title()
    ctx = select_context()
    ctx_cnf = context_config[ctx]

    print("*** Please ensure you have configured the {} config file in {}.\n".format(ctx, ctx_cnf["template_path"]))

    confirm = input("The program will analyse your inputs and ask some questions before we change something in your machine. \nPlease confirm if you need to start hardening {}. (Enter yes/no): ".format(ctx))

    confirm = confirm.lower()
    if confirm in ["yes", "y"]:
        ch = importlib.import_module('security_hardener.src.{}'.format(ctx))
        ch.harden()
    
    else:
        print("Have a nice day!")


main()
