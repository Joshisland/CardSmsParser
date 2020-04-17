#!/usr/bin/python
# coding: utf-8
import re
from collections import namedtuple


class ParsingFailedError(Exception):
    pass


class ParsedResultBase(object):
    """Default values"""

    def __init__(self):
        self.installment = "일시불"
        self.hour = 3
        self.minute = 30
        self.is_cancelled = False


class ParsedResult(ParsedResultBase):
    def __init__(self, data):
        super(ParsedResult, self).__init__()
        for key, value in data.items():
            setattr(self, key, self._wrap(value))

    def __str__(self):
        return ",".join([str(data) for data in self.__dict__.values()])

    def to_str(self):
        # 2019. 6. 2 오후 11:03:00
        ampm = "오전" if self.hour < 12 else "오후"
        date = "2019. %s. %s %s %s:%s:00" % (
            self.month,
            self.day,
            ampm,
            self.hour % 12,
            self.minute,
        )
        try:
            category = self.in_out
        except:
            category = "카드구매"
        try:
            name = self.card_name
        except:
            name = self.account_no
        datalist = [date, self.place, "", "", date, self.amount, category, name]
        if self.is_cancelled:
            datalist.append("CANCEL")
        return ",".join(map(str, datalist))

    def _wrap_value(self, value):
        """Convert comma separated number in string into int or float"""
        if isinstance(value, str):
            temp = value.replace(",", "")
            try:
                return int(temp) if int(temp) == float(temp) else float(temp)
            except ValueError:
                pass
        return value

    def _wrap(self, value):
        """Recursively convert data structure"""
        if isinstance(value, (tuple, list, set, frozenset)):
            return type(value)([self._wrap(v) for v in value])
        else:
            return (
                ParsedResult(value)
                if isinstance(value, dict)
                else self._wrap_value(value)
            )


class Struct(object):
    """Comment removed"""

    def __init__(self, data):
        for name, value in data.iteritems():
            setattr(self, name, self._wrap(value))

    def _wrap(self, value):
        if isinstance(value, (tuple, list, set, frozenset)):
            return type(value)([self._wrap(v) for v in value])
        else:
            return Struct(value) if isinstance(value, dict) else value


class SmsParserBase(object):
    def __init__(self):
        pass

    def parse(self, target, debug=False):
        if debug:
            print("target:%s" % target)

        res = self._parse_internal(target)
        try:
            return ParsedResult(res["group"])
        except TypeError as err:
            raise ParsingFailedError()

        if debug:
            for key in ["pattern", "result", "group"]:
                try:
                    print("%s: %s" % (key, res[key]))
                except KeyError:
                    pass

        return res["result"]

    def _parse_internal(self, target):
        pass


def get_parser(typestr):
    """Returns a parser

    :param typestr:
    :return: indicated parser
    """
    if typestr in ["현대", "현대카드", "Hyundai"]:
        return HyundaiCardParser()
    elif typestr in ["우리", "우리카드", "Woori"]:
        return WooriCardParser()
    elif typestr in ["우리은행", "wooribank"]:
        return WooriBankParser()
    elif typestr in ["국민카드", "국민", "kookmin", "KookminCard"]:
        return KookminCardParser()
    else:
        raise AttributeError("Not supported type:%s" % typestr)


class HyundaiCardParser(SmsParserBase):
    def __init__(self):
        pass

    def _parse_internal(self, target):
        pat = re.compile(
            r"\[Web발신\]\n"
            r"(?P<card_name>.*)승인 "
            r"(?P<name_part>.*)\n"
            r"(?P<amount>[\d,]*)원 (?P<installment>.*)\n"
            r"(?P<month>\d*)/(?P<day>\d*) (?P<hour>\d*):(?P<minute>\d*) "
            r"(?P<place>.*)\n"
            r"누적(?P<accumulated>[\d,]*)원"
        )
        res = pat.search(target)
        if res:
            return {"result": res, "pattern": pat, "group": res.groupdict()}

        cancel_pat = re.compile(
            r"\[Web발신\]\n"
            r"(?P<card_name>.*) 취소\n"
            r"(?P<name_part>.*)\n"
            r"(?P<amount>[\d,]*)원 (?P<installment>.*)\n"
            r"(?P<month>\d*)/(?P<day>\d*) (?P<hour>\d*):(?P<minute>\d*)\n"
            r"(?P<place>.*)\n"
            r"누적(?P<accumulated>[\d,]*)원"
        )
        res = cancel_pat.search(target)
        if res:
            groupdict = res.groupdict()
            groupdict["is_cancelled"] = True
            return {"result": res, "pattern": cancel_pat, "group": groupdict}


class WooriCardParser(SmsParserBase):
    def __init__(self):
        pass

    def _parse_internal(self, target):
        pat = re.compile(
            r"\[Web발신\]\n"
            r"(?P<card_name>.*)승인\n"
            r"(?P<name_part>.*)님\n"
            r"(?P<amount>[\d,]*)원 (?P<installment>.*)\n"
            r"(?P<month>\d*)/(?P<day>\d*) (?P<hour>\d*):(?P<minute>\d*)\n"
            r"(?P<place>.*)\n"
            r"누적(?P<accumulated>[\d,]*)원"
        )
        res = pat.search(target)
        if res:
            return {"result": res, "pattern": pat, "group": res.groupdict()}

        pat = re.compile(
            r"\[Web발신\]\n"
            r"(?P<card_name>.*)승인\n"
            r"(?P<name_part>.*)님\n"
            r"(?P<amount>[\d,]*)원 (?P<installment>.*)\n"
            r"(?P<month>\d*)/(?P<day>\d*) (?P<hour>\d*):(?P<minute>\d*)\n"
            r"(?P<place>.*)\n"
            r"POINT(?P<point>[\d,]*)점 사용\n"
        )
        res = pat.search(target)
        if res:
            return {"result": res, "pattern": pat, "group": res.groupdict()}

        pat = re.compile(
            r"\[Web발신\]\n"
            r"(?P<card_name>.*)매출접수\n"
            r"(?P<name_part>.*)님\n"
            r"(?P<amount>[\d,]*)원\n"
            r"(?P<month>\d*)월(?P<day>\d*)일기준\n"
            r"(?P<place>.*)"
        )
        res = pat.search(target)
        if res:
            return {"result": res, "pattern": pat, "group": res.groupdict()}

        pat = re.compile(
            r"\[Web발신\]\n"
            r"(?P<card_name>.*)승인취소\n"
            r"(?P<name_part>.*)님\n"
            r"(?P<amount>[\d,]*)원\n"
            r"(?P<month>\d*)/(?P<day>\d*) (?P<hour>\d*):(?P<minute>\d*)\n"
            r"(?P<place>.*)\n"
        )
        res = pat.search(target)
        if res:
            groupdict = res.groupdict()
            groupdict["is_cancelled"] = True
            return {"result": res, "pattern": pat, "group": groupdict}


class KookminCardParser(SmsParserBase):
    def __init__(self):
        pass

    def _parse_internal(self, target):
        pat = re.compile(
            r"\[Web발신\]\n"
            r"KB국민카드(?P<card_name>.*)승인\n"
            r"(?P<name_part>.*)\n"
            r"(?P<amount>[\d,]*)원 (?P<installment>.*)\n"
            r"(?P<month>\d*)/(?P<day>\d*) (?P<hour>\d*):(?P<minute>\d*)\n"
            r"(?P<place>.*)\n"
            r"누적(?P<accumulated>[\d,]*)원"
        )
        res = pat.search(target)
        if res:
            return {"result": res, "pattern": pat, "group": res.groupdict()}


class WooriBankParser(SmsParserBase):
    def __init__(self):
        pass

    def _parse_internal(self, target):
        pat = re.compile(
            r"\[Web발신\]\n"
            r"우리 (?P<month>\d*)/(?P<day>\d*) (?P<hour>\d*):(?P<minute>\d*)\n"
            r"(?P<account_no>.*)\n"
            r"(?P<in_out>.*) (?P<amount>[\d,]*)원\n"
            r"(?P<place>.*)\n"
            r"잔액 (?P<balance>.*)원\n"
        )
        res = pat.search(target)
        if res:
            return {"result": res, "pattern": pat, "group": res.groupdict()}
