from django.shortcuts import render, redirect
from TransitData.GTFS import GTFS
from TransitData.GTFS_Async import GTFS as AGTFS
from .forms import stationForm
import time
from django.core.signals import request_finished

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
    
'''
async def async_helper():
    async with httpx.AsyncClient() as client:
        headers = {'api_key': '1b32768b1e994630bcffe0177cbe4350'}
        feed = gtfs_realtime_pb2.FeedMessage()
        response = await client.get('https://api.wmata.com/gtfs/rail-gtfsrt-vehiclepositions.pb', headers=headers)
        feed.ParseFromString(response.content)
        await asyncio.sleep(10)
        print(feed)
        print('---------------------------------------')
'''