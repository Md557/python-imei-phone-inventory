import logging
from multiprocessing import Pool
from db.models import InventoryEvents
from typing import List, Dict
from utils.exceptions import EventCodeException, FaultCodeException, InvalidIMEIException
from utils.logger import get_logger
from etl.validators import ImeiValidator


class RawFileProcessor(ImeiValidator):
    def __init__(self, path, log_level=logging.INFO, *args, **kwargs):
        self.path = path
        self.processes = kwargs.get('processes', 4)
        self.processor = Pool(self.processes)
        self.logger = get_logger(str(__class__), level=log_level)
        self.errors = []
        self.inventory = dict()
        self.in_stock_inventory = dict()
        self.fault_codes = dict()


    def process(self):
        self.logger.info(f'starting to process file {self.path}')
        data = self.read_raw_stream()
        records = self.group_records(data)
        self.inventory = self.process_records(records)
        self.process_in_stock_inventory()
        self.display_inventory()
        self.logger.info(f"Fault codes received: {list(self.fault_codes)}")
        self.logger.info(f"Fault codes mapping: {self.fault_codes}")

        if self.errors:
            self.logger.warning(f"{len(self.errors)} Invalid records were found: {self.errors}")
        else:
            self.logger.info("No invalid records were found")


    def read_raw_stream(self):
        self.logger.setLevel(logging.DEBUG)
        with open(self.path, newline='\r\n') as f:
            data = f.readlines()
        if not data:
            return None
        data = [i.strip('\r\n') for i in data]

        self.logger.debug(f'data read as {data}')
        return data


    def group_records(self, data) -> List:
        fault_code = None
        description = None
        event = None
        imei = None
        sku = None
        records = list()
        fault_codes = dict()
        for line in data:
            if not line:
                if not imei:
                    self.logger.warning(f"warning, no imei to store - skipping record, faults={fault_codes}")
                    continue
                valid_imei = self.validate_IMEI(imei)
                records.append({
                    'imei': imei,
                    'valid_imei': valid_imei,
                    'sku': sku,
                    'event': event,
                    'description': description,
                    'faults': fault_codes,
                })
                fault_code, description, event, imei, sku = None, None, None, None, None
                fault_codes = dict()
                continue
            try:
                if len(line) >= 4 and line[0:4] == '    ':
                    self.logger.debug("fault code lines found")
                    line = line.strip('    ')
                    [fault_code, description] = line.split(' ')
                    if not fault_code.isdigit():
                        self.logger.warning(f"invalid fault code {fault_code} - skipping line")
                        raise FaultCodeException("Invalid fault code")
                    fault_codes[int(fault_code)] = description
                else:
                    [event, imei, sku] = line.split(' ')
                    if not self.validate_IMEI(imei):
                        raise InvalidIMEIException(imei)
                if fault_code:
                    self.logger.debug(f"fault: {fault_code}, {description}")
                else:
                    self.logger.debug(f"event: {event}, {imei}, {sku}")
            except Exception as e:
                self.logger.warning(f"Exception {e} occurred - continuing")
                self.errors.append({'record': line, 'exception': e})
                continue

        for item in records:
            self.logger.debug(f"{item}\n")

        return records


    def process_records(self, records: List) -> Dict:
        inventory = dict()

        for item in records:
            if not item['valid_imei']:
                continue
            event = item['event']
            sku = item['sku']
            if item['faults']:
                for k, v in item['faults'].items():
                    self.fault_codes[k] = v
            try:
                value = InventoryEvents[event].value
                inventory[sku] = inventory[sku] + value if sku in inventory.keys() else value
            except KeyError:
                self.logger.warning(f"invalid event found {event}")
                self.errors.append({'record': item, 'exception': EventCodeException(event)})

        return inventory


    def process_in_stock_inventory(self):
        for k, v in self.inventory.items():
            if v > 0:
                self.in_stock_inventory[k] = v


    def display_inventory(self):
        self.logger.info(f'{len(self.inventory)} skus were recorded at the facility.  Some may no longer be at the '
                         'facility.  Details by sku:')
        self.logger.info(self.inventory)
        self.logger.info(f'{len(self.in_stock_inventory)} skus are still at the facility. Inventory details by sku:')
        self.logger.info(self.in_stock_inventory)
