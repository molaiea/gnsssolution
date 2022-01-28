from django.shortcuts import render
from django.http import JsonResponse
import georinex as gr
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
import numpy as np
from .algorithms import satellite_position, app_coords, jacobienne, minimos_cuadrados, extract_params
# Imaginary function to handle an uploaded file.
#from somewhere import handle_uploaded_file
def handle_uploaded_file(f):
    name = str(f)
    cachepath = "D:\gnsssolution\mygnsssolution\mysolution\cache"
    path = f"{cachepath}\{name}"
    with open(path , 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    nav = gr.load(path)
    epoch1 = nav.coords['time'].values[0]
    epoch2 = nav.coords['time'].values[1]
    satellites = nav.coords['sv'].values
    values_epoch1 = np.zeros((len(satellites),17))
    satellites_in_range_epoch1 = []
    satellites_in_range_epoch2 = []
    values_epoch2 = np.zeros((len(satellites),17))
    for i in range(len(satellites)):
        values_epoch1[i] = np.array((extract_params(path, satellites[i], 0)))
        values_epoch2[i] = np.array((extract_params(path, satellites[i], 1)))
        if len(values_epoch1[i][~np.isnan(values_epoch1[i])]) > 1:
            satellites_in_range_epoch1.append(satellites[i])
        if len(values_epoch2[i][~np.isnan(values_epoch2[i])]) > 1:
            satellites_in_range_epoch2.append(satellites[i])
    print(satellites_in_range_epoch1)
    coords_epoch1 = {}
    coords_epoch2 = {}
    for i in range(len(satellites_in_range_epoch1)):
        coords_epoch1[satellites_in_range_epoch1[i]] = satellite_position(path,satellites_in_range_epoch1[i],0) 
    for i in range(len(satellites_in_range_epoch2)):
        coords_epoch2[satellites_in_range_epoch2[i]] = satellite_position(path,satellites_in_range_epoch2[i],1) 
    
    print(coords_epoch1["G08"])
    print(coords_epoch2["G08"])



def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            print(str(request.FILES['file']))
            handle_uploaded_file(request.FILES['file'])
            # nav = gr.load('name.txt')
            # print(nav.sel(sv='G08')['SVclockBias'])

            return HttpResponseRedirect('/upload')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})


def home_view(request):
    
    return render(request, "home.html")


def sendData(req):
    # print(req.POST.get('data'))
    
    result = req.POST
    print("testing")
    print(result.get('data'))
    
    return JsonResponse({"instance": 123}, status=200)
# Create your views here.
