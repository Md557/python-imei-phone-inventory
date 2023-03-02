from enum import Enum
import logging
import os
from utils.logger import get_logger


class InventoryEvents(Enum):
    RECV = 1
    SHIP = -1
    SEND = -1


class PSQLDriver:
    dbname = os.environ.get('PSQL_NAME', 'postgres')
    user = os.environ.get('PSQL_USER', 'postgres')
    password = os.environ.get('PSQL_PASSWORD', 'pass12345')
    host = os.environ.get('PSQL_HOST', 'localhost')
    port = os.environ.get('PSQL_PORT', '5432')
    schema = 'imei'
    imei_table = 'imei_data'
    fault_code_table = 'fault_codes'
    faults_table = 'faults'
    options = f'-c search_path={schema}'

    def __init__(self, log_level=logging.INFO, *args, **kwargs):
        self.conn = None
        self.logger = get_logger(str(__class__), level=log_level)
        self.connect()

    def connect(self):
        import psycopg2
        self.conn = psycopg2.connect(host=self.host, port=self.port, dbname=self.dbname, user=self.user,
                                     password=self.password, options=self.options)

    def create_table1(self):
        with self.conn.cursor() as cur:
            cur.execute(
                f"CREATE TABLE IF NOT EXISTS {self.imei_table} ("
                "imei       integer NOT NULL primary key"
                ",sku       varchar(40) NOT NULL"
                ",inventory integer NOT NULL"
                f")"
            )
            self.conn.commit()

    def create_table2(self):
        with self.conn.cursor() as cur:
            cur.execute(
                f"CREATE TABLE IF NOT EXISTS {self.fault_code_table} ("
                "code         integer NOT NULL primary key"
                ",description varchar(80) NOT NULL"
                f")"
            )
            self.conn.commit()


    def create_table3(self):
        with self.conn.cursor() as cur:
            cur.execute(
                f"CREATE TABLE IF NOT EXISTS {self.faults_table} ("
                "code INT"
                ",imei INT"
                f",CONSTRAINT fk_fault_code FOREIGN KEY(code) REFERENCES {self.fault_code_table}(code)"
                f",CONSTRAINT fk_imei FOREIGN KEY(imei) REFERENCES {self.imei_table}(imei)"
                f")"
            )
            self.conn.commit()
