import sys

from project_archer.environment.environment import BashEnvironment

def main():
    run_mode = None

    if len(sys.argv) > 1:
        run_mode = sys.argv[1]

    env = BashEnvironment()

    if not run_mode:
        print("""You need to define a run mode, e.g.:

        $ . archer.sh
        $ project -n test
        $ project test""")
        quit(1)

    env.define_command(run_mode, 'eval `%s -m project_archer.project --internalRunMode=%s $@`' % (sys.executable, run_mode))
    env.flush()


if __name__ == '__main__':
    main()
