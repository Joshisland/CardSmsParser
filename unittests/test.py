#!/usr/bin/python
# coding: utf-8

import unittest

from sms_parser import get_parser


class ParserTestCase(unittest.TestCase):
    def check_result(self, parser_type, src, expected):
        result = get_parser(parser_type).parse(src)
        for key, value in expected.items():
            self.assertEqual(expected[key], getattr(result, key))

    def test_hyundai_card1(self):
        parser_type = '현대카드'
        src = '[Web발신]\n현대ZERO승인 홍*동\n2,700원 일시불\n08/06 11:01 우산국영재약국\n누적809,286원\n1.0% 적립'
        expected = {'card_name': '현대ZERO', 'name_part': '홍*동', 'amount': 2700, 'installment': '일시불', 'month':
            8, 'day': 6, 'hour': 11, 'minute': 1, 'place': '우산국영재약국', 'accumulated': 809286}
        self.check_result(parser_type, src, expected)

    def test_hyundai_card2(self):
        parser_type = '현대카드'
        src = ('[Web발신]\n'
        '현대카드 ZERO 취소\n'
        '홍*동\n'
        '5,900원 일시불\n'
        '06/24 10:49\n'
        '이주호한의원\n'
        '누적201,090원\n')
        expected = {'card_name': '현대카드 ZERO', 'name_part': '홍*동', 'amount': 5900, 'installment': '일시불', 'month':
            6, 'day': 24, 'hour': 10, 'minute': 49, 'place': '이주호한의원', 'accumulated':
            201090, 'is_cancelled':True}
        self.check_result(parser_type, src, expected)


    def test_woori_card1(self):
        src = '[Web발신]\n우리(3890)승인\n홍*동님\n8,500원 일시불\n08/12 19:11\n풍년옥\n누적1,307,020원'
        result = get_parser('우리카드').parse(src)
        expected = {'card_name': '우리(3890)', 'name_part': '홍*동', 'amount': 8500, 'installment': '일시불', 'month': 8,
                    'day': 12, 'hour': 19, 'minute': 11, 'place': '풍년옥', 'accumulated': 1307020}
        for key, value in expected.items():
            self.assertEqual(expected[key], getattr(result, key))

    def test_woori_card2(self):
        src = '[Web발신]\n우리카드(3890)매출접수\n홍*동님\n32,880원\n07월31일기준\n한국전력전기요금수납'
        result = get_parser('우리카드').parse(src)
        expected = {'card_name': '우리카드(3890)', 'name_part': '홍*동', 'amount': 32880, 'month': 7,
                    'day': 31, 'place': '한국전력전기요금수납'}
        for key, value in expected.items():
            self.assertEqual(expected[key], getattr(result, key))

    def test_woori_bank(self):
        src = '[Web발신]\n우리 09/01 09:45\n3450*01\n출금 5,000원\n페이코제로페이\n잔액 1,111,111원'
        src = '[Web발신]\n우리 09/02 03:48\n*846950\n입금 3,500,000원\n생활비\n잔액 2,222,222원'

    def test_kookmin_card2(self):
        src = '[Web발신] [KB국민카드]홍길동님 08/14 결제금액 41,700원. 잔여포인트리62,199(08/01기준)'




if __name__ == '__main__':
    unittest.main()
