from django.conf.urls import url

#from oscar.core.application import Application

from oscar.core.application import OscarConfig
#from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class DSDDashboardApplication(OscarConfig):
    name = 'django_oscar_dsd.dashboard'
    label = 'dsd_dashboard'
    namespace = 'dashboard'

    verbose_name = _('DSD dashboard')
    default_permissions = ['is_staff', ]
    """
    def ready(self):
        super(DSDDashboardApplication, self).ready()

        from apps.dsd.dashboard.views import DSDProductListView, DSDProductCreateView, DSDProductUpdateView, \
            DSDProductDeleteView

        self.dsd_product_list_view = DSDProductListView
        self.dsd_product_create_view = DSDProductCreateView
        self.dsd_product_update_view = DSDProductUpdateView
        self.dsd_product_delete_view = DSDProductDeleteView

        print('DSDDashboardApplication ready')
    """

    def get_urls(self):
        urls = super(DSDDashboardApplication, self).get_urls()
        print('OLD URLS', urls)

        from .urls import urlpatterns

        """
        urlpatterns = [
            url(r'^products/$', self.dsd_product_list_view.as_view(), name='dsd_product-list'),
            url(r'^products/create/$', self.dsd_product_create_view.as_view(), name='dsd_product-create'),
            url(r'^products/(?P<pk>\d+)/$', self.dsd_product_update_view.as_view(),
                name='dsd_product-update'),
            url(r'^products/(?P<pk>\d+)/delete/$', self.dsd_product_delete_view.as_view(),
                name='dsd_product-delete'),

        ]
        #return urlpatterns
        print('DSDDashboardApplication get_urls', urlpatterns)
        
        """
        return self.post_process_urls(urlpatterns)


#application = DSDDashboardApplication()
