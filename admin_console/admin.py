from django.contrib import admin

# Register your models here.
from admin_console.models import SurveyFile, City, Barangay, Household, HouseholdMember

admin.site.register(SurveyFile)
admin.site.register(City)
admin.site.register(Barangay)
admin.site.register(Household)
admin.site.register(HouseholdMember)
