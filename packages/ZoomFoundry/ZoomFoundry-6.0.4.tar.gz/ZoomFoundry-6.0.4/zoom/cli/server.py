"""
    zoom server cli
"""

import logging
import os
import sys
from argparse import ArgumentParser


def server(instance='.'):
    """run an instance using Python's builtin HTTP server"""

    parser = ArgumentParser(
        description='run a built-in zoom http server',
        usage='zoom server [options] instance'
        )

    parser.add_argument("-p", "--port", type=int, default=80,
                        help='http service port')
    parser.add_argument("-n", "--noop", action='store_true',
                        help='use special debugging middleware stack')
    parser.add_argument("-u", "--user", type=str, default=None,
                        help='run site as specified user')
    parser.add_argument("-v", "--verbose", action='store_true',
                        help='verbose console logging')
    parser.add_argument("-f", "--filter", type=str, default=None,
                        help='log filter')
    parser.add_argument('instance', nargs='?', default=None)
    args = parser.parse_args()

    from zoom.server import run as runweb
    import zoom.middleware
    try:
        if args.instance and not os.path.exists(args.instance):
            print('{!r} is not a valid directory'.format(args.instance))
        else:
            instance = args.instance
            fmt = (
                '%(asctime)s %(levelname)-8s %(name)-20s '
                '%(lineno)-4s %(message)s'
            )
            con_formatter = logging.Formatter(fmt)
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.WARNING)
            console_handler.setFormatter(con_formatter)

            root_logger = logging.getLogger()
            root_logger.setLevel(logging.DEBUG)
            root_logger.addHandler(console_handler)

            if args.filter:
                console_handler.addFilter(logging.Filter(name=args.filter))

            if args.verbose:
                console_handler.setLevel(logging.DEBUG)
            else:
                console_handler.setLevel(logging.INFO)

            for handler in root_logger.handlers:
                handler.setFormatter(con_formatter)

            if args.noop:
                handlers = zoom.middleware.DEBUGGING_HANDLERS
                runweb(port=args.port, instance=instance, handlers=handlers)
            else:
                runweb(port=args.port, instance=instance, username=args.user)

            print('\rstopped')

    except PermissionError:
        print('PermissionError: is port {} in use?\n'
              'use -p <port> to choose a different port'.format(args.port))

    except OSError:
        print('OSError: is port {} in use?\n'
              'use -p <port> to choose a different port'.format(args.port))

