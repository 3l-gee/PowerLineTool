from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from . import mapFunction 
import json

LineStringHandler_instance = mapFunction.LineStringHandler()

def index(request):
    return render(request, 'map/index.html', {'stage_one_instance': LineStringHandler_instance})

def remFeature(request):
    if request.method == 'POST' :
        data = json.loads(request.body)
        featureId = data.get('featureId')
        if featureId == "null" : 
            LineStringHandler_instance.remFeatures()
            return JsonResponse({'success': True, 'features': LineStringHandler_instance.features})
        else : 
            LineStringHandler_instance.remFeature(featureId)
            return JsonResponse({'success': True, 'features': LineStringHandler_instance.features})

def log_coordinates(request):
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        latitudeMod, longitudeMod = mapFunction.transform_coordinates(3857, 2056, longitude, latitude)

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
            LineStringHandler_instance.addFeatureTLM(featureId)

            return JsonResponse({'success': True, 'features': LineStringHandler_instance.features})

        elif featureType == "DCS" : 
            LineStringHandler_instance.addFeatureDCS(featureId, featureData) 
            
            return JsonResponse({'success': True, 'features': LineStringHandler_instance.features})

    return HttpResponse(LineStringHandler_instance.features) 

def getFeature(request):
    if request.method == 'GET' :
        return JsonResponse({'success': True, 'features': LineStringHandler_instance.features})
    
    return HttpResponse(LineStringHandler_instance.features) 


def validateStepOne(request):
    successParameters = {
        "value" : False, 
        "continuous" : False,
    }

    if len(LineStringHandler_instance.features) > 0 : 
        successParameters["value"] = True

    #Todo
    if True : 
        successParameters["continuous"] = True

    return JsonResponse({'success': all(successParameters.values()), 'features': LineStringHandler_instance.features})

def validateStepTwo(request):
    if request.method == 'POST' :
        data = json.loads(request.body)
        featureId = data.get('featureId')
        featureType = data.get('featureType')
        featureData = data.get('featureData')

        successParameters = {
            "value" : False, 
        }
            
        stage_two_instance = mapFunction.StageTow(request)

        #Todo
        if True : 
            successParameters["value"] = True

        return JsonResponse({'success': all(successParameters.values()), 'features': LineStringHandler_instance.features})
    

def fuse(request):
    if request.method == 'POST' :
        # TODO handel unfusable cases (not last point)
        # JsonResponse

        data = json.loads(request.body)
        point1_id = data["points"][0]["id"]
        point1_source = data["points"][0]["source"]
        point2_id = data["points"][1]["id"]
        point2_source = data["points"][1]["source"]

        if LineStringHandler_instance.same_point(point1_source, point1_id, point2_source, point2_id):
            LineStringHandler_instance.fuse(point1_source, point1_id, point2_source, point2_id)
            return JsonResponse({'success': True, 'features': LineStringHandler_instance.features})
        
        return JsonResponse({'success': False, 'features': LineStringHandler_instance.features})
    
def divide(request):
    if request.method == 'POST' :
        # TODO handel undividable cases (last point)
        # JsonResponse

        data = json.loads(request.body)
        point_id = data["points"][0]["id"]
        point_source = data["points"][0]["source"]
        LineStringHandler_instance.divide(point_source, point_id)
        return JsonResponse({'success': True, 'features': LineStringHandler_instance.features})


def export(request): 
    return print(request)

# TODO handel export
        
# TODO handel history