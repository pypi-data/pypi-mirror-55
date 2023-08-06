from argparse import ArgumentParser
import os

from dodo_commands import Dodo


def _args():
    parser = ArgumentParser()
    args = Dodo.parse_args(parser)
    args.output_dir = Dodo.get_config('/SPHINX/output_dir')
    args.src_dir = Dodo.get_config('/SPHINX/src_dir')
    return args


if Dodo.is_main(__name__):
    args = _args()

    if not os.path.exists(args.output_dir):
        Dodo.run(['mkdir', '-p', args.output_dir])

    Dodo.run([
        'sphinx-build',
        '-b',
        'html',
        args.src_dir,
        args.output_dir,
    ], )
