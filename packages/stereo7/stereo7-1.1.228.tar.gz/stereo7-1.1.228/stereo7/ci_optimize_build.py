import os


def main(project, parser):
    if os.path.isfile('tools/CI_optimize_build.py'):
        return 0 == os.system('cd tools; python CI_optimize_build.py')
    return True
