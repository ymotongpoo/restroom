# -*- coding: utf-8 -*-


class BoardNotFoundException(Exception):
    '''
    板情報が見つからなかった場合の例外
    '''
    pass


class ThreadNotFoundException(Exception):
    '''
    スレッドが見つからなかった場合の例外
    '''
    pass


class DatExpireException(Exception):
    '''
    スレッドがdat落ちしていた場合の例外
    '''
    pass

