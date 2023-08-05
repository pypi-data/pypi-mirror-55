import time

from django.db import models
from django.utils import timezone
from django.conf import settings

from oscar.core.loading import get_class, get_model

from .backend.models import CreatedAtModel, UpdatableModel, PublicableModel

from .utils import get_product_parent_category, create_product, update_stockrecord

from .settings import DSD_NO_IMAGE_URL

create_from_breadcrumbs = get_class('catalogue.categories', 'create_from_breadcrumbs')
Product = get_model('catalogue', 'Product')


class AbstractDSDProduct(models.Model):
    class Meta:
        abstract = True

    dsd_id = models.CharField(max_length=255, null=True, blank=True) # id
    dsd_options = models.TextField(null=True, blank=True) # options

    productCode = models.CharField(max_length=255, null=True, blank=True)
    price = models.CharField(max_length=255, null=True, blank=True)

    EAN1 = models.TextField(null=True, blank=True)
    EAN2 = models.TextField(null=True, blank=True)

    supplierSKU = models.CharField(max_length=255, null=True, blank=True)

    supportInfo = models.TextField(null=True, blank=True)
    licenceType = models.CharField(max_length=255, null=True, blank=True)

    brandName = models.CharField(max_length=255, null=True, blank=True)

    name = models.CharField(max_length=255, null=True, blank=True)
    nameDefault = models.CharField(max_length=255, null=True, blank=True)

    image = models.URLField(null=True, blank=True)
    packshotImage = models.URLField(null=True, blank=True)

    yearsValid = models.CharField(max_length=255, null=True, blank=True)
    client_fields = models.TextField(null=True, blank=True)
    numberOfUsers = models.CharField(max_length=255, null=True, blank=True)

    stock = models.CharField(max_length=255, null=True, blank=True)

    acquisitionPrice = models.FloatField(null=True, blank=True)
    client_mandatory = models.BooleanField(null=True, blank=True)

    productGroup = models.CharField(max_length=255, null=True, blank=True)

    downloadCode = models.CharField(max_length=255, null=True, blank=True)

    downloadLink = models.URLField(null=True, blank=True)
    shortDownloadLink = models.URLField(null=True, blank=True)

    directDownloadLink_fr = models.URLField(null=True, blank=True)
    directDownloadLink_en = models.URLField(null=True, blank=True)
    directDownloadLink_de = models.URLField(null=True, blank=True)
    directDownloadLink_es = models.URLField(null=True, blank=True)
    directDownloadLink_nl = models.URLField(null=True, blank=True)
    directDownloadLink = models.URLField(null=True, blank=True) # modeltranslation

    name_fr = models.CharField(max_length=255, null=True, blank=True)
    name_en = models.CharField(max_length=255, null=True, blank=True)
    name_de = models.CharField(max_length=255, null=True, blank=True)
    name_es = models.CharField(max_length=255, null=True, blank=True)
    name_nl = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True) # modeltranslation

    description_fr = models.TextField(null=True, blank=True)
    description_en = models.TextField(null=True, blank=True)
    description_de = models.TextField(null=True, blank=True)
    description_es = models.TextField(null=True, blank=True)
    description_nl = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True) # modeltranslation

    shortDescription_en = models.TextField(null=True, blank=True)
    shortDescription_fr = models.TextField(null=True, blank=True)
    shortDescription_de = models.TextField(null=True, blank=True)
    shortDescription_es = models.TextField(null=True, blank=True)
    shortDescription_nl = models.TextField(null=True, blank=True)
    shortDescription = models.TextField(null=True, blank=True)  # modeltranslation


class DSDProduct(AbstractDSDProduct, CreatedAtModel, UpdatableModel, PublicableModel):
    class Meta:
        verbose_name = "DSD Product"

    # foreign
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL, related_name="dsd_product")

    def publish(self):
        linked_products = Product.objects.filter(dsd_product=self)
        updated = linked_products.count() > 0

        if updated:
            print('Updated')
        else:
            print('New')

        print('publishing product "{}"'.format(self))

        title = getattr(self, 'name', None)
        title_en = title
        title_fr = getattr(self, 'name_fr', None)

        description = getattr(self, 'description_en', None)
        description_en = description
        description_fr = getattr(self, 'description_fr', None)

        short_description = getattr(self, 'shortDescription_en', None)
        short_description_en = short_description
        short_description_fr = getattr(self, 'shortDescription_fr', None)

        image_url = getattr(self, 'image', None)
        if image_url == DSD_NO_IMAGE_URL:
            image_url = None

        upc = getattr(self, 'productCode', None)
        sku = getattr(self, 'supplierSKU', None)

        product_group = getattr(self, 'productGroup', settings.OSCAR_DEFAULT_CATEGORY)

        stats = {
            'new_items': 0,
            'updated_items': 0
        }

        price_excl_tax = getattr(self, 'price', None)

        if 0 in [len(title), len(description)] or price_excl_tax == "0.00":
            print('CAN NOT PUBLISH')
        else:
            print('title', title_en)
            print('description', description_en)
            print('title_fr', title_fr)
            print('description_fr', description_fr)
            print('image', image_url)

            _category_str, _category_found = get_product_parent_category(product_group)

            if _category_found:
                if updated:
                    _product = self.product
                    _product.image_url = image_url
                    _product.save()
                else:
                    _product = create_product(settings.OSCAR_DEFAULT_CATEGORY, _category_str, upc, title_en, title_fr,
                                              description_en, description_fr, short_description_en, short_description_fr,
                                              image_url, stats)

                    self.is_public = True
                    self.product = _product
                    self.save()

                # stock

                time_string = timezone.now().strftime("%Y-%m-%d-%H-%M-%S")

                stock_record_sku = "{}-{}".format(sku, time_string)

                _stock = update_stockrecord(_product, 'DSD', stock_record_sku, price_excl_tax, 500, stats)

                print('created stock "{}"'.format(_stock))


            else:
                print('NOT publishing because of category "{}"'.format(_category_str))
