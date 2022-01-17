from django.shortcuts import render
from django.http import JsonResponse

def home_view(request):
    
    return render(request, "home.html")


def sendData(req):
    # print(req.POST.get('data'))
    
    result = req.POST
    print("testing")
    print(result)
    
    return JsonResponse({"instance": 123}, status=200)
# Create your views here.
