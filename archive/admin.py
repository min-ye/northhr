from django.contrib import admin
from archive.models import Category, Person
 
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'code')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Person)
admin.site.site_header = "管理平台"
#admin.site.index_template = 'admin/index.html'
#admin.autodiscover()