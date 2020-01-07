from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from django.core.paginator import Paginator
from api.users.serializers import UserSerializer
from login.models import User
from api import auth, views
from edbw import settings
import libhttp

def users_callback(key, person, user_type, id_map={}):
    if 'page' in id_map:
        page = id_map['page']
    else:
        page = -1
    
    records = min(id_map['records'], settings.MAX_RECORDS_PER_PAGE)

    if 'id' in id_map:
        ids = id_map['id']
        
        rows = User.objects.filter(id__in=ids).values('json')
    else:
        rows = User.objects.all().values('json')
    
    paginator = Paginator(rows, records)
     
    if page > 0:
        return views.json_page_resp('persons', page, paginator) #JsonResponse({'page':page, 'pages':paginator.num_pages, 'persons':[x['json'] for x in page_rows]}, safe=False)
    else:
        return views.json_resp(paginator.get_page(1))


def users(request):
    id_map = libhttp.ArgParser() \
        .add('key') \
        .add('id', multiple=True) \
        .add('page', arg_type=int) \
        .add('records', default_value=settings.DEFAULT_RECORDS) \
        .parse(request)
 
    return auth.auth(request, users_callback, id_map=id_map)
