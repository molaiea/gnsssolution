from django.shortcuts import render
from django.http import JsonResponse
import georinex as gr
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm

# Imaginary function to handle an uploaded file.
#from somewhere import handle_uploaded_file
def handle_uploaded_file(f):
    with open('name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            print(request.FILES['file'])
            handle_uploaded_file(request.FILES['file'])
            nav = gr.load('name.txt')
            print(nav.sel(sv='G08')['SVclockBias'])

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
