#!/usr/bin/python3

import os
import sys
#import base64
#import struct
#import hashlib
import secrets
import argparse
import binascii
from typing import List, TYPE_CHECKING
# from typing import Any, Callable, Iterable, Union, Optional, List, Tuple, Dict

if __name__ == "__main__":
    import requirements # type: ignore
else:
    from . import requirements





def H(x):
    return binascii.hexlify(x).decode("ascii").upper()



def parse_args(inpArgs: List):
    parser = argparse.ArgumentParser(prog="Reqqie", description="the lightweight requirement management guy")
    parser.add_argument("reqfile", type=str, help="main requirement file")
    parser.add_argument("-y", "--yes", action="store_true", help="answer yes to all interactive questions")
    parser.add_argument("-n", "--no",  action="store_true", help="answer no to all interactive questions")
    parser.add_argument("-d", "--dry", action="store_true", help="run dry, ie make no changes")
    parser.add_argument("-u", "--updatesrc", action="store_true", help="update/rewrite the source files")
    parser.add_argument("-v", "--verbose", action="store_true", help="verbose output")
    parser.add_argument("--debug_test", type=int, default=0, help="if set, special debug (logic/printouts) are run. Mainly used during dev")
    parser.add_argument("--indent", default=4, help="indention in output files")
    parser.add_argument("--uidlen", default=18, help="length (bytes) of unique id generator")


    return parser.parse_args(inpArgs)


def main():
    args = parse_args(sys.argv[1:])

    try:
        reqs = requirements.Requirements(args.reqfile)
    except Exception as exc:
        print ("Error:", exc)
        raise Exception()
        # return -1

    reqs.analyze()
    reqs.report_txt()
    if not args.dry:
        reqs.write_back()


if __name__ == "__main__":
    main()
