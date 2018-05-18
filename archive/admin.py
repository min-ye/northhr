from django.contrib import admin
from archive.models import Heading, Category, Archive, Person

class CategoryInline(admin.StackedInline):
   model = Category

class HeadingAdmin(admin.ModelAdmin):
   list_display = ('name', 'code', 'chinese_code', 'sequence')
   inlines = [ CategoryInline ]

class CategoryAdmin(admin.ModelAdmin):
   list_display = ('name', 'code', 'sequence')

class ArchiveAdmin(admin.ModelAdmin):
   list_display = ('name', 'sequence', 'comment', 'description')

admin.site.register(Heading, HeadingAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Archive, ArchiveAdmin)
admin.site.register(Person)
admin.site.site_header = "管理平台"
#admin.site.index_template = 'admin/index.html'
#admin.autodiscover()