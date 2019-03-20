from django.contrib.auth import authenticate, login, logout
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
from .models import DataFile, Barangay, Amenity, City, Region, Province


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

class GetActiveCities(APIView):
    def get(self, request):
        cities = City.objects.filter(is_active=True).order_by('province__name', 'name')

        li = []
        for c in cities:
            li.append(c.json())

        return HttpResponse(json.dumps(li),content_type='application/json',status=200)

class datafiles(APIView):
    def get(self, request):
        files = DataFile.objects.all()
        serializer = DataFileSerializer(files, many=True)
        return Response(serializer.data)

class BarangayGeojson(APIView):
    def get(self, request, city):
        if isinstance(city, int):
            brgys = Barangay.objects.filter(city__id=city)
        else:
            brgys = Barangay.objects.filter(city__name__iexact=city.replace('_', ' '))
        d = {"type":"FeatureCollection", 'features' : []}
        for brgy in brgys:
            d['features'].append(brgy.json())

        return HttpResponse(json.dumps(d),content_type='application/json',status=200)

class AmenityGeojson(APIView):
    def get(self, request, city):
        if isinstance(city, int):
            amenities = Amenity.objects.filter(barangay__city__id=city)
        else:
            amenities = Amenity.objects.filter(barangay__city__name__iexact=city.replace('_', ' '))
        # d = {"type": "FeatureCollection", 'features': []}
        s = ','.join(['name', 'latitude', 'longitude', 'barangay', 'type', 'icon']) + '\n'
        for amenity in amenities:
            s += amenity.row() + '\n'
            # d['features'].append(amenity.json())

        return HttpResponse(s, content_type='application/json', status=200)

@login_required
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

@login_required
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
def get_provinces(request):
    regions = Region.objects.all()
    context = {
        'regions': regions,
    }
    return render(request, 'admin_console/province.html', context)
    pass

@login_required
def get_cities(request, id):
    province = Province.objects.get(id=id)
    # cities = City.objects.filter(province__id=id)

    context = {
        'province': province
    }
    return render(request, 'admin_console/cities.html', context)
    pass

class CityList(View):
    def get(self, request, id):
        province = Province.objects.get(id=id)
        # cities = City.objects.filter(province__id=id)

        context = {
            'province': province
        }
        return render(request, 'admin_console/cities.html', context)

    def post(self, request,id):
        cities = [int(id) for id in request.POST.getlist('cities')]
        province = Province.objects.get(id=id)
        for city in province.cities():
            if city.id in cities and not city.is_active:
                city.is_active = True
                city.save()
            elif city.id not in cities and city.is_active:
                city.is_active = False
                city.save()
        return redirect('/')

@login_required
def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def users(request):
    return render(request, 'admin_console/users.html')