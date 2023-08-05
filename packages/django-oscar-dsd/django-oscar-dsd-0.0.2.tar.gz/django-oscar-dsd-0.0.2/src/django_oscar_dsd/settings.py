try:
    from django.conf import settings

    DJANGO_INSTALLED_APPS = settings.INSTALLED_APPS
    DJANGO_IS_LOADED = True

except:
    DJANGO_INSTALLED_APPS = None
    DJANGO_IS_LOADED = False

    class _Settings():
        pass

    settings = _Settings()


ACTIONS = [
  'list_dsd_products',
  'load_dsd_backend_products',
]

CONTENT_TYPE_HEADER = 'application/json'
REQUEST_HEADERS = {
    'Content-type': CONTENT_TYPE_HEADER
}
REQUEST_TIMEOUT = 30

DSD_LOGIN_URL = getattr(settings, 'DSD_LOGIN_URL', "https://www.dsdeurope.nl/api2s/login.json")
DSD_PRODUCTS_URL = getattr(settings, 'DSD_PRODUCTS_URL', "https://www.dsdeurope.nl/api2s/index.json")

DSD_USERNAME = getattr(settings, 'DSD_USERNAME')
DSD_PASSWORD = getattr(settings, 'DSD_PASSWORD')

DSD_PRODUCT_ID_FIELD = getattr(settings, 'DSD_PRODUCT_ID_FIELD', "productCode")

DSD_NO_IMAGE_URL = getattr(settings, 'DSD_NO_IMAGE_URL', "https://www.dsdeurope.nl/img/products/no-image.jpg")

DSD_PRODUCT_FIELDS = [
    'dsd_id',
    'dsd_options',

    'productCode',
    'price',

    'EAN1',
    'EAN2',

    'supplierSKU',

    'supportInfo',
    'licenceType',

    'brandName',
    'name',
    'nameDefault',

    'image',
    'packshotImage',

    'yearsValid',
    'client_fields',
    'numberOfUsers',

    'stock',
    'acquisitionPrice',
    'client_mandatory',

    'productGroup',

    'downloadCode',

    'downloadLink',
    'shortDownloadLink',

    'directDownloadLink_fr',
    'directDownloadLink_en',
    'directDownloadLink_de',
    'directDownloadLink_es',
    'directDownloadLink_nl',

    'name_fr',
    'name_en',
    'name_de',
    'name_es',
    'name_nl',

    'description_fr',
    'description_en',
    'description_de',
    'description_es',
    'description_nl',

    'shortDescription_en',
    'shortDescription_fr',
    'shortDescription_de',
    'shortDescription_es',
    'shortDescription_nl'
]

DSD_KNOWN_CATEGORIES = {
  "Anti-Virus & Security": [
    "Kaspersky Anti-Virus",
    "BullGuard AntiVirus",
    "BullGuard Internet Security",
    "Trend Micro Internet Security",
    "Trend Micro Antivirus",
    "Trend Micro Maximum Security",
    "Kaspersky Total Security Multi-Device",
    "Panda Antivirus Pro",
    "Panda Global Protection",
    "Panda Internet Security",
    "Avast Internet Security",
    "AVG Anti-Virus",
    "AVG Internet Security",
    "Panda Antivirus Pro",
    "Panda Internet Security",
    "Panda Global Protection",
    "Kaspersky Internet Security for Android",
    "Kaspersky Internet Security Multi-Device",
    "Panda Antivirus Pro",
    "Panda Global Protection",
    "Panda Internet Security",
    "Avast Premier",
    "Kaspersky Internet Security Multi-Device",
    "BullGuard IDentity Protection",
    "Panda Mobile Security",
    "ESET NOD32 Antivirus",
    "Norton Security",
    "Avira Antivirus Pro",
    "Avira Internet Security Suite",
    "Kaspersky Small Office Security AUTO-RENEW",
    "Trend Micro Mobile Security",
    "G Data AntiVirus",
    "G Data Internet Security",
    "G Data Total Security",
    "G Data Security for Android",
    "McAfee AntiVirus",
    "McAfee Internet Security",
    "McAfee LiveSafe",
    "McAfee Total Protection",
    "Kaspersky Safe Kids",
    "Norton Security",
    "ESET Multi-Device Security",
    "ESET Internet Security",
    "Bitdefender Antivirus Plus",
    "Bitdefender Internet Security",
    "Bitdefender Total Security Multi-Device",
    "Bitdefender Mobile Security",
    "Kaspersky Endpoint Security for Business - SELECT",
    "Bitdefender Antivirus for Mac",
    "F-Secure Freedome VPN",
    "F-Secure Safe",
    "F-Secure Total Security & Privacy",
    "Norton WiFi Privacy",
    "F-Secure Internet Security",
    "Bitdefender Family",
    "Norton Utilities",
    "Kaspersky Automated Security Awareness"
  ],
  "Utilities & PC Maintenance": [
    "Iolo System Mechanic",
    "ABBYY Screenshot Reader",
    "Magix Game Control",
    "ABBYY Lingvo for Windows",
    "Acronis Backup",
    "Acronis Backup Advanced",
    "ABBYY FineReader",
    "Acronis True Image"
  ],
  "Business and Office": [
    "Microsoft Office 365",
    "Microsoft Office 2013",
    "Microsoft Office 2016",
    "Microsoft Office 2019"
  ],
  "Mac Software": [
    "ABBYY FineReader MAC",
    "G Data AntiVirus for Mac",
    "Parallels Desktop for Mac"
  ],
  "Operating Systems": [
    "Microsoft Windows 10",
    "Microsoft Windows Server"
  ],
  "Photo, Video & Digital Imaging": [
    "Magix Fastcut",
    "Magix Video Deluxe",
    "Magix Video Easy",
    "Magix Fotostory",
    "Magix Photo & Graphic Designer",
    "VEGAS Movie Studio",
    "Adobe Elements"
  ],
  "Programming & Web Development": [
    "Magix Web Designer"
  ],
  "Music": [
    "Magix Music Maker",
    "Magix Audio Cleaning Lab"
  ],
  "DISABLED": [
    "G Data Solutions pour entreprises",
    "Office 365 Services",
    "Kaspersky Endpoint Security Cloud",
    "Kaspersky Security for Mail Server",
    "Kaspersky Endpoint Security for Business - ADVANCED",
    "Kaspersky Security for Microsoft Office 365",
    "ESET MSP",
    "Kaspersky Hybrid Cloud Security",
    "Bitdefender Cloud Security for MSP",
    "Dropbox Business",
    "Data Deposit Box Backup",
    "Dropsuite Backup",
    "Dropbox Business",
    "RG System Remote Monitoring & Management",
    "CodeTwo Email Signatures pour Office 365",
    "Teamleader",
    "Pulseway Enterprise Server (on premises)",
    "Pulseway SaaS Enterprise Server (hosted)"
  ]
}
