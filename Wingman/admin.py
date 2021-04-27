from django.contrib import admin
from .models import *
from .models import Category, User, Auction, Bid, Comment, WatchList,Sport_Cat,SportField,Appointment,Del_Corp,Delivery
# Register your models here.
admin.site.register(Category)
admin.site.register(User)
admin.site.register(Auction)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(WatchList)
admin.site.register(Sport_Cat)
admin.site.register(SportField)
admin.site.register(Appointment)
admin.site.register(Del_Corp)
admin.site.register(Delivery)
admin.site.register(Request)
admin.site.register(Request_Category)
admin.site.register(Request_Comment)
admin.site.register(Request_WatchList)