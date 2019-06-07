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
from .models import SurveyFile, Barangay, Amenity, City, Region, Province

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
        print(city.amenity_types())
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
        datasets = [city.get_barangay_config(), city.get_amenity_config(), blank_config]
        info = {"app": "kepler.gl"}
        config = {
            "version": "v1",
            "config": {
                "visState": {
                    "filters": [
                        {
                            "dataId": "barangays",
                            "id": "8whi6i9v",
                            "name": "desirability",
                            "type": "range",
                            "value": [
                                0,
                                100
                            ],
                            "enlarged": False,
                            "plotType": "histogram",
                            "yAxis": None
                        },
                        {
                            "dataId": "amenities",
                            "id": "0jv9s58qg",
                            "name": "class",
                            "type": "multiSelect",
                            "value": city.amenity_types(),
                            "enlarged": False,
                            "plotType": "histogram",
                            "yAxis": None
                        }
                    ],
                    "layers": [
                        {
                            "id": "jusnudd",
                            "type": "icon",
                            "config": {
                                "dataId": "amenities",
                                "label": "Amenity",
                                "color": [
                                    255,
                                    254,
                                    230
                                ],
                                "columns": {
                                    "lat": "latitude",
                                    "lng": "longitude",
                                    "icon": "icon"
                                },
                                "isVisible": True,
                                "visConfig": {
                                    "radius": 35,
                                    "fixedRadius": False,
                                    "opacity": 1.0,
                                    "colorRange": {
                                        "name": "Uber Viz Qualitative 4",
                                        "type": "qualitative",
                                        "category": "Uber",
                                        "colors": city.amenity_colors(),
                                        "reversed": False
                                    },
                                    "radiusRange": [
                                        0,
                                        50
                                    ],
                                    "hi-precision": False
                                },
                                "textLabel": {
                                    "field": None,
                                    "color": [
                                        255,
                                        255,
                                        255
                                    ],
                                    "size": 50,
                                    "offset": [
                                        0,
                                        0
                                    ],
                                    "anchor": "middle"
                                }
                            },
                            "visualChannels": {
                                "colorField": {
                                    "name": "class",
                                    "type": "string"
                                },
                                # "colorField": None,
                                "colorScale": "ordinal",
                                "sizeField": None,
                                "sizeScale": "linear"
                            }
                        },
                        {
                            "id": "xrf8f2s",
                            "type": "point",
                            "config": {
                                "dataId": "barangays",
                                "label": "Center",
                                "color": [
                                    23,
                                    184,
                                    190
                                ],
                                "columns": {
                                    "lat": "latitude",
                                    "lng": "longitude",
                                    "altitude": None
                                },
                                "isVisible": False,
                                "visConfig": {
                                    "radius": 10,
                                    "fixedRadius": False,
                                    "opacity": 0.8,
                                    "outline": False,
                                    "thickness": 2,
                                    "colorRange": {
                                        "name": "Global Warming",
                                        "type": "sequential",
                                        "category": "Uber",
                                        "colors": [
                                            "#5A1846",
                                            "#900C3F",
                                            "#C70039",
                                            "#E3611C",
                                            "#F1920E",
                                            "#FFC300"
                                        ]
                                    },
                                    "radiusRange": [
                                        0,
                                        50
                                    ],
                                    "hi-precision": False
                                },
                                "textLabel": {
                                    "field": None,
                                    "color": [
                                        255,
                                        255,
                                        255
                                    ],
                                    "size": 50,
                                    "offset": [
                                        0,
                                        0
                                    ],
                                    "anchor": "middle"
                                }
                            },
                            "visualChannels": {
                                "colorField": None,
                                "colorScale": "quantile",
                                "sizeField": None,
                                "sizeScale": "linear"
                            }
                        },
                        {
                            "id": "izm95sg",
                            "type": "geojson",
                            "config": {
                                "dataId": "barangays",
                                "label": "Barangay",
                                "color": [
                                    246,
                                    209,
                                    138,
                                    255
                                ],
                                "columns": {
                                    "geojson": "_geojson"
                                },
                                "isVisible": True,
                                "visConfig": {
                                    "opacity": 0.8,
                                    "thickness": 0.5,
                                    "colorRange": {
                                        "name": "Purple Blue Yellow 6",
                                        "type": "sequential",
                                        "category": "Uber",
                                        "colors": [
                                            "#2B1E3E",
                                            "#343D5E",
                                            "#4F777E",
                                            "#709E87",
                                            "#99BE95",
                                            "#D6DEBF"
                                        ],
                                        "reversed": False
                                    },
                                    "radius": 10,
                                    "sizeRange": [
                                        0,
                                        10
                                    ],
                                    "radiusRange": [
                                        0,
                                        50
                                    ],
                                    "heightRange": [
                                        0,
                                        500
                                    ],
                                    "elevationScale": 5,
                                    "hi-precision": False,
                                    "stroked": True,
                                    "filled": True,
                                    "enable3d": False,
                                    "wireframe": False
                                },
                                "textLabel": {
                                    "field": None,
                                    "color": [
                                        255,
                                        255,
                                        255
                                    ],
                                    "size": 50,
                                    "offset": [
                                        0,
                                        0
                                    ],
                                    "anchor": "middle"
                                }
                            },
                            "visualChannels": {
                                "colorField": {
                                    "name": "desirability",
                                    "type": "real"
                                },
                                "colorScale": "quantile",
                                "sizeField": None,
                                "sizeScale": "linear",
                                "heightField": None,
                                "heightScale": "linear",
                                "radiusField": None,
                                "radiusScale": "linear"
                            }
                        },
                        {
                            "id": "lldqtu",
                            "type": "geojson",
                            "config": {
                                "dataId": "outline",
                                "label": "Barangay outline",
                                "color": [
                                    255,
                                    254,
                                    230
                                ],
                                "columns": {
                                    "geojson": "_geojson"
                                },
                                "isVisible": True,
                                "visConfig": {
                                    "opacity": 0.8,
                                    "thickness": 0.5,
                                    "colorRange": {
                                        "name": "Global Warming",
                                        "type": "sequential",
                                        "category": "Uber",
                                        "colors": [
                                            "#5A1846",
                                            "#900C3F",
                                            "#C70039",
                                            "#E3611C",
                                            "#F1920E",
                                            "#FFC300"
                                        ]
                                    },
                                    "radius": 10,
                                    "sizeRange": [
                                        0,
                                        10
                                    ],
                                    "radiusRange": [
                                        0,
                                        50
                                    ],
                                    "heightRange": [
                                        0,
                                        500
                                    ],
                                    "elevationScale": 5,
                                    "hi-precision": False,
                                    "stroked": True,
                                    "filled": False,
                                    "enable3d": False,
                                    "wireframe": False
                                },
                                "textLabel": {
                                    "field": None,
                                    "color": [
                                        255,
                                        255,
                                        255
                                    ],
                                    "size": 50,
                                    "offset": [
                                        0,
                                        0
                                    ],
                                    "anchor": "middle"
                                }
                            },
                            "visualChannels": {
                                "colorField": None,
                                "colorScale": "quantile",
                                "sizeField": None,
                                "sizeScale": "linear",
                                "heightField": None,
                                "heightScale": "linear",
                                "radiusField": None,
                                "radiusScale": "linear"
                            }
                        }
                    ],
                    "interactionConfig": {
                        "tooltip": {
                            "fieldsToShow": {
                                "barangays": [
                                    "name",
                                    "desirability"
                                ],
                                "amenities": [
                                    "name",
                                    "barangay",
                                    "class",
                                    "type"
                                ],
                                "outline": []
                            },
                            "enabled": True
                        },
                        "brush": {
                            "size": 0.5,
                            "enabled": False
                        }
                    },
                    "layerBlending": "normal",
                    "splitMaps": []
                }
            }
        }

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
            pandas.read_excel(survey_file.file)
            return redirect('/upload')
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

class SurveyMappingView(View):
    def get(self, request, id):
        survey = SurveyFile.objects.get(id=id)
        if not survey.is_processed:
            print("--")
            print(survey.file)
            file = xlrd.open_workbook(survey.file.name)
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
            pass
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
