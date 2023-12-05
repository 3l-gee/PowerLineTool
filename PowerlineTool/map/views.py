from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import logging
from . import Mapfunctions 

stage_one_instance = Mapfunctions.StageOne()

#TEST
def log_hello(request):
    # Log a message when the button is clicked
    logging.info('Hello, world!')
    return HttpResponse('Logged "Hello, world!"') 

def index(request):
    return render(request, 'map/index.html', {'stage_one_instance': stage_one_instance})

def remFeature(request):
    if request.method == 'POST' :
        stage_one_instance.remFeature()

    return HttpResponse(stage_one_instance.features) 

def log_coordinates(request):
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        latitudeMod, longitudeMod = Mapfunctions.transform_coordinates(3857, 2056, longitude, latitude)

        return JsonResponse({'coordinates': [round(latitudeMod,1), round(longitudeMod,1)], 'status': 'success' })
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid HTTP method'})
    

def addFeature(request): 
    if request.method == 'POST' :
        featureId = request.POST.get('featureId')
        featureType = request.POST.get('featureType')
        if featureType == "TLM" : 
            stage_one_instance.addFeatureTLM(featureId)

            return JsonResponse({'success': True, 'features': stage_one_instance.features})

        elif featureType == "DCS" : 
            stage_one_instance.addFeatureDCS(featureId, request.POST.get('featureData')) 
            
            return HttpResponse(stage_one_instance.features) 

    return HttpResponse(stage_one_instance.features) 

def getFeature(request):
    if request.method == 'GET' :
        
        return JsonResponse({'success': True, 'features': stage_one_instance.features})
    
    return HttpResponse(stage_one_instance.features) 
