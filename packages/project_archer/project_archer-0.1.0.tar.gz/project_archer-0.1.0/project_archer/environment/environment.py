# Because we want to export variables to the shell running the script, we can't
# actually interact with the environment directly from the script (and have it
# persist) - instead, we output the bash commands which will modify the
# environment, which the parent shell can then |eval|

class BashEnvironment:
    def __init__(self):
        self._execution = ""
    
    def set_envvar(self, name, value):
        self._execution += "export " + escape(name) + "='" + escape(value) + "'\n"
        return self

    def unset_envvar(self, name):
        self._execution += "unset " + escape(name) + "\n"
        return self

    def log(self, message):
        self._execution += "echo -e $'" + escape(message) + "'\n"
        return self

    def define_command(self, name, body):
        self._execution += ("function " + escape(name) + "() {\t" +
            "\n\t".join(line for line in body.split('\n') if line) +
            "\n}\n")
        return self

    def remove_command(self, name):
        self._execution += "unset -f " + escape(name) + "\n"
        return self

    def execute(self, body):
        self._execution += escape(body) + "\n"
        return self

    def flush(self):
            print(self._execution.replace("\n", ";"))
            return self

def escape(message):
    if type(message) is not str:
        message = str(message)

    return message.replace('\n', '\\n').replace("'", "\\'")
