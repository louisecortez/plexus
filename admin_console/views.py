from django.http import HttpResponseRedirect
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
import json

from admin_console.forms import UploadFileForm
from admin_console.serializers import DataFileSerializer
from .models import DataFile, Barangay


def index(request):
    return render(request, 'admin_console/index.html')

def files(request):
    pass

def households(request):
    pass

def householdmembers(request):
    pass

def barangay(request):
    pass

# Create your views here.

class datafiles(APIView):
    def get(self, request):
        files = DataFile.objects.all()
        serializer = DataFileSerializer(files, many=True)
        return Response(serializer.data)

class brgy(APIView):
    def get(self, request):
        brgys = Barangay.objects.filter(city__name='Manila')
        d = {"type":"FeatureCollection", 'features' : []}
        for brgy in brgys:
            d['features'].append(brgy.json())

        return HttpResponse(json.dumps(d),content_type='application/json',status=200)

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return render(request, 'admin_console/home.html', {'form': form})
        else:
            print(form.errors)
            print('fail')
    else:
        form = UploadFileForm()
    return render(request, 'admin_console/home.html', {'form': form})

def handle_uploaded_file(f):

    print(f.read())
    households = str(f.read()).split('[\r\n]+')[1:]
    for h in households:
        print(h)

    with open('name.txt', 'wb+') as destination:
        destination.write(str(f.read()))


