from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import logging
from . import mapFunctions 
import json

stage_one_instance = mapFunctions.StageOne()



#TEST
def log_hello(request):
    # Log a message when the button is clicked
    logging.info('Hello, world!')
    return HttpResponse('Logged "Hello, world!"') 

def index(request):
    return render(request, 'map/index.html', {'stage_one_instance': stage_one_instance})

def remFeature(request):
    if request.method == 'POST' :
        data = json.loads(request.body)
        featureId = data.get('featureId')
        if featureId == "null" : 
            stage_one_instance.remFeatures()
            return JsonResponse({'success': True, 'features': stage_one_instance.features})
        else : 
            stage_one_instance.remFeature(featureId)
            return JsonResponse({'success': True, 'features': stage_one_instance.features})

def log_coordinates(request):
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        latitudeMod, longitudeMod = mapFunctions.transform_coordinates(3857, 2056, longitude, latitude)

        return JsonResponse({'coordinates': [round(latitudeMod,1), round(longitudeMod,1)], 'status': 'success' })
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid HTTP method'})
    

def addFeature(request): 
    if request.method == 'POST' :
        data = json.loads(request.body)
        featureId = data.get('featureId')
        featureType = data.get('featureType')
        featureData = data.get('featureData')

        if featureType == "TLM" : 
            stage_one_instance.addFeatureTLM(featureId)

            return JsonResponse({'success': True, 'features': stage_one_instance.features})

        elif featureType == "DCS" : 
            stage_one_instance.addFeatureDCS(featureId, featureData) 
            
            return JsonResponse({'success': True, 'features': stage_one_instance.features})

    return HttpResponse(stage_one_instance.features) 

def getFeature(request):
    if request.method == 'GET' :
        return JsonResponse({'success': True, 'features': stage_one_instance.features})
    
    return HttpResponse(stage_one_instance.features) 


def validateStepOne(request):
    successParameters = {
        "value" : False, 
        "continuous" : False,
    }

    if len(stage_one_instance.features) > 0 : 
        successParameters["value"] = True

    #Todo
    if True : 
        successParameters["continuous"] = True

    return JsonResponse({'success': all(successParameters.values()), 'features': stage_one_instance.features})

def validateStepTwo(request):
    if request.method == 'POST' :
        data = json.loads(request.body)
        featureId = data.get('featureId')
        featureType = data.get('featureType')
        featureData = data.get('featureData')

        successParameters = {
            "value" : False, 
        }
            
        stage_two_instance = mapFunctions.StageTow(request)

        #Todo
        if True : 
            successParameters["value"] = True

        return JsonResponse({'success': all(successParameters.values()), 'features': stage_one_instance.features})