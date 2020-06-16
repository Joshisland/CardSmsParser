"""Alias for card/account"""

alias: dict = {
    "*123456": "생활비계좌",
    "*234557": "용돈계좌",
    "1234*56": "월급계좌",
    "우리카드(1234)": "카드1",
    "우리(1234)": "카드1",
    "우리카드(2345)": "카드3",
}


def apply_alias(data):
    try:
        replaced = alias.get(data.account_no, None)
        if replaced:
            data.account_no = replaced
        return
    except AttributeError as err:
        pass

    try:
        replaced = alias.get(data.card_name, None)
        if replaced:
            data.card_name = replaced
        return
    except AttributeError:
        pass
