from aiohttp import web
from views import *

# Define all routes and views here

# path_to_static_folder = './data'
routes = [
    web.view('/', AddConversionView),
    web.view('/config', ConfigsView),
    web.view('/conversions', ConversionsView),
    # web.view('/conversions_processing', ConversionsProcessingView),
]
