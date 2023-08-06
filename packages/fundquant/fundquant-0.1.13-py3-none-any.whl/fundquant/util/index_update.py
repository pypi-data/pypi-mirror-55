import pymysql

from fundquant.data_get.xq_data import XqApi
from fundquant.util.dateutil import today_plus


def etf_head_complete(code: str, exchange: str = 'SH'):
    code = str(code).zfill(6)

    if code.find('SZ') >= 0 or code.find('SH') >= 0:
        return code

    if code.find('512') == 0 or code.find('510') == 0:
        return 'SH' + code

    if code.find('159') == 0:
        return 'SZ' + code

    if code.find('3') == 0:
        return 'SZ' + code


def tmp():
    conn = pymysql.connect(user='root', password='', database='quant', charset='utf8')
    cursor = conn.cursor()
    sql = "select etf_code, etf_name, index_id, index_name from jsl_etf_list where index_id <> '-' "
    cursor.execute(sql)
    conn.commit()

    for item in cursor.fetchall():
        etf_code = item[0]
        etf_name = item[1]
        index_code = item[2]
        index_name = item[3]

        df = XqApi().get_his_k_data(etf_head_complete(etf_code), today_plus(20 * 360), today_plus(0),
                                    return_column=['date', 'close'])

        for item in df.values:
            print(item)


if __name__ == '__main__':
    tmp()
