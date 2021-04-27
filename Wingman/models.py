from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

class Sport_Cat(models.Model):
    name=models.CharField(max_length=32)

    def __str__(self):
        return self.name

class Auction(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    initial_price = models.FloatField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_actions")
    final_buyer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                    related_name="bought_actions")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="auctions")
    active = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)
    article_image = models.URLField(null=True,blank=True)
    image=models.ImageField(null=True,blank=True,upload_to = "")

    def __str__(self):
        return f"title:{self.title}, " \
               f"owner: {self.owner}, " \
               f"active:{self.active}"

    @property
    def last_bid(self):
        return Bid.objects.filter(auction=self).order_by("created").last()


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bids")
    created = models.DateTimeField(auto_now_add=True)
    price = models.FloatField()

    def __str__(self):
        return f"user:{self.user.username}, " \
               f"auction: {self.auction.title}, " \
               f"price:{self.price}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"user:{self.user.username}, " \
               f"auction: {self.auction.title}, " \
               f"comment: {self.text} "


class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watch_lists")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="watch_lists")

class AucPic(models.Model):
    name=models.CharField(max_length=32)
    image=models.ImageField(upload_to = "")

class SportField(models.Model):
    name=models.CharField(max_length=64)
    type=models.ForeignKey(Sport_Cat,on_delete=models.CASCADE,related_name="sportfield")
    price=models.FloatField()
    active=models.BooleanField()
    cur_user=models.ForeignKey(User, on_delete=models.CASCADE, related_name="usingfield",null=True, blank=True)
    active_time=models.DateTimeField(auto_now_add=True)

class Appointment(models.Model):
    founder=models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointment")
    description=models.TextField()
    bringup_time=models.DateTimeField(auto_now_add=True)
    active=models.BooleanField()

class Del_Corp(models.Model):
    name=models.CharField(max_length=8)
    def __str__(self):
        return self.name

class Delivery(models.Model):
    corporation=models.ForeignKey(Del_Corp, on_delete=models.CASCADE, related_name="delivery")
    receiver=models.ForeignKey(User, on_delete=models.CASCADE, related_name="delivery",null=True,blank=True)
    description=models.CharField(max_length=32)
    active=models.BooleanField()

    def __str__(self):
        return f"Corp:{self.corporatiion}, " \
               f"receiver: {self.receiver}, " \
               f"active:{self.active}"

# ####################################################################
# """
#     Request System
# """

class Request_Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

class Request(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    bringup_time=models.DateTimeField(auto_now_add=True)
    num_joins = models.IntegerField(default=0)
    category = models.ForeignKey(Request_Category, on_delete=models.CASCADE, related_name="request")
    active = models.BooleanField()
    success= models.BooleanField(default=False)
    # user =models.ForeignKey(User, on_delete=models.CASCADE,related_name="request")
    def __str__(self):
        return f"title:{self.title},"\
               f"active:{self.active}"

class Request_Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="request_comments")
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name="request_comments")
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"user:{self.user.username}, " \
               f"auction: {self.request.title}, " \
               f"comment: {self.text} "

class Request_WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="request_watch_lists")
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name="request_watch_lists")

class Request_Joined_List(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="request_joined_lists")
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name="request_joined_lists")