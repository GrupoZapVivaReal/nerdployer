
import argparse
import os
from nerdployer.flow import NerdFlow


def _run(file, context):
    flow = NerdFlow(file, context)
    flow.run()


def _initialize_context(pairs):
    context = {}
    if pairs:
        for pair in pairs:
            k, v = pair.split('=')
            try:
                context[k] = eval(v)
            except NameError:
                context[k] = v
    return context


def main():
    parser = argparse.ArgumentParser(description='nerdployer tool')
    parser.add_argument('--nerdfile', default='nerdfile', help='nerdfile in yaml or json format')
    parser.add_argument('--context', nargs='*', help='initial nerdployer context in key=value format')
    args = parser.parse_args()

    if not os.path.exists(args.nerdfile):
        parser.error('please provide a nerdfile')

    _run(args.nerdfile, _initialize_context(args.context))	


if __name__ == '__main__':
    main()
