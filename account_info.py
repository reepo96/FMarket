# encoding:utf-8
import base64
import configparser
import ast
from gmssl import sm4

'''BASE_LOCATION = "."  # 根目录地址
MD_LOCATION = BASE_LOCATION + "\MarketData"  # 行情数据地址
TD_LOCATION = BASE_LOCATION + "\TradingData"  # 交易数据地址
SD_LOCATION = BASE_LOCATION + "\StrategyData"  # 策略数据地址'''
BASE_LOCATION = "d:/flow"
MD_LOCATION = BASE_LOCATION
TD_LOCATION = BASE_LOCATION
SM4_KEY = b"xxxxxxxxxxabcdef" #SM4密钥，必须是16字节


class FutureAccountInfo:
    def __init__(self, accounttype,md_page_dir=MD_LOCATION, td_page_dir=TD_LOCATION):
        config = configparser.ConfigParser()
        config.read('config.ini')

        self.broker_id = config[accounttype]['BrokerID']
        self.server_dict = ast.literal_eval(config[accounttype]['server_dict']) # 服务器地址
        self.reserve_server_dict = ast.literal_eval(config[accounttype]['reserve_server_dict'])  # 备用服务器地址
        self.investor_id = config[accounttype]['InvestorID']  # 账户
        self.password = config[accounttype]['Password']  # 密码
        self.app_id = config[accounttype]['AppID']  # 认证使用AppID
        self.auth_code = config[accounttype]['AuthCode']  # 认证使用授权码
        self.instrument_id_list = ast.literal_eval(config['Sub']['instrument_id_list'])  # 订阅合约列表[]
        self.bar_freq_list =  ast.literal_eval(config['Sub']['bar_freq_list'])  # K线类型列表()
        self.md_page_dir = md_page_dir  # MdApi流文件存储地址，默认MD_LOCATION
        self.td_page_dir = td_page_dir  # TraderApi流文件存储地址，默认TD_LOCATION

        if accounttype == "Real" :
            # 解密
            sm4_cipher = sm4.CryptSM4()
            sm4_cipher.set_key(SM4_KEY, sm4.SM4_DECRYPT)
            self.investor_id = sm4_cipher.crypt_ecb(base64.b64decode(self.investor_id)).decode()
            self.password = sm4_cipher.crypt_ecb(base64.b64decode(self.password)).decode()

        '''print(f'broker_id={self.broker_id},server_dict={self.server_dict},'
              f'reserve_server_dict={self.reserve_server_dict},'
              f'instrument_id_list={self.instrument_id_list},bar_freq_list={self.bar_freq_list}')'''


my_future_account_info_dict = {
    # 交易时间测试
    'SimNow': FutureAccountInfo( 'SimNow' ),
    'Real': FutureAccountInfo( 'Real' ),
}
