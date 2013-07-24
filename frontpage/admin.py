from django.contrib import admin

from frontpage.models import CarouselItem

class CarouselItemAdmin(admin.ModelAdmin):
    pass

admin.site.register(CarouselItem, CarouselItemAdmin)
