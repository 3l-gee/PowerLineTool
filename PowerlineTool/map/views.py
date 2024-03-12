from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from . import mapFunction 
import json

LineStringHandler_instance = mapFunction.LineStringHandler()

def index(request):
    return render(request, 'map/index.html', {'stage_one_instance': "LineStringHandler_instance"})

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


def validation(request):
    successParameters = {
        "value" : False
    }

    if len(LineStringHandler_instance.features) > 0 : 
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

        if point1_id not in LineStringHandler_instance.graphs[point1_source].find_end_nodes() :
            return JsonResponse({'success': False, 'message' : f'you muste fuse at the end of the line, {point1_id} is not at the end of the line {point1_source}'})
        
        if point2_id not in LineStringHandler_instance.graphs[point2_source].find_end_nodes() :
            return JsonResponse({'success': False, 'message' : f'you muste fuse at the end of the line, {point2_id} is not at the end of the line {point2_source}'})

        if LineStringHandler_instance.same_point(point1_source, point1_id, point2_source, point2_id):
            LineStringHandler_instance.fuse(point1_source, point1_id, point2_source, point2_id)
            return JsonResponse({'success': True, 'features': LineStringHandler_instance.features})
        
        return JsonResponse({'success': False})
    
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
    if request.method == 'POST' :
        if len(LineStringHandler_instance.features) != 1: 
            return JsonResponse({'success': False, 
                                 'message' :f'Currently {len(LineStringHandler_instance.features)} feature(s) open, must be reduced to 1.'})
        else : 
            export_file = LineStringHandler_instance.generate_export_files()
            if len(list(export_file.keys())) != 1 :
                return JsonResponse({'success': False, 
                        'message' :f'Currently {len(list(export_file.keys()))} feature(s) open, must be reduced to 1.'})  
            else :
                key = list(export_file.keys())[0]
                return JsonResponse({'success': True,"id" : key,  "dcs" : export_file[key]["dcs"], "history" : export_file[key]["history"]})


# TODO handel export
        
# TODO handel historys