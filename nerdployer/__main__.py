
import sys
from nerdployer.flow import NerdFlow
import nerdployer.helpers.bootstrap as bootstrap


def run(file):
    initial_context = {}
    flow = NerdFlow(file, initial_context)
    flow.run()
    return 0


if __name__ == '__main__':
    bootstrap.run()
    run(sys.argv[1])
