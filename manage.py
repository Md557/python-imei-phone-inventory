import argparse
from etl.raw_file_processor import RawFileProcessor
from utils.logger import get_logger
from db.models import PSQLDriver


def parse_args():
    parser = argparse.ArgumentParser(description='Process raw text file with IMEI/SKU/faults.')
    parser.add_argument('--processes',type=int, default=4, required=False,
                        help='parallel processing - # of processes')
    parser.add_argument('--path', dest='path', type=str, default='input/data.txt',
                        help='path to the input file, e.g. input/data.test.mix.txt')
    parser.add_argument('--log_level', dest='log_level', type=int, default=10,
                        help='log level (10=debug, 20=info, ..). 20 or lower is recommended')
    parser.add_argument('--create_tables', dest='create_tables', action='store_true',
                        help='creates tables')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    logger = get_logger(__name__, level=args.log_level)
    logger.info(f'Starting to read file [{args.path}] with [{args.processes}] processes')
    if args.log_level > 20:
        logger.error('your log level is set too high - you may miss important results.  Suggest info (20) or lower')

    if args.create_tables:
        db_driver = PSQLDriver(log_level=args.log_level)
        db_driver.create_table1()
        db_driver.create_table2()
        db_driver.create_table3()


    processor = RawFileProcessor(path=args.path, processes=args.processes, log_level=args.log_level)
    processor.process()

