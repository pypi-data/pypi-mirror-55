import argparse

from dodo_commands import Dodo
from dodo_commands.framework.util import remove_trailing_dashes


def _args():
    parser = argparse.ArgumentParser()
    parser.add_argument('flow_typed_args', nargs=argparse.REMAINDER)
    args = Dodo.parse_args(parser)
    args.flow_typed = 'node_modules/.bin/flow-typed'
    args.cwd = Dodo.get_config('/WEBPACK/webpack_dir')
    return args


if Dodo.is_main(__name__, safe=True):
    args = _args()
    Dodo.run([args.flow_typed, 'install'] +
             remove_trailing_dashes(args.flow_typed_args),
             cwd=args.cwd)
