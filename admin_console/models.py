import ast
import datetime
from statistics import mean

from django.contrib.auth.models import AbstractUser, User
from django.db import models


# Create your models here.
class Region(models.Model):
    name = models.CharField(default="", max_length=255)

    def __str__(self):
        return self.name

    def provinces(self):
        return Province.objects.filter(region__id=self.id).order_by('name')


class Province(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    name = models.CharField(default="", max_length=255)
    sid = models.CharField(default="", max_length=255)

    def __str__(self):
        return self.name

    def cities(self):
        return City.objects.filter(province__id=self.id).order_by('name')


class City(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    name = models.CharField(default="", max_length=255)
    is_active = models.BooleanField(default=False)
    sid = models.CharField(default="", max_length=255)

    def __str__(self):
        return self.name + ', ' + self.province.name

    def toggle_active(self):
        self.is_active = not self.is_active

    def json(self):
        return {
            'id': self.id,
            'name': self.name + ', ' + self.province.name
        }

    def get_barangay_config(self):
        config = {
            "version": "v1",
            "data": {
                "id": "barangays",
                "label": "Barangay",
                "color": [
                    143,
                    47,
                    191
                ],
                "allData": [],
                "fields": Barangay.config_fields()
            }
        }

        for barangay in self.barangay_set.all():
            values = barangay.values()
            # values[0]['properties']['index'] = ctr
            config['data']['allData'].append(values)

        return config

    def get_amenity_config(self):
        config = {
            "version": "v1",
            "data": {
                "id": "amenities",
                "label": "Amenity",
                "color": [
                    143,
                    47,
                    191
                ],
                "allData": [],
                "fields": Amenity.config_fields()
            }
        }

        for barangay in self.barangay_set.all():
            for amenity in barangay.amenity_set.all():
                config['data']['allData'].append(amenity.values())

        return config

    def amenity_types(self):
        return sorted(list(Amenity.objects.filter(barangay__city_id=self.id).values_list('classification',flat=True).distinct()))

    def amenity_colors(self):
        color_map = {
            'Academic Facilities': '#800000',
            'Accomodations': '#4363d8',
            'Financial Establishments': '#e6beff',
            'Food Establishments': '#fabebe',
            'Market and Convenience Stores': '#42d4f4',
            'Medical Facilities': '#ffe119',
            'Others': '#a9a9a9',
            'Recreational Facilities': '#f032e6',
            'Service Shops': '#ffffff',
            'Stores': '#808000'
        }
        return [color_map[a] for a in self.amenity_types()]


class Barangay(models.Model):
    name = models.CharField(default="", max_length=255)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    geojson = models.TextField(default="")
    population = models.IntegerField(default=0)
    income = models.FloatField(default=0.0)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    spatial = models.FloatField(default=0.0)
    temporal = models.FloatField(default=0.0)
    economic = models.FloatField(default=0.0)
    physical = models.FloatField(default=0.0)
    psychological = models.FloatField(default=0.0)
    physiological = models.FloatField(default=0.0)
    sustainability = models.FloatField(default=0.0)
    performance = models.FloatField(default=0.0)
    fairness = models.FloatField(default=0.0)
    sid = models.CharField(default="", max_length=255)

    def __str__(self):
        return self.name

    def get_td(self):
        return round(mean(
            [self.spatial, self.temporal, self.economic, self.physical, self.psychological, self.physiological,
             self.sustainability, self.performance, self.fairness]), 6)

    def json(self):
        j = {'type': 'Feature', 'geometry': ast.literal_eval(self.geojson), 'properties': {}}
        j['properties']['name'] = self.name
        j['properties']['income'] = self.income
        j['properties']['population'] = self.population
        j['properties']['latitude'] = self.latitude
        j['properties']['longitude'] = self.longitude
        j['properties']['desirability'] = round(mean(
            [self.spatial, self.temporal, self.economic, self.physical, self.psychological, self.physiological,
             self.sustainability, self.performance, self.fairness]), 6) * 100
        j['properties']['spatial'] = self.spatial * 100
        j['properties']['temporal'] = self.temporal * 100
        j['properties']['economic'] = self.economic * 100
        j['properties']['physical'] = self.physical * 100
        j['properties']['psychological'] = self.psychological * 100
        j['properties']['physiological'] = self.physiological * 100
        j['properties']['sustainability'] = self.sustainability * 100
        j['properties']['performance'] = self.performance * 100
        j['properties']['fairness'] = self.fairness * 100
        return j

    def row(self):
        col = [
            str({'type': 'Feature', 'geometry': ast.literal_eval(self.geojson)})
        ]
        pass

    @staticmethod
    def config_fields():
        return [
            {
                "name": "_geojson",
                "type": "geojson",
                "format": ""
            },
            {
                "name": "name",
                "type": "string",
                "format": ""
            },
            {
                "name": "income",
                "type": "real",
                "format": ""
            },
            {
                "name": "population",
                "type": "integer",
                "format": ""
            },
            {
                "name": "latitude",
                "type": "real",
                "format": ""
            },
            {
                "name": "longitude",
                "type": "real",
                "format": ""
            },
            {
                "name": "desirability",
                "type": "real",
                "format": ""
            },
            {
                "name": "spatial",
                "type": "real",
                "format": ""
            },
            {
                "name": "temporal",
                "type": "real",
                "format": ""
            },
            {
                "name": "economic",
                "type": "real",
                "format": ""
            },
            {
                "name": "physical",
                "type": "real",
                "format": ""
            },
            {
                "name": "psychological",
                "type": "real",
                "format": ""
            },
            {
                "name": "physiological",
                "type": "real",
                "format": ""
            },
            {
                "name": "sustainability",
                "type": "real",
                "format": ""
            },
            {
                "name": "performance",
                "type": "real",
                "format": ""
            },
            {
                "name": "fairness",
                "type": "real",
                "format": ""
            },
            {
                "name": "id",
                "type": "string",
                "format": ""
            }
        ]

    @staticmethod
    def basic_config_fields():
        return [
            {
                "name": "_geojson",
                "type": "geojson",
                "format": ""
            }
        ]

    def values(self):
        geo = {'type': 'Feature', 'geometry': ast.literal_eval(self.geojson), 'properties': {}}
        li = [geo, self.name, self.income, self.population, self.latitude, self.longitude,
              round(self.get_td() * 100, 4),
              round(self.spatial * 100, 4),
              round(self.temporal * 100, 4), round(self.economic * 100, 4), round(self.physical * 100, 4),
              round(self.psychological * 100, 4),
              round(self.physiological * 100, 4), round(self.sustainability * 100, 4),
              round(self.performance * 100, 4), round(self.fairness * 100, 4), str(self.id)]
        return li

class SurveyFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True)
    file = models.FileField(upload_to='upload/survey/', null=True, max_length=500)
    description = models.TextField(default="")
    date_collected = models.DateField(default=datetime.date.today)
    uploaded_by = models.DateTimeField(auto_now=True)
    is_processed = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)

class Household(models.Model):
    submission_id = models.CharField(default="", max_length=255)
    submission_time = models.CharField(default="", max_length=255, null=True)
    survey_file = models.ForeignKey(SurveyFile, on_delete=models.CASCADE)
    barangay = models.ForeignKey(Barangay, on_delete=models.CASCADE, null=True)
    address = models.CharField(default="", max_length=255, null=True)
    address_extra = models.TextField(default="", null=True)
    income = models.FloatField(default=0.0)
    education = models.CharField(default="", max_length=255)
    num_cars = models.IntegerField(default=0)
    years_residing = models.IntegerField(default=0)
    own_or_rent = models.CharField(default="", max_length=255)
    num_members = models.IntegerField(default=0)


class HouseholdMember(models.Model):
    household = models.ForeignKey(Household, on_delete=models.CASCADE)
    submission_id = models.CharField(default="", max_length=255)
    role = models.CharField(default="", max_length=255)
    age = models.IntegerField(default=0)
    occupation = models.CharField(default="", max_length=255)

class MainHouseholdMember(HouseholdMember):
    job = models.CharField(default="", max_length=255, null=True)
    income_range = models.CharField(default="", max_length=255)
    trip_purpose = models.CharField(default="", max_length=255)
    dest_barangay = models.ForeignKey(Barangay, on_delete=models.CASCADE, null=True)
    dest_address = models.CharField(default="", max_length=255, null=True)
    dest_address_extra = models.TextField(default="", null=True)

    trip_mode = models.CharField(default="", max_length=255)
    travel_time = models.IntegerField(default=0)

    # if car
    gas_or_diesel = models.CharField(default="", max_length=255, null=True)
    fuel_cost = models.FloatField(default=0.0)# weekly

    # if public
    fare = models.FloatField(default=0.0) # one way

    is_flood_prone = models.BooleanField(default=False)
    will_cancel = models.BooleanField(default=False)

    new_time = models.FloatField(default=0.0, null=True)
    new_cost = models.FloatField(default=0.0, null=True)

    @staticmethod
    def config_fields():
        return [
            {
                "name": "o_id",
                "type": "string",
                "format": ""
            },
            {
                "name": "o_lat",
                "type": "real",
                "format": ""
            },
            {
                "name": "o_long",
                "type": "real",
                "format": ""
            },
            {
                "name": "d_id",
                "type": "string",
                "format": ""
            },
            {
                "name": "d_lat",
                "type": "real",
                "format": ""
            },
            {
                "name": "d_long",
                "type": "real",
                "format": ""
            },
            {
                "name": "cnt",
                "type": "integer",
                "format": ""
            }
        ]


class Amenity(models.Model):
    barangay = models.ForeignKey(Barangay, on_delete=models.CASCADE)
    name = models.CharField(default="", max_length=255)
    type = models.CharField(default="", max_length=255)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    sid = models.CharField(default="", max_length=255)
    classification = models.CharField(default="", max_length=255)

    def __str__(self):
        return self.name

    def json(self):
        j = {
            'type': 'Feature',
            'geometry': {
                "type": "Point",
                "coordinates": [self.longitude, self.latitude]
            },
            'properties': {
                'name': self.name,
                'barangay': self.barangay.name,
                'type': self.type,
                'icon': 'place'
            }
        }

        return j

    def row(self):
        return ','.join(['"' + self.name + '"', str(self.latitude), str(self.longitude), '"' + self.barangay.name + '"',
                         '"' + self.type + '"', 'place'])

    def values(self):
        map = {
            "Academic Facilities": "employees",
            "Accomodations": "home",
            "Financial Establishments": "payment",
            "Food Establishments": "events",
            "Market and Convenience Stores": "cart",
            "Medical Facilities": "control-on",
            "Others": "pin",
            "Recreational Facilities": "car",
            "Service Shops": "support",
            "Stores": "promo-alt"
        }
        li = [self.name, self.latitude, self.longitude, self.barangay.name, self.type, self.classification,
              map[self.classification]]
        return li

    @staticmethod
    def config_fields():
        return [
            {
                "name": "name",
                "type": "string",
                "format": ""
            },
            {
                "name": "latitude",
                "type": "real",
                "format": ""
            },
            {
                "name": "longitude",
                "type": "real",
                "format": ""
            },
            {
                "name": "barangay",
                "type": "string",
                "format": ""
            },
            {
                "name": "type",
                "type": "string",
                "format": ""
            },
            {
                "name": "class",
                "type": "string",
                "format": ""
            },
            {
                "name": "icon",
                "type": "string",
                "format": ""
            }
        ]


class Indicator(models.Model):
    name = models.CharField(default="", max_length=255)
    description = models.CharField(default="", max_length=255)


class Coefficient(models.Model):
    indicator = models.ForeignKey(Indicator, on_delete=models.CASCADE)

    variable = models.CharField(default="", max_length=255)
    coefficient = models.FloatField(default=0.0)

# class User(AbstractUser):
#     username = models.