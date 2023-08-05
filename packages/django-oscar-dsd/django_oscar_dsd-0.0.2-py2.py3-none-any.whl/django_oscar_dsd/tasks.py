from celery import shared_task
from celery.utils.log import get_task_logger

from .functions import load_dsd_backend_products as _load_dsd_backend_products

logger = get_task_logger('dsd.tasks')


def base_task(f, **kwargs):
    errors = []
    result = None

    try:
        result = f(**kwargs)

    except Exception as e:
        if hasattr(e, 'message'):
            msg = e.message
        else:
            msg = str(e)

        print('Task failed "{}"'.format(msg))
        logger.exception(msg)
        errors.append(msg)

    ret = {
        'data': {
            'result': result
        },
        'meta': {
            'status': 'OK' if len(errors) == 0 else 'ERROR',
            'errors': {}
        }
    }
    ret['meta']['errors'] = errors

    return ret


@shared_task(bind=True)
def load_dsd_backend_products(self, **kwargs):
    return base_task(_load_dsd_backend_products, **kwargs)
