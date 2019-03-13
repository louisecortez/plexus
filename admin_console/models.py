import ast

from django.db import models


# Create your models here.
class DataFile(models.Model):
    name = models.CharField(default="", max_length=255)
    description = models.TextField(default="")


class City(models.Model):
    name = models.CharField(default="", max_length=255)
    region = models.CharField(default="", max_length=255)
    province = models.CharField(default="", max_length=255)
    geojson = models.TextField(default="")
    is_active = models.BooleanField(default=False)


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

    def json(self):
        j = {'type': 'Feature', 'geometry': ast.literal_eval(self.geojson), 'properties': {}}
        j['properties']['income'] = self.income
        j['properties']['population'] = self.population
        j['properties']['latitude'] = self.latitude
        j['properties']['longitude'] = self.longitude
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
    osm_id = models.CharField(default="", max_length=255)

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
        return ','.join([self.name, str(self.latitude), str(self.longitude), self.barangay.name, self.type, 'place'])


class Indicator(models.Model):
    name = models.CharField(default="", max_length=255)
    description = models.CharField(default="", max_length=255)


class Coefficient(models.Model):
    indicator = models.ForeignKey(Indicator, on_delete=models.CASCADE)

    variable = models.CharField(default="", max_length=255)
    coefficient = models.FloatField(default=0.0)
