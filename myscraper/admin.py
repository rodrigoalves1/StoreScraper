from django.contrib import admin
from .models import Product


def change_status(productadmin, request, queryset):
	for obj in queryset:
		if obj.status == 'e':
			obj.status = 'd'
		else:
			obj.status = 'e'
		obj.save()
	change_status.short_description = "invert product status"

class ProductAdmin(admin.ModelAdmin):
    list_display = ['url', 'status','store']
    ordering = ['store','url']
    actions = [change_status]



admin.site.register(Product,ProductAdmin)
