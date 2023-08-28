from security_hardener import context_runner, actions

def harden():

    context_runner.run("webserver", actions)
