import sys
import argparse
import datetime as dt
from amapi.AmDistributions import AmDistributions
from amapi.AmAttributions import AmAttributions

def valid_date(s):
    try:
        return dt.datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)

def dist(args):
    AmDistributions(args).report()

def attr(args):
    AmAttributions(args).report()

def build_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "report_mnemonic",
        help="produce the report specified here",
        choices=["dist","attr"]
        )
    parser.add_argument(
        "-u",
        "--username",
        help="username for authentication"
        )
    parser.add_argument(
        "-p",
        "--password",
        help="password for authentication"
        )
    parser.add_argument(
        "-A",
        "--app",
        help="app key to report on"
        )
    parser.add_argument(
        "-V",
        "--vendor",
        help="vendor key to report on"
        )
    parser.add_argument(
        "-b",
        "--begdate",
        help="beginning date for report yyyy-mm-dd",
        type=valid_date
        )
    parser.add_argument(
        "-e",
        "--enddate",
        help="ending date for report yyyy-mm-dd",
        default=dt.datetime.utcnow(),
        type=valid_date
        )
    parser.add_argument(
        "-d",
        "--t_minus_days",
        help="# of days backward to report",
        default=30,
        type=int
        )
    parser.add_argument(
        "-v",
        "--verbosity",
        action="count",
        help="enable verbose output to print details of input records",
        default=0
        )
    return parser

def main():
    args = build_arg_parser().parse_args()
    this = sys.modules[__name__]
    getattr(this, args.report_mnemonic)(args)

if __name__ == '__main__':
    main()
