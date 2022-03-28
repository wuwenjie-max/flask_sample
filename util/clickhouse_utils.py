from clickhouse_driver import Client, connect

from util.log_utils import sys_logger
from util.setting import BATCH_SIZE, CLICKHOUSE_HOST, CLICKHOUSE_PORT, CLICKHOUSE_DB, CLICKHOUSE_USER, CLICKHOUSE_PASS



def query(sql, batch_lines=BATCH_SIZE):

    with connect(
            host=CLICKHOUSE_HOST,
            port=CLICKHOUSE_PORT,
            user=CLICKHOUSE_USER,
            password=CLICKHOUSE_PASS,
            database=CLICKHOUSE_DB,

    ) as conn:
        cursor = conn.cursor()
        cursor.set_stream_results(True, batch_lines)
        cursor.execute(sql)
        while True:
            res = cursor.fetchmany(batch_lines)
            if res:
                yield res
            else:
                break