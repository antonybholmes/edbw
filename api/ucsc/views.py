from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
import libhttp
from api.ucsc.models import Track
from api.ucsc.serializers import TrackSerializer
from api import auth

  
def tracks_callback(key, person, user_type, id_map={}):
    ids = id_map['id']

    tracks = Track.objects.filter(sample_id__in=ids) #Track.objects.all() #(id__in=ids)
    
    serializer = TrackSerializer(tracks, many=True, read_only=True)
    
    return JsonResponse(serializer.data, safe=False)    


def tracks(request):
    id_map = libhttp.parse_params(request, {'id':-1, 'key':''})
 
    return auth.auth(request, tracks_callback, id_map=id_map)