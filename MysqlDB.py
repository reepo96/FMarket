from DBApi import DBApi
import pymysql
class MysqlDB(DBApi):
    def __init__(self, db_ip, usr, passwd, dbname):
        self.conn = pymysql.connect(
            host=db_ip,
            user=usr,
            password=passwd,
            database=dbname,
            charset='utf8'
        )

    def get_all_tab(self):
        sql = 'show TABLES'
        cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute(sql)
        all_tab = []
        tablist = cursor.fetchall()
        for tab in tablist:
            all_tab.append(tab['Tables_in_fmarket'])
        return all_tab
    def createtable(self, tabname):
        sql = "CREATE TABLE IF NOT EXISTS "+ tabname+"  (\
    `InstrumentID` varchar(82) CHARACTER SET gbk COLLATE gbk_chinese_ci NOT NULL,\
    `barfreq` int(5) UNSIGNED NOT NULL,\
    `TradingDay` varchar(10) NOT NULL,\
    `UpdateTime` varchar(10) NOT NULL,\
    `ProductID` varchar(82) CHARACTER SET gbk COLLATE gbk_chinese_ci NOT NULL,\
    `BarType` char(1) CHARACTER SET gbk COLLATE gbk_chinese_ci NOT NULL,\
    `HighestPrice` double NOT NULL,\
    `OpenPrice` double NOT NULL,\
    `LowestPrice` double NOT NULL,\
    `ClosePrice` double NOT NULL,\
    `BarVolume` int(11) NULL DEFAULT NULL,\
    `BarTurnover` double NULL DEFAULT NULL,\
    `BarSettlement` double NULL DEFAULT NULL,\
    `BVolume` int(11) NULL DEFAULT NULL,\
    `SVolume` int(11) NULL DEFAULT NULL,\
    `FVolume` int(11) NULL DEFAULT NULL,\
    `DayVolume` int(11) NULL DEFAULT NULL,\
    `DayTurnover` double NULL DEFAULT NULL,\
    `DaySettlement` double NULL DEFAULT NULL,\
    `OpenInterest` double NULL DEFAULT NULL,\
    PRIMARY KEY(`InstrumentID`, `barfreq`, `TradingDay`, `UpdateTime`) USING BTREE,\
    INDEX `IDX_"+tabname+"_INSTRUMENTID`(`InstrumentID`) USING BTREE\
    ) ENGINE = InnoDB CHARACTER SET = gbk COLLATE = gbk_chinese_ci ROW_FORMAT = Dynamic;"
        cursor = self.conn.cursor()
        cursor.execute(sql)
        self.conn.commit()

    def savebar(self, barfreq, bar_cache):
        productid = bar_cache['InstrumentID'][:-4]
        print(f"savebar,productid={productid},barfreq={barfreq}")
        sql = f"insert into t_market_data_{productid.decode('utf-8')}{barfreq}min values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor = self.conn.cursor()
        cursor.execute(sql, (
            bar_cache['InstrumentID'],
            barfreq,
            bar_cache['TradingDay'],
            bar_cache['UpdateTime'],
            productid,
            1,  #1-分钟，2-小时，3-日，4-周，5-月
            bar_cache['HighPrice'],
            bar_cache['OpenPrice'],
            bar_cache['LowPrice'],
            bar_cache['LastPrice'],
            bar_cache['BarVolume'],
            bar_cache['BarTurnover'],
            bar_cache['BarSettlement'],
            bar_cache['BVolume'],
            bar_cache['SVolume'],
            bar_cache['FVolume'],
            bar_cache['DayVolume'],
            bar_cache['DayTurnover'],
            bar_cache['DaySettlement'],
            bar_cache['OpenInterest']
        ))
        self.conn.commit()

    def getbar(self, productid, instrumentid, freq, beginDay, endDay):
        sql = ""
        cursor = self.conn.cursor()
        if (endDay > 0):
            sql = f"select * from t_market_data_{productid}{freq}min where InstrumentID = %s and TradingDay >= %s and TradingDay <= %s order by TradingDay,UpdateTime;"
            cursor.execute(sql,(instrumentid,beginDay,endDay))
        else:
            sql = f"select * from t_market_data_{productid}{freq}min where InstrumentID = %s and TradingDay >= %s order by TradingDay,UpdateTime;"
            cursor.execute(sql, (instrumentid, beginDay))

        all_data = cursor.fetchall()
        return all_data

