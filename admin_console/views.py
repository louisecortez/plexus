from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
import json

from admin_console.forms import UploadFileForm, UserLoginForm
from admin_console.serializers import DataFileSerializer
from .models import DataFile, Barangay, Amenity, City, Region, Province, OD


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


class GetOD(APIView):
    def get(self, request, city):
        # cities = City.objects.filter(is_active=True).order_by('province__name', 'name')
        pairs = OD.objects.filter(origin__city_id=city).values('origin', 'destination').annotate(o=Count('origin'),
                                                                                                 d=Count('destination'))
        li = "o_id, o_lat, o_long, d_id, d_lat, d_long, cnt\n"
        # print(pairs)
        for p in pairs:
            # print(p)
            orig = Barangay.objects.get(id=p['origin'])
            dest = Barangay.objects.get(id=p['destination'])
            # li.append({
            #     "o_id": p['origin'],
            #     "o_lat": orig.latitude,
            #     "o_long": orig.longitude,
            #     "d_id": p['destination'],
            #     "d_lat": dest.latitude,
            #     "d_long": dest.longitude,
            #     "cnt": p['d']
            # })
            li += str(p['origin']) + ',' + str(orig.latitude) + ',' + str(orig.longitude) + ',' + str(
                p['destination']) + ',' + str(dest.latitude) + ',' + str(dest.longitude) + ',' + str(p['d']) + '\n'

        return HttpResponse(li, content_type='application/json', status=200)


class GetActiveCities(APIView):
    def get(self, request):
        cities = City.objects.filter(is_active=True).order_by('province__name', 'name')

        li = []
        for c in cities:
            li.append(c.json())

        return HttpResponse(json.dumps(li), content_type='application/json', status=200)


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
        d = {"type": "FeatureCollection", 'features': []}
        for brgy in brgys:
            d['features'].append(brgy.json())

        return HttpResponse(json.dumps(d), content_type='application/json', status=200)


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
            "fields": OD.config_fields()
        }
    }
    pairs = OD.objects.filter(origin__city_id=city).values('origin', 'destination').annotate(o=Count('origin'),
                                                                                             d=Count('destination'))
    li = []
    for p in pairs:
        orig = Barangay.objects.get(id=p['origin'])
        dest = Barangay.objects.get(id=p['destination'])
        li.append([p['origin'],
                   orig.latitude,
                   orig.longitude,
                   p['destination'],
                   dest.latitude,
                   dest.longitude,
                   p['d']])
    config['data']['allData'] = li
    return config


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
        datasets = [city.get_barangay_config(), city.get_amenity_config(), blank_config, getPairs(city)]
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
                        # {
                        #     "dataId": "pairs",
                        #     "id": "2ule5kakj",
                        #     "name": "cnt",
                        #     "type": "range",
                        #     "enlarged": False,
                        #     "plotType": "histogram",
                        #     "yAxis": None
                        # },
                        {
                            "dataId": "amenities",
                            "id": "0jv9s58qg",
                            "name": "class",
                            "type": "multiSelect",
                            # "value": city.amenity_types(),
                            "value": [],
                            "enlarged": False,
                            "plotType": "histogram",
                            "yAxis": None
                        },
                        {
                            "dataId": "pairs",
                            "id": "khyo98gm8",
                            "name": "o_id",
                            "type": "range",
                            "value": [
                                0,
                                0
                            ],
                            "enlarged": False,
                            "plotType": "histogram",
                            "yAxis": None
                        }
                    ],
                    "layers": [
                        {
                            "id": "slcy4jtg",
                            "type": "arc",
                            "config": {
                                "dataId": "pairs",
                                "label": "Pairs",
                                "color": [
                                    255,
                                    254,
                                    230
                                ],
                                "columns": {
                                    "lat0": "o_lat",
                                    "lng0": "o_long",
                                    "lat1": "d_lat",
                                    "lng1": "d_long"
                                },
                                "isVisible": False,
                                "visConfig": {
                                    "opacity": 1,
                                    "thickness": 5,
                                    "colorRange": {
                                        "name": "ColorBrewer Greys-6",
                                        "type": "sequential",
                                        "category": "ColorBrewer",
                                        "colors": [
                                            "#f7f7f7",
                                            "#d9d9d9",
                                            "#bdbdbd",
                                            "#969696",
                                            "#636363",
                                            "#252525"
                                        ],
                                        "reversed": False
                                    },
                                    "sizeRange": [
                                        0,
                                        10
                                    ],
                                    "targetColor": [
                                        38,
                                        26,
                                        16
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
                                # "colorField": {
                                #     "name": "cnt",
                                #     "type": "integer"
                                # },
                                "colorScale": "quantile",
                                # "sizeField": None,
                                "sizeField": {
                                    "name": " cnt",
                                    "type": "integer"
                                },
                                "sizeScale": "linear"
                            }
                        },
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
                                # "colorField": {
                                #     "name": "class",
                                #     "type": "string"
                                # },
                                "colorField": None,
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
                                    # "colorRange": {
                                    #     "name": "Purple Blue Yellow 6",
                                    #     "type": "sequential",
                                    #     "category": "Uber",
                                    #     "colors": [
                                    #         "#2B1E3E",
                                    #         "#343D5E",
                                    #         "#4F777E",
                                    #         "#709E87",
                                    #         "#99BE95",
                                    #         "#D6DEBF"
                                    #     ],
                                    #     "reversed": False
                                    # },
                                    "colorRange": {
                                        "name": "ColorBrewer YlOrRd-6",
                                        "type": "sequential",
                                        "category": "ColorBrewer",
                                        "colors": [
                                            "#bd0026",
                                            "#f03b20",
                                            "#fd8d3c",
                                            "#feb24c",
                                            "#fed976",
                                            "#ffffb2"
                                        ],
                                        "reversed": True
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
                                    128, 128, 128
                                ],
                                "columns": {
                                    "geojson": "_geojson"
                                },
                                "isVisible": True,
                                "visConfig": {
                                    "opacity": 0.05,
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
                                "outline": [],
                                "pairs": [
                                    "cnt"
                                ]
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
        return redirect('/cities/')


@login_required
def logout_view(request):
    logout(request)
    return redirect('/')


@login_required
def users(request):
    return render(request, 'admin_console/users.html')
