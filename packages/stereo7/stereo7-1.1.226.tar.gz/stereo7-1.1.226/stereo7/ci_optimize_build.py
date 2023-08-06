import os


def main(project, parser):
    if os.path.isfile('CI_optimize_build.py'):
        return 0 == os.system('CI_optimize_build.py')
    return True
