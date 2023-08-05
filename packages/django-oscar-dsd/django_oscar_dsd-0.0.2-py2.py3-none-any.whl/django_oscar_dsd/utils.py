import json
import requests
from decimal import Decimal as D

from django.conf import settings
from oscar.core.loading import get_class, get_classes

from .settings import DSD_USERNAME, DSD_PASSWORD, DSD_LOGIN_URL, DSD_PRODUCTS_URL, DSD_KNOWN_CATEGORIES, \
    DSD_PRODUCT_FIELDS, DSD_PRODUCT_ID_FIELD, REQUEST_HEADERS, REQUEST_TIMEOUT, DJANGO_IS_LOADED

if DJANGO_IS_LOADED:
    ImportingError = get_class('partner.exceptions', 'ImportingError')
    Partner, StockRecord = get_classes('partner.models', ['Partner',
                                                          'StockRecord'])
    ProductClass, Product, Category, ProductCategory = get_classes(
        'catalogue.models', ('ProductClass', 'Product', 'Category',
                             'ProductCategory'))
    create_from_breadcrumbs = get_class('catalogue.categories', 'create_from_breadcrumbs')


def login():
    """
    Login

    :return: session object
    """

    session = requests.Session()
    _res = session.get(DSD_LOGIN_URL, auth=(DSD_USERNAME, DSD_PASSWORD), headers=REQUEST_HEADERS,
                       timeout=REQUEST_TIMEOUT)

    return session


def call_dsd_products_endpoint(session=None, page=0):
    if session is None:
        session = login()

    products_url = DSD_PRODUCTS_URL + '?page={}'.format(page)

    res = session.get(products_url, auth=(DSD_USERNAME, DSD_PASSWORD), headers=REQUEST_HEADERS, timeout=REQUEST_TIMEOUT)

    try:
        res_status_code = res.status_code
        res_body = res.json()

    except:
        res_status_code = None
        res_body = None

    return res_body, res_status_code


def get_dsd_products(page=None):
    """
    List products

    :return: products as list
    """

    products = []
    session = login()

    if page is None:
        page = 0

        res_body, res_status_code = call_dsd_products_endpoint(session, page)

        res_total_pages = int(res_body.get('pagination').get('total_pages'))

        for page in range(1, res_total_pages + 1):
            res_body, res_status_code = call_dsd_products_endpoint(session, page)

            res_products = res_body.get('products')

            products += res_products

    else:
        res_body, res_status_code = call_dsd_products_endpoint(session, page)

        res_products = res_body.get('products')

        products += res_products

    return products


def get_product_parent_category(category_name):
    root_category = settings.OSCAR_DEFAULT_CATEGORY
    category_parent_name = 'Uncategorized'

    if category_name == root_category:
        return category_name, True

    found = False
    for key, children_categories in DSD_KNOWN_CATEGORIES.items():
        print('Getting paret category for "{}"'.format(category_name))
        if found:
            break
        if key == 'DISABLED':
            print('Disabled category "{}"'.format(key))
            continue

        if category_name in children_categories:
            category_parent_name = key
            found = True

    if found:
        return root_category + ' > ' + category_parent_name + ' > ' + category_name, True
    else:
        return root_category + ' > ' + category_parent_name, False


def create_product(product_class, category_str, upc,
                   title, title_fr,
                   description, description_fr,
                   short_description, short_description_fr,
                   image_url, stats):
    # Create item class and item
    product_class, __ \
        = ProductClass.objects.get_or_create(name=product_class)

    try:
        item = Product.objects.get(upc=upc)
        stats['updated_items'] += 1
    except Product.DoesNotExist:
        item = Product()
        stats['new_items'] += 1

    item.product_class = product_class

    item.image_url = image_url

    item.upc = upc
    item.title_en = title
    item.title_fr = title_fr
    item.short_description_en = short_description
    item.short_description_fr = short_description_fr
    item.description_en = description
    item.description_fr = description_fr

    """
    if item.image_url:
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(urlopen(item.image_url).read())
        img_temp.flush()
        item.image_file.save(f"image_{item.pk}", File(img_temp))
    """

    item.save()

    # Category
    cat = create_from_breadcrumbs(category_str)
    ProductCategory.objects.update_or_create(product=item, category=cat)

    print('item created', item)
    return item


def update_product():
    pass


def update_stockrecord(item, partner_name, partner_sku, price_excl_tax, num_in_stock, stats):
    # Create partner and stock record
    partner, _ = Partner.objects.get_or_create(
        name=partner_name)

    stock_records = StockRecord.objects.filter(product=item).order_by('-date_created')

    if stock_records.count() > 0:
        print('Disabling old stocks')
        """
        for _stock in stock_records:
            _stock.num_in_stock = 0
            _stock.save()
        """
    else:
        print('No prev stocks')

    stock = StockRecord()

    stock.product = item
    stock.partner = partner
    stock.partner_sku = partner_sku
    stock.price_excl_tax = D(price_excl_tax)
    stock.num_in_stock = num_in_stock
    stock.save()

    return stock


def fill_in_dsd_product(dsd_product, backend_product):
    for field in DSD_PRODUCT_FIELDS:
        field_value = backend_product.get(field, None)
        if field not in ['dsd_id', 'dsd_options']:
            setattr(dsd_product, field, field_value)

    backend_product_id = backend_product['id']
    backend_product_options = backend_product.get('options', None)

    dsd_product.dsd_id = backend_product_id
    dsd_product.dsd_options = json.dumps(backend_product_options)


def get_dsd_product_updated_fields(dsd_product, backend_product):
    updated_fields = []
    for field in DSD_PRODUCT_FIELDS:
        if field not in ['dsd_id', 'dsd_options']:
            dsd_product_field_value = getattr(dsd_product, field, None)
            backend_product_field_value = backend_product.get(field, None)
            equals = dsd_product_field_value == backend_product_field_value
            # print('{}: {} == {}'.format(field, dsd_product_field_value, backend_product_field_value))
            if not equals:
                updated_fields.append(field)

    dsd_product_options_value = getattr(dsd_product, 'dsd_options', None)
    _backend_product_options_value = backend_product.get('options', None)
    backend_product_options_value = json.dumps(_backend_product_options_value)
    if dsd_product_options_value != backend_product_options_value:
        updated_fields.append('dsd_options')

    return updated_fields


def load_single_dsd_backend_product(backend_dsd_product, publish=True):
    from .models import DSDProduct

    backend_dsd_product_id = backend_dsd_product[DSD_PRODUCT_ID_FIELD]

    query_args = {
        DSD_PRODUCT_ID_FIELD: backend_dsd_product_id
    }

    previous_products = DSDProduct.objects.filter(**query_args)
    already_created = previous_products.count() > 0
    print('previous_products', query_args, previous_products)

    if already_created:
        print('Already created: {}'.format(backend_dsd_product_id))
        dsd_product = previous_products.first()
        updated_fields = get_dsd_product_updated_fields(dsd_product, backend_dsd_product)

        if len(updated_fields) > 0:
            print('Updated fields "{}"'.format(updated_fields))

            for updated_field in updated_fields:
                if updated_field not in ['dsd_id', 'dsd_options']:
                    new_value = backend_dsd_product.get(updated_field)
                    setattr(dsd_product, updated_field, new_value)
                else:
                    print('Updated field', updated_field)
                    if updated_field == 'dsd_id':
                        setattr(dsd_product, updated_field, backend_dsd_product.get('id'))
                    else:
                        updated_product_options = json.dumps(backend_dsd_product.get('options'))
                        setattr(dsd_product, updated_field, updated_product_options)

            dsd_product.save()
        else:
            publish = False

    else:
        print('Creating new {}'.format(backend_dsd_product_id))
        dsd_product = DSDProduct()

        fill_in_dsd_product(dsd_product, backend_dsd_product)

        dsd_product.save()

    if publish:
        try:
            dsd_product.publish()

        except Exception as e:
            print('Can NOT publish "{}" because of "{}"'.format(dsd_product, e))
