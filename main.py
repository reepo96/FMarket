import ast
import sys
import time

from MysqlDB import MysqlDB
from MyTick import MyTick
if __name__ == '__main__':
    my_db = MysqlDB("localhost", "root", "123456", "fmarket")
    #my_db.createtable('t_market_data_cu1min')
    barlist = []
    '''barlist.append(('cu2309',1,12345678,'cu',1,1,6666.66,5555.55,2222.22,3333.33,8888,7777,12345.67,567.89))
    barlist.append(('cu2309', 2, 12345679, 'cu', 1, 1, 6666.66, 5555.55, 2222.22, 3333.33, 8888, 7777, 12345.67, 567.89))
    barlist.append(
        ('cu2309', 3, 12345680, 'cu', 1, 1, 6666.66, 5555.55, 2222.22, 3333.33, 8888, 7777, 12345.67, 567.89))
    barlist.append(
        ('cu2309', 4, 12345681, 'cu', 1, 1, 6666.66, 5555.55, 2222.22, 3333.33, 8888, 7777, 12345.67, 567.89))
    barlist.append(
        ('cu2309', 5, 12345682, 'cu', 1, 1, 6666.66, 5555.55, 2222.22, 3333.33, 8888, 7777, 12345.67, 567.89))
    my_db.savebar('cu',1,barlist)'''

    #all_data = my_db.getbar('cu','cu2309', 1, 1,0)
    #print(all_data)

    from account_info import my_future_account_info_dict

    future_account = my_future_account_info_dict['Real']

    instrument_id_list = []
    product_id_list = []
    while True:
        try:
            with open('allinstrument.txt', 'r') as file:
                content = file.read()
                instrument_id_list = ast.literal_eval(content)
                break
        except FileNotFoundError:
            print('allinstrument.txt not found')
            time.sleep(1)

    while True:
        try:
            with open('allproduct.txt', 'r') as file:
                content = file.read()
                product_id_list = ast.literal_eval(content)
                break
        except FileNotFoundError:
            print('allproduct.txt not found')
            time.sleep(1)

    #print(instrument_id_list)

    all_tab_list = my_db.get_all_tab()

    #根据合约ID和K线频率（1分钟，5分钟等）创建表格
    for productid in product_id_list:
        for freq in future_account.bar_freq_list:
            tab_name = f"t_market_data_{productid.lower()}{freq}min"

            if tab_name in all_tab_list:
                print(f'table:{tab_name} is exist')
            else:
                print(f'table:{tab_name} is not exist and create it')
                my_db.createtable(tab_name)

    tick_engine = MyTick(future_account.broker_id
                               , future_account.reserve_server_dict['qita1']['MDServer']
                               #, future_account.server_dict['MDServer']
                               , instrument_id_list
                               , None
                               , future_account.investor_id
                               , future_account.password
                                , future_account.md_page_dir)
    tick_engine.setdb(my_db)
    tick_engine.Join()





