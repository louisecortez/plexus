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


class Barangay(models.Model):
    name = models.CharField(default="", max_length=255)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    geojson = models.TextField(default="")
    population = models.IntegerField(default=0)
    income = models.FloatField(default=0.0)
    def json(self):
        j = ast.literal_eval(self.geojson)
        j['properties']['income'] = self.income
        j['properties']['population'] = self.population
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


class Indicator(models.Model):
    name = models.CharField(default="", max_length=255)
    description = models.CharField(default="", max_length=255)


class Coefficient(models.Model):
    indicator = models.ForeignKey(Indicator, on_delete=models.CASCADE)

    variable = models.CharField(default="", max_length=255)
    coefficient = models.FloatField(default=0.0)