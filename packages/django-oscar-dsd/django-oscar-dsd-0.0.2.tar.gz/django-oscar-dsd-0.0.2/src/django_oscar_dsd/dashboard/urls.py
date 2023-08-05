from django.conf.urls import url


from .views import DSDProductListView, DSDProductCreateView, DSDProductUpdateView, \
    DSDProductDeleteView, DSDProductPublishView


urlpatterns = [
    url(r'^products/$', DSDProductListView.as_view(), name='dsd_product-list'),
    url(r'^products/create/$', DSDProductCreateView.as_view(), name='dsd_product-create'),
    url(r'^products/(?P<pk>\d+)/$', DSDProductUpdateView.as_view(),
        name='dsd_product-update'),
    url(r'^products/(?P<pk>\d+)/delete/$', DSDProductDeleteView.as_view(),
        name='dsd_product-delete'),

    url(r'^products/(?P<pk>\d+)/publish/$', DSDProductPublishView.as_view(),
        name='dsd_product-publish'),

]
