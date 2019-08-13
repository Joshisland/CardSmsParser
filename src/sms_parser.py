#!/usr/bin/python
# coding: utf-8
import re


class SmsParserBase(object):
    def __init__(self):
        pass

    def parse(self, target, debug=False):
        if debug:
            print("target:", target)

        res = self._parse_internal(target)

        if debug:
            for key in ['pattern', 'result', 'group']:
                try:
                    print("%s: %s" % (key, res[key]))
                except KeyError:
                    pass

        return res['result']

    def _parse_internal(self, target):
        pass


def get_parser(typestr):
    """Returns a parser

    :param typestr:
    :return: indicated parser
    """
    if typestr in ["현대", "현대카드", "Hyundai"]:
        return HyundaiCardParser()
    if typestr in ["우리", "우리카드", "Woori"]:
        return WooriCardParser()
    else:
        raise AttributeError("Not supported type:%s" % typestr)


class HyundaiCardParser(SmsParserBase):
    def __init__(self):
        pass

    def _parse_internal(self, target):
        pat = re.compile(r'\[Web발신\]\n'
                         r'(?P<card_name>.*)승인 '
                         r'(?P<name_part>.*)\n'
                         r'(?P<amount>[\d,]*)원 (?P<installment>.*)\n'
                         r'(?P<month>\d*)/(?P<day>\d*) (?P<hour>\d*):(?P<minute>\d*) '
                         r'(?P<place>.*)\n'
                         r'누적(?P<accumulated>[\d,]*)원')
        res = pat.search(target)
        return {'result': res, 'pattern': pat, 'group': res.groupdict()}


class WooriCardParser(SmsParserBase):
    def __init__(self):
        pass

    def _parse_internal(self, target):
        pat = re.compile(r'\[Web발신\]\n'
                         r'(?P<card_name>.*)승인\n'
                         r'(?P<name_part>.*)님\n'
                         r'(?P<amount>[\d,]*)원 (?P<installment>.*)\n'
                         r'(?P<month>\d*)/(?P<day>\d*) (?P<hour>\d*):(?P<minute>\d*)\n'
                         r'(?P<place>.*)\n'
                         r'누적(?P<accumulated>[\d,]*)원')
        res = pat.search(target)
        return {'result': res, 'pattern': pat, 'group': res.groupdict()}
