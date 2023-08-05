import json
import logging

from .utils import get_dsd_products, load_single_dsd_backend_product

logger = logging.getLogger('dsd.functions')


def list_dsd_products(page=None, logger=logger):
    return get_dsd_products(page)


def load_dsd_backend_products(limit=None, publish=True, logger=logger):
    try:
        loaded_dsd_products = 0

        dsd_products = get_dsd_products()

        for p in dsd_products:
            if limit is not None:
                if loaded_dsd_products == limit:
                    break

            dsd_product = p.get('ProductArray')

            #ok = input("press a key to continue:")
            #print('ok', ok)

            load_single_dsd_backend_product(dsd_product, publish)
            loaded_dsd_products += 1

        return loaded_dsd_products

    except:
        logger.error('load_dsd_backend_products', exc_info=True)
        raise
