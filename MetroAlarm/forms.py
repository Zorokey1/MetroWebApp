from django import forms 
from TransitData.GTFS import GTFS

class stationForm(forms.Form):
    
    stationChoices = [(k, v) for k, v in GTFS.stationDict.items()]
    endpointChoices = [(v, k) for k, v in GTFS.directionDict.items()]
    currentStation = forms.ChoiceField(choices=stationChoices)
    destinationStation = forms.ChoiceField(choices=stationChoices)
    endpoint = forms.ChoiceField(choices=endpointChoices)
    