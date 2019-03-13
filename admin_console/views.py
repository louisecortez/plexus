from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
import json

from admin_console.forms import UploadFileForm, UserLoginForm
from admin_console.serializers import DataFileSerializer
from .models import DataFile, Barangay, Amenity, City


@login_required
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

class BarangayGeojson(APIView):
    def get(self, request, city):
        brgys = Barangay.objects.filter(city__name__iexact=city.replace('_', ' '))
        d = {"type":"FeatureCollection", 'features' : []}
        for brgy in brgys:
            d['features'].append(brgy.json())

        return HttpResponse(json.dumps(d),content_type='application/json',status=200)

class AmenityGeojson(APIView):
    def get(self, request, city):
        amenities = Amenity.objects.filter(barangay__city__name__iexact=city.replace('_', ' '))
        # d = {"type": "FeatureCollection", 'features': []}
        s = ','.join(['name', 'latitude', 'longitude', 'barangay', 'type', 'icon']) + '\n'
        for amenity in amenities:
            s += amenity.row() + '\n'
            # d['features'].append(amenity.json())

        return HttpResponse(s, content_type='application/json', status=200)

class UploadDataFile(View):
    def get(self, request):
        form = UploadFileForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            file = form.cleaned_data.get('file')
            print(file)
            handle_uploaded_file(request.FILES['file'])
            return redirect('/')

        context = {
            'form': form,
        }
        return render(request, 'admin_console/home.html', context)

    def post(self, request):
        pass

@login_required
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

@login_required
def upload(request):
    form = UploadFileForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        file = form.cleaned_data.get('file')
        print(file)
        handle_uploaded_file(request.FILES['file'])
        return redirect('/')

    context = {
        'form': form,
    }
    return render(request, 'admin_console/home.html', context)


# class UserLogin(View):
#     template_name = 'admin_console/login.html'
#
#     def get(self, request):
#         user = UserLoginForm()
#         return render(request, self.template_name, {'form': user})
#
#     def post(self, request):
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         form = UploadFileForm()
#         if user is not None:
#             login(request, user)
#             return render(request, 'admin_console/index.html', {'form': form})
#         else:
#             # Return an 'invalid login' error message.
#             return render(request, self.template_name, {'form': user})

def login_view(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('/')

    context = {
        'form': form,
    }
    return render(request, 'admin_console/login.html', context)

@login_required
def get_cities(request):
    cities = City.objects.all()
    context = {
        'cities': cities,
    }
    return render(request, 'admin_console/cities.html', context)
    pass

