import os

settings = {
    'host': os.environ.get('ACCOUNT_HOST', 'https://pettobot.documents.azure.com:443/'),
    'master_key': os.environ.get('ACCOUNT_KEY', '7gv2zATVBayM7F6zpaoHH4EnVZMCEU7aveXIGIe0coyCeO9JdyPDXkzKhGifIGRPs1vG8EfgMx25ACDbC6KxsQ=='),
    'database_id': os.environ.get('COSMOS_DATABASE', 'petbot'),
    'container_id': os.environ.get('COSMOS_CONTAINER', 'PB'),
}