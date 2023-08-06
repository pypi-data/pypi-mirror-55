import argparse

from dodo_commands import Dodo, ConfigArg, remove_trailing_dashes


def _args():
    parser = argparse.ArgumentParser(
        description="Runs the django development server.")
    return Dodo.parse_args(parser,
                           config_args=[
                               ConfigArg('/DJANGO/port',
                                         '--port',
                                         default='8000'),
                               ConfigArg('/DJANGO/python',
                                         '--python',
                                         default='python'),
                               ConfigArg('/DJANGO/src_dir',
                                         '--cwd',
                                         default='.'),
                               ConfigArg('/DJANGO/manage_py',
                                         '--manage-py',
                                         default='manage.py'),
                               ConfigArg('/DJANGO/runserver_args',
                                         '--runserver_args',
                                         nargs='+'),
                           ])


if Dodo.is_main(__name__):
    args = _args()
    Dodo.run([
        args.python,
        args.manage_py,
        "runserver",
        "0.0.0.0:%s" % args.port,
    ] + remove_trailing_dashes(args.runserver_args or []),
             cwd=args.cwd)
