import aws_tools
import logging

states = aws_tools.terminate_all_instances()
logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s: %(asctime)s: %(message)s')
if states is None:
    logging.info(f'No instances are terminated')
