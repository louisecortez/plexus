import ast
from statistics import mean

from django.db import models


# Create your models here.
class DataFile(models.Model):
    name = models.CharField(default="", max_length=255)
    description = models.TextField(default="")


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
        return self.name

    def toggle_active(self):
        self.is_active = not self.is_active

    def json(self):
        return {
            'id': self.id,
            'name': self.province.name + " - " + self.name
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
        ctr = 0
        for barangay in self.barangay_set.all():
            values = barangay.values()
            values[0]['properties']['index'] = ctr
            config['data']['allData'].append(values)
            ctr+=1

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
             self.sustainability, self.performance, self.fairness]), 6)
        j['properties']['spatial'] = self.spatial
        j['properties']['temporal'] = self.temporal
        j['properties']['economic'] = self.economic
        j['properties']['physical'] = self.physical
        j['properties']['psychological'] = self.psychological
        j['properties']['physiological'] = self.physiological
        j['properties']['sustainability'] = self.sustainability
        j['properties']['performance'] = self.performance
        j['properties']['fairness'] = self.fairness
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
            }
        ]

    def values(self):
        geo = {'type': 'Feature', 'geometry': ast.literal_eval(self.geojson), 'properties': {}}
        li = [geo, self.name, self.income, self.population, self.latitude, self.longitude, self.get_td(), self.spatial,
              self.temporal, self.economic, self.physical, self.psychological, self.physiological, self.sustainability,
              self.performance, self.fairness]
        return li


class Household(models.Model):
    datafile = models.ForeignKey(DataFile, on_delete=models.CASCADE)
    barangay = models.ForeignKey(Barangay, on_delete=models.CASCADE)
    address = models.CharField(default="", max_length=255)
    income = models.IntegerField(default=0)
    education = models.CharField(default="", max_length=255)
    numCars = models.IntegerField(default=0)
    yearsResiding = models.IntegerField(default=0)
    ownOrRent = models.CharField(default="", max_length=255)
    numMembers = models.IntegerField(default=0)


class HouseholdMember(models.Model):
    household = models.ForeignKey(Household, on_delete=models.CASCADE)
    role = models.CharField(default="", max_length=255)
    age = models.IntegerField(default=0)
    occupation = models.CharField(default="", max_length=255)
    tripPurpose = models.CharField(default="", max_length=255)
    destAddress = models.CharField(default="", max_length=255)
    destBarangay = models.ForeignKey(Barangay, on_delete=models.CASCADE)
    tripMode = models.CharField(default="", max_length=255)
    travelTime = models.IntegerField(default=0)
    job = models.CharField(default="", max_length=255)
    income = models.IntegerField(default=0)
    gasOrDiesel = models.CharField(default="", max_length=255)
    fuelCost = models.IntegerField(default=0)
    isFloodProne = models.BooleanField(default=False)
    addTime = models.IntegerField(default=0)
    addCost = models.IntegerField(default=0)


class Amenity(models.Model):
    barangay = models.ForeignKey(Barangay, on_delete=models.CASCADE)
    name = models.CharField(default="", max_length=255)
    type = models.CharField(default="", max_length=255)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    sid = models.CharField(default="", max_length=255)

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
        li = [self.name, self.latitude, self.longitude, self.barangay.name, self.type, 'place']
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
