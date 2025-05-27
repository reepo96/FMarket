# encoding:utf-8
from AlgoPlus.CTP.MdApi import TickEngine
from AlgoPlus.ta.time_bar import tick_to_bar
from AlgoPlus.utils.base_field import to_str, to_bytes
from MysqlDB import MysqlDB
from BarPub import BarPub

class MyTick(TickEngine):
    '''def __init__(self, bar_freq_list,broker_id, md_server, subscribe_list, md_queue_list, investor_id, password,
                 flow_path):
        self.bar_freq_list = bar_freq_list
        super().__init__(broker_id,md_server,subscribe_list,md_queue_list,investor_id,password,flow_path)'''

    def setdb(self, db_instance):
        self.db_instance = db_instance

    def init_extra(self):
        # Bar字段
        bar_cache = {
            "DataType": "bardata",
            "BarFreq": 1, #K线频率：1=分钟K线，5=5分钟K线等等
            "InstrumentID": b"",
            "UpdateTime": b"99:99:99",
            "LastPrice": 0.0,
            "HighPrice": 0.0,
            "LowPrice": 0.0,
            "OpenPrice": 0.0,
            "BarVolume": 0,
            "BarTurnover": 0.0,
            "BarSettlement": 0.0,
            "BVolume": 0,
            "SVolume": 0,
            "FVolume": 0,
            "DayVolume": 0,
            "DayTurnover": 0.0,
            "DaySettlement": 0.0,
            "OpenInterest": 0.0,
            "TradingDay": b"99999999",
        }

        from account_info import my_future_account_info_dict
        future_account = my_future_account_info_dict['SimNow']

        self.barpuber = BarPub()
        self.bar_freq_list = future_account.bar_freq_list
        self.bar_dict = {}  # Bar字典容器
        # 遍历订阅列表
        for instrument_id in self.subscribe_list:
            # 将str转为byte
            if not isinstance(instrument_id, bytes):
                instrument_id = to_bytes(instrument_id.encode('utf-8'))

            # 初始化Bar字段
            bar_cache["InstrumentID"] = instrument_id

            #遍历K线类型
            self.bar_dict[instrument_id] = {}
            for bar_freq in self.bar_freq_list:
                self.bar_dict[instrument_id][bar_freq] = bar_cache.copy()

    # ///深度行情通知
    def OnRtnDepthMarketData(self, pDepthMarketData):
        Instrument_dict = self.bar_dict[pDepthMarketData['InstrumentID']]
        #print(f"Instrument_dict={Instrument_dict}")

        if Instrument_dict is None:
            return

        bar_data = next(iter(Instrument_dict.values()))
        last_update_time = bar_data["UpdateTime"]

        #if pDepthMarketData['InstrumentID'] == b'cu2309':
        #    print(f"last_update_time={last_update_time},min{last_update_time[:-2]}|tick_time={pDepthMarketData['UpdateTime']},min{pDepthMarketData['UpdateTime'][:-2]}")

        is_new_1minute = (pDepthMarketData['UpdateTime'][:-2] != last_update_time[:-2]) and pDepthMarketData[
            'UpdateTime'] != b'21:00:00' and last_update_time != b'99:99:99' # 1分钟K线条件

        if pDepthMarketData['InstrumentID'] == b'cu2407':
            print(f"{pDepthMarketData['InstrumentID']},UpdateTime={pDepthMarketData['UpdateTime']},lastime={last_update_time},is_new_1minute={is_new_1minute}")

        is_new_5minute = is_new_1minute and int(pDepthMarketData['UpdateTime'][-5:-3]) % 5 == 0  # 5分钟K线条件
        is_new_10minute = is_new_1minute and int(pDepthMarketData['UpdateTime'][-5:-3]) % 10 == 0  # 10分钟K线条件
        is_new_15minute = is_new_1minute and int(pDepthMarketData['UpdateTime'][-5:-3]) % 15 == 0  # 15分钟K线条件
        is_new_30minute = is_new_1minute and int(pDepthMarketData['UpdateTime'][-5:-3]) % 30 == 0  # 30分钟K线条件
        is_new_hour = is_new_1minute and int(pDepthMarketData['UpdateTime'][-5:-3]) % 60 == 0  # 60分钟K线条件

        #print('is_new_1minute={},is_new_5minute={},is_new_10minute={},is_new_30minute={},is_new_hour={},'.format(is_new_1minute,is_new_5minute,is_new_10minute,is_new_30minute,is_new_hour))

        is_new_time = False
        for bar_freq in self.bar_freq_list:
            bar_data = Instrument_dict[bar_freq]
            bar_data['BarFreq'] = bar_freq
            if bar_freq == 1:
                is_new_time = is_new_1minute
            elif bar_freq == 5:
                is_new_time = is_new_5minute
            elif bar_freq == 10:
                is_new_time = is_new_10minute
            elif bar_freq == 10:
                is_new_time = is_new_15minute
            elif bar_freq == 30:
                is_new_time = is_new_30minute
            elif bar_freq == 60:
                is_new_time = is_new_hour
            else:
                continue

            #if is_new_time:
                #MysqlDB.savebar(self.db_instance,bar_freq,bar_data)
                #self.barpuber.send_tickdata(pDepthMarketData)
                #self.barpuber.senddata(bar_data)

            #没有成交量导致tick_to_bar函数处理出错
            if pDepthMarketData['Volume'] == 0:
                pDepthMarketData['Volume'] = 1
                pDepthMarketData['Turnover'] = 0

            tick_to_bar(bar_data, pDepthMarketData, is_new_time)
