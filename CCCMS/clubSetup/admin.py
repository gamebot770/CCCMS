from django.contrib import admin
from .models import *


#Inlines
class CriteriaInline (admin.TabularInline):
	model = Criteria
	max_num = 3

class TermInline (admin.TabularInline):
	model = Term
	max_num = 3

#Admin Classes
class AcademicYearAdmin(admin.ModelAdmin):
	readonly_fields = ['yearID']
	inlines = [TermInline]
	
class ClubAdmin(admin.ModelAdmin):
	inlines = [ CriteriaInline, ]

# Register your models here.
admin.site.register(Club,ClubAdmin)
admin.site.register(Term)
admin.site.register(Student)
admin.site.register(AcademicYear,AcademicYearAdmin)
admin.site.register(Form)




	
