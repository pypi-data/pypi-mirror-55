#!/usr/bin/env python3

import colorful
import yaml
import logging
from argparse import ArgumentParser, RawTextHelpFormatter, ArgumentDefaultsHelpFormatter
import sys
import json
import os

logging.basicConfig(
        format='%(asctime)s %(levelname)-8s: %(message)s',
        level=logging.DEBUG,
        datefmt='%Y-%m-%d %H:%M:%S')



class JSONLogs:
    def __init__(self, arguments):
        self.args = self.__class__.defaults()
        self.args.update(arguments)

        self.output = {}
        numeric_level = getattr(logging, self.args['log_level'].upper(), None)
        logging.getLogger().setLevel(numeric_level)

    @classmethod
    def defaults(cls):
        default_keys = {
            'log_level': 'info',
            'line_format': '{p[@timestamp]:30} {c.red} {p[app]:15} {c.reset} {c.bold} {p[message]}',
        }
        return default_keys

    @classmethod
    def setup_args(cls, arguments):
        parser = ArgumentParser(
                formatter_class=ArgumentDefaultsHelpFormatter,
                description='''

Filter and present JSON streaming logs

'''
        )
        defaults = cls.defaults()
        parser.add_argument('--log-level', help="Logging level", default=defaults['log_level'])
        parser.add_argument('--line-format', '-f', help="PyFormat based line format", default=defaults['line_format'])
        parser.add_argument('--show-format', action='store_true', help="Show current format string and exit")
        parser.add_argument('--any', action='store_true', help="Show content if ANY filter matches rather than ALL")
        parser.add_argument('--show-raw', action='store_true', help="Show raw non-json logs")
        parser.add_argument('filters', nargs='*', help="List of filters")
        _args = vars(parser.parse_args(arguments))
        if os.environ.get('JLOG_FORMAT'):
            _args['line_format'] = os.environ.get('JLOG_FORMAT')
        return _args


    def is_wanted(self, p):
        if self.args['filters'] == []:
            return True

        if self.args.get('any'):
            for i in self.args['filters']:
                if eval(i) is True:
                    return True
            return False
        else:
            for i in self.args['filters']:
                if eval(i) is False:
                    return False
            return True

    def parse_line(self, line):
        try:
            dict = json.loads(line)
            logging.debug('===' + repr(dict))
            if self.is_wanted(dict) is False:
                return

            print(colorful.reset, end='')
            print(self.args['line_format'].format(p=dict, c=colorful))
        except json.decoder.JSONDecodeError:
            if self.args.get('show_raw'):
                if line.endswith('\n'):
                    print(":::" + line[:-1])


    def run(self):
        if self.args.get('show_format'):
            print(self.args['line_format'])
            return

        try:
            for line in iter(sys.stdin.readline, b''):
                self.parse_line(line)
        except KeyboardInterrupt:
            sys.stdout.flush()
            pass


def main():
    args = JSONLogs.setup_args(sys.argv[1:])
    cli = JSONLogs(args)
    try:
        sys.exit(cli.run())
    except RuntimeError as e:
        logging.error(str(e))
        sys.exit(1)


if __name__ == '__main__':
    main()

