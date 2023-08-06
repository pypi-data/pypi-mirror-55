# -*- coding: utf-8 -*-
import tushare as ts
from logbook import Logger, StreamHandler, FileHandler
import sys


class TushareDataset:
    """
    https://tushare.pro/
    文档说明https://tushare.pro/document/1
    token来自 https://tushare.pro/user/token
    """
    @property
    def log(self):
        return self._log

    @property
    def proapi(self):
        return self._proapi

    def __init__(self, log=None):
        if log:
            self._log = log
        else:
            StreamHandler(sys.stdout).push_application()
            self._log = Logger(self.__class__.__name__)
        self.log.info("tushare version: " + ts.__version__)
        self._proapi = ts.pro_api("e4c26b73400a0c0a99881dc1ba7c955dfb6ffd1ab60e70f5989ad7fa")


if __name__ == '__main__':
    ts = TushareDataset()
    data = ts.proapi.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    ts.log.info(data)
    df = ts.proapi.trade_cal(exchange='', start_date='20190201', end_date='20190303',
                               fields='exchange,cal_date,is_open,pretrade_date', is_open='0')
    ts.log.info(df)
