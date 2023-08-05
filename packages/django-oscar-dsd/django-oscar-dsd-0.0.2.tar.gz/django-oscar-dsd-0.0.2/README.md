# django-oscar-dsd

Django Oscar DSD integration


## Setup

**settings.py**

```
OSCAR_DASHBOARD_NAVIGATION.append(
    {
        'label': _('DSD'),
        'icon': 'icon-list',
        'children': [
            {
                'label': _('Products'),
                'url_name': 'dashboard:dsd_product-list',
                'access_fn': lambda user, url_name, url_args, url_kwargs: user.is_staff,
            },
        ]
    }
)
```


## Note

This project has been set up using PyScaffold 3.2.1. For details and usage
information on PyScaffold see https://pyscaffold.org/.
