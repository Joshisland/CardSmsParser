#!/usr/env/python
# encoding: utf-8

import os
import sys

from sms_parser import get_parser, ParsingFailedError
from alias import apply_alias


def process_internal(buf, parser):
    # get parser and run
    try:
        res = parser.parse(buf, debug=False)
        return res
    except ParsingFailedError:
        print("ParsingFailed:%s" % buf.replace("\n", "\\n"))
        return


def print_result(res):
    if res:
        print(res.to_str())


def process(fname_input, parser):
    buf = None
    with open(fname_input, "rt") as fin:
        for line in fin:
            if "Web발신" in line:
                buf = line.replace("\\n", "\n")
                res = process_internal(buf, parser)
                apply_alias(res)
                print_result(res)


if __name__ == "__main__":
    filename_txt = sys.argv[1]
    parser = get_parser(sys.argv[2])
    process(filename_txt, parser)
    # filename_csv = filename_txt + '.csv'
