from django.shortcuts import render, redirect
from TransitData.GTFS import GTFS
from .forms import stationForm
import time
from django.core.signals import request_finished
from django.http import JsonResponse
# Create your views here.

def home_view(request):
    context = {}
    return render(request, "home_page.html", context)

def alarm_view(request):
    form = stationForm(request.POST or None)
    if form.is_valid():
        request.session['currentStation'] = request.POST['currentStation']
        request.session['destinationStation'] = request.POST['destinationStation']
        request.session['endpoint'] = request.POST['endpoint']
        return redirect("active/")
        
    context = {'form': form}
    return render(request, "alarm_page.html", context)

def active_view(request):
    context = {'data': request.session['currentStation']}
    return render(request,"active_page.html", context)

def finished_view(request):
    return render(request,"finished_page.html")

def getTimingData(request):
    currentStation = request.session['currentStation']
    currentStationID = GTFS.getStationID(currentStation)
    destinationStation = request.session['destinationStation']
    destinationStationID = GTFS.getStationID(destinationStation)
    endpoint = request.session['endpoint']
    userTrainID = GTFS.getUserTrain(currentStationID, endpoint)
    while(not GTFS.nextStation(userTrainID,1).equals(destinationStationID)):
        pass
    return JsonResponse({"Status": "True"}) 
