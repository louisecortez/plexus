import re

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count, Max
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
import json

from admin_console import kepler_config
from admin_console.forms import UploadFileForm, UserLoginForm
from admin_console.serializers import DataFileSerializer
from .models import SurveyFile, Barangay, Amenity, City, Region, Province, Household, HouseholdMember, \
    MainHouseholdMember

import xlrd


@login_required
def index(request):
    cities = City.objects.all()
    survey_file = SurveyFile.objects.all().order_by('-uploaded_by')
    context = {
        'cities': cities,
        'survey_file': survey_file
    }
    return render(request, 'admin_console/index.html', context)
    pass


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

        return HttpResponse(json.dumps(li), content_type='application/json', status=200)


def getPairs(city):
    config = {
        "version": "v1",
        "data": {
            "id": "pairs",
            "label": "Pairs",
            "color": [
                143,
                47,
                191
            ],
            "allData": [],
            "fields": MainHouseholdMember.config_fields()
        }
    }

    pairs = MainHouseholdMember.objects.filter(household__survey_file__city_id=city, dest_barangay__isnull=False,
                                               household__barangay__isnull=False).values('household__barangay',
                                                                                         'dest_barangay', 'travel_distance').annotate(
        o=Count('household__barangay'), d=Count('dest_barangay'), dist=Max('travel_distance'))
    # pairs = OD.objects.filter(origin__city_id=city).values('origin', 'destination').annotate(o=Count('origin'),
    #                                                                                          d=Count('destination'))

    li = []
    for p in pairs:
        orig = Barangay.objects.get(id=p['household__barangay'])
        dest = Barangay.objects.get(id=p['dest_barangay'])
        li.append([str(p['household__barangay']),
                   orig.latitude,
                   orig.longitude,
                   str(p['dest_barangay']),
                   dest.latitude,
                   dest.longitude,
                   p['d'],
                   round(p['dist'],4)])
    config['data']['allData'] = li
    return config


class datafiles(APIView):
    def get(self, request):
        files = SurveyFile.objects.all()
        serializer = DataFileSerializer(files, many=True)
        return Response(serializer.data)


class BarangayGeojson(APIView):
    def get(self, request, city):
        if isinstance(city, int):
            brgys = Barangay.objects.filter(city__id=city)
        else:
            brgys = Barangay.objects.filter(city__name__iexact=city.replace('_', ' '))
        d = {"type": "FeatureCollection", 'features': []}
        for brgy in brgys:
            d['features'].append(brgy.json())

        return HttpResponse(json.dumps(d), content_type='application/json', status=200)


class ConfigJson(APIView):
    def get(self, request, city):
        city = City.objects.get(id=city)
        # print(city.amenity_types())
        blank_config = {
            "version": "v1",
            "data": {
                "id": "outline",
                "label": "Barangay Outline",
                "color": [
                    143,
                    47,
                    191
                ],
                "allData": [],
                "fields": Barangay.basic_config_fields()
            }
        }
        datasets = [city.get_barangay_config(), city.get_amenity_config(), blank_config, getPairs(city)]
        info = {"app": "kepler.gl"}
        config = kepler_config.json(city)

        j = {
            "datasets": datasets,
            "config": config,
            "info": info
        }

        return HttpResponse(json.dumps(j), content_type='application/json', status=200)


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
        # if form.is_valid():
        # handle_uploaded_file(request.FILES['file'])
        form.save()
        # return render(request, 'admin_console/home.html', {'form': form})
        return redirect('/upload')
        # else:
        #     print(form.errors)
        #     print('fail')
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

    if request.method == 'POST':
        if form.is_valid():
            survey_file = form.save(commit=False)
            survey_file.user = request.user
            survey_file.save()
            # print('start')
            # wb = openpyxl.load_workbook(survey_file.file)
            # print(wb.sheetnames)
            # sheet1 = wb[wb.sheetnames[0]]
            # print(sheet1['A1'].value)
            # pandas.read_excel(survey_file.file)
            return redirect('/survey/mapping/' + str(survey_file.id))
        else:
            print(form.errors.as_data())
    cities = City.objects.all().order_by('province__region_id', 'province_id', 'name')
    regions = Region.objects.all()
    context = {
        'form': form,
        "cities": cities,
        'regions': regions
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

    def post(self, request, id):
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


# @login_required
# def survey(request, id):
#     city = City.objects.get(id=id)
#
#     context = {
#         'city': city
#     }
#     return render(request, 'admin_console/survey.html', context)
#     pass

def process_workbook(wb, survey_id, city_id):
    # Household
    sheet1 = wb.sheet_by_index(0)

    for i in range(1, sheet1.nrows):
        row = sheet1.row_values(i)
        if row[3].strip() != "":
            household = Household(
                survey_file_id=survey_id,
                address=row[2],
                barangay=Barangay.objects.filter(name=row[3], city_id=city_id).first(),
                address_extra=row[4],
                income=float(row[5]),
                education=row[6],
                num_cars=int((re.findall('\d+', row[7]) + ['0'])[0]),
                years_residing=int((re.findall('\d+', row[8]) + ['0'])[0]),
                own_or_rent=row[9],
                num_members=int(row[10]),
                submission_id=row[17],
                submission_time=row[19]
            )
            household.save()
    print("DONE HOUSEHOLD")
    # Household Member
    sheet2 = wb.sheet_by_index(1)

    for i in range(1, sheet2.nrows):
        row = sheet2.row_values(i)
        if int(row[1]) > 6:
            member = MainHouseholdMember(
                household=Household.objects.filter(survey_file_id=survey_id, submission_id=row[250]).first(),
                role=row[0],
                age=int(row[1]),
                occupation=row[2],
                job=row[3],
                income_range=row[4] or row[5],
                trip_purpose=row[6],
                dest_address=row[8],
                dest_barangay=Barangay.objects.filter(name=row[9], city_id=city_id).first(),
                dest_address_extra=row[10],
                trip_mode=row[17] or row[11],
                gas_or_diesel=row[12],
                fuel_cost=float(row[13]) if row[13] else 0,
                fare=float(row[18]) if row[18] else None or float(row[23]) if row[23] else 0,
                travel_time=float(row[27]),
                is_flood_prone=True if row[31] == 'Yes' else False,
                will_cancel=True if row[32] == 'Yes' else False,
                new_cost=float(row[34]) if row[34] else None,
                new_time=float(row[36]) if row[36] else None,
                submission_id=row[250]
            )
            # print(str(i)+", ", end="")
            member.save()
    print("DONE HOUSEHOLD MEMBER")
    # extra
    sheet3 = wb.sheet_by_index(2)

    for i in range(1, sheet3.nrows):
        row = sheet3.row_values(i)
        if int(row[1]) > 6:
            member = HouseholdMember(
                household=Household.objects.filter(survey_file_id=survey_id, submission_id=row[6]).first(),
                role=row[0],
                age=int(row[1]),
                occupation=row[2],
                submission_id=row[6]
            )
            member.save()
    print("DONE HOUSEHOLD MEMBER EXTRA")
    return True


class SurveyMappingView(View):
    def get(self, request, id):
        survey = SurveyFile.objects.get(id=id)
        if not survey.is_processed:
            print("start")
            file = xlrd.open_workbook(survey.file.name)
            print("load")
            if process_workbook(file, id, survey.city_id):
                survey.is_processed = True
                survey.save()
            print("end")
            return redirect('/upload')
            sheets = []
            for sheet_name in file.sheet_names():
                sheet = file.sheet_by_name(sheet_name)
                sheets.append({
                    'name': sheet_name,
                    'cols': sheet.row_values(0)
                })

            context = {
                'filetype': 'xlsx',
                'sheets': sheets
            }
            return render(request, 'admin_console/mapping.html', context)
        else:
            redirect('/')
        city = City.objects.get(id=id)

        context = {
            'city': city
        }

        pass

    def post(self, request, id):
        # city = City.objects.get(id=id)
        # selected = request.POST['cities']
        # if selected == 'publish' and not city.is_active:
        #     city.is_active = True
        #     city.save()
        #     print(city.name, " is now active")
        # elif selected == 'unpublish' and city.is_active:
        #     city.is_active = False
        #     city.save()
        #     print(city.name, " is now inactive")
        return redirect('/')


class SurveyDataView(View):
    def get(self, request, id):
        city = City.objects.get(id=id)

        context = {
            'city': city
        }
        return render(request, 'admin_console/survey.html', context)
        pass

    def post(self, request, id):
        city = City.objects.get(id=id)
        selected = request.POST['cities']
        if selected == 'publish' and not city.is_active:
            city.is_active = True
            city.save()
            print(city.name, " is now active")
        elif selected == 'unpublish' and city.is_active:
            city.is_active = False
            city.save()
            print(city.name, " is now inactive")
        return redirect('/')
