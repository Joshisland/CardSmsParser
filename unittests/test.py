#!/usr/bin/python
# coding: utf-8

import unittest

from sms_parser import get_parser


class ParserTestCase(unittest.TestCase):
    def test_hyundai_card1(self):
        src = '[Web발신]\n현대ZERO승인 홍*동\n2,700원 일시불\n08/06 11:01 우산국영재약국\n누적809,286원\n1.0% 적립'
        result = get_parser('현대카드').parse(src).groupdict()
        expected = {'card_name': '현대ZERO', 'name_part': '홍*동', 'amount': '2,700', 'installment': '일시불', 'month':
            '08', 'day': '06', 'hour': '11', 'minute': '01', 'place': '우산국영재약국', 'accumulated': '809,286'}
        self.assertEqual(result, expected)

    def test_woori_card1(self):
        src = '[Web발신]\n우리(3890)승인\n홍*동님\n8,500원 일시불\n08/12 19:11\n풍년옥\n누적1,307,020원'
        result = get_parser('우리카드').parse(src).groupdict()
        expected = {'card_name': '우리(3890)', 'name_part': '홍*동', 'amount': '8,500', 'installment': '일시불', 'month': '08',
                    'day': '12', 'hour': '19', 'minute': '11', 'place': '풍년옥', 'accumulated': '1,307,020'}
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
