import logging

from aiomisc import entrypoint
from exchange.services import RestService, ExchangeRatesUpdater
import os


def start():
    rest = RestService(address='0.0.0.0', port=8082)
    rates = ExchangeRatesUpdater(interval=30)
    with entrypoint(rest, rates,
                    pool_size=os.cpu_count()*2 + 1,
                    log_buffer_size=1024,
                    log_format='json',
                    log_flush_interval=0.2,
                    log_config=True,
                    log_level=logging.INFO) as loop:
        loop.run_forever()
