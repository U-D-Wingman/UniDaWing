from django.shortcuts import render

# Create your views here.
# _*_ coding="utf-8" _*_

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db import models
from django.core.files.base import ContentFile

from . import util
from .models import *
# from .models import User, Category, Auction, Bid, WatchList, Comment, AucPic, SportField


# from .forms import CreateForm


def index(request):
        title = '首页'
        page_content=[]
        entries=util.list_entries()

        dict_vars = {"title": title, "entries":entries,"page_content":page_content }

        return render(request, "home.html", dict_vars)



def auctionindex(request):
    auctions = {}
    auctions = Auction.objects.filter(active=True).all()
    dict_vars={"auctions":auctions}
    return render(request, "auctions/index.html",dict_vars)


def sportsindex(request):
        title = 'Active listings'
    
        sportfields = SportField.objects.all()
    
        dict_vars = {"title": title, "sportfields": sportfields}

        return render(request, "sports/sportsindex.html", dict_vars)


def delivery(request):
    deli = Delivery.objects.all()
    dict_vars={"deliveries":deli}
    return render(request,"deliveries/deliveries.html",dict_vars)


def requestindex(request):
    requests={}
    requests= Request.objects.filter(active=True).all()
    dict_vars={"requests":requests}
    return render(request, "request/index.html",dict_vars)

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")


@login_required
def create_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        category_id = request.POST["category"]
        url = request.POST["article_img"]
        initial_price = request.POST["initial_price"]
        current_user="su"
        pic = request.FILES.get('article_img_local')
        auction = Auction(title=title, description=description, initial_price=initial_price,
                          owner=request.user, category=Category.objects.get(pk=category_id), active=True,
                          article_image=url,image=pic,current_highest_price=initial_price)
    #    pic_name=str(auction.pk)+".jpg"
    #    aucpic=AucPic(name=pic_name,image=pic)
        auction.save()
    #    aucpic.save()
        return HttpResponseRedirect(reverse('listed_article', args=[auction.id],))

    dict_vars = {"categories": Category.objects.all()}

    return render(request, "auctions/create_listing.html", dict_vars)


def listed_article(request, article_id):
    article = Auction.objects.get(pk=article_id)
    last_bids = Bid.objects.filter(auction=article).order_by("created")
    bids_count = Bid.objects.filter(auction=article).count()
    auctions_ids_in_watch_list = {}
    if request.user.is_authenticated:
        auctions_ids_in_watch_list = WatchList.objects.filter(user=request.user).values_list('auction', flat=True)

    if request.method == "POST":
        bid = Bid(user=request.user, auction=article, price=request.POST["new_bid"])
        bid.save()
        if float(request.POST["new_bid"])>article.current_highest_price:
            article.current_highest_price=float(request.POST["new_bid"])
            article.save()
        return HttpResponseRedirect(reverse("listed_article", args=[article_id]))

    dict_vars = {"article": article, "bids": last_bids, "bids_counts": bids_count}
    dict_vars.update({"comments": Comment.objects.filter(auction=article).order_by("-created").all(),
                      "auctions_ids_in_watch_list": auctions_ids_in_watch_list})
    return render(request, "auctions/listed_article.html", dict_vars)


@login_required
def watch_list(request):
    if request.method == "POST":
        article_id = request.POST["article_id"]
        auction = Auction.objects.get(pk=article_id)
        if WatchList.objects.filter(auction=auction, user=request.user).all().first() is None:
            w = WatchList(auction=auction, user=request.user)
            w.save()
        else:
            w = WatchList.objects.get(auction=auction, user=request.user)
            w.delete()
        return HttpResponseRedirect(reverse("listed_article", args=[article_id]))

    title = 'My watchlist'
    ids = WatchList.objects.filter(user=request.user).values_list('auction', flat=True)
    auctions = Auction.objects.filter(id__in=ids)
    dict_vars = {"title": title, "auctions": auctions, "remove_article": True}

    return render(request, "auctions/index.html", dict_vars)


def close_auction(request,bid_id):
    if request.method == "POST":
        article_id = request.POST["article_id"]
        auction = Auction.objects.get(pk=article_id)
        choosed_bid = Bid.objects.get(pk=bid_id)
        if choosed_bid is not None:
            auction.final_buyer = choosed_bid.user
            auction.active = False
            auction.save()
        else:
            auction.active = False
            auction.save()
        return HttpResponseRedirect(reverse("listed_article", args=[article_id]))

def edit_auction(request,article_id):
    if request.method == "POST":
        # article_id = request.POST["article_id"]
        auction = Auction.objects.get(pk=article_id)
        # title = request.POST["title"]
        # description = request.POST["description"]
        # category_id = request.POST["category"]
        # url = request.POST["article_img"]
        # initial_price = request.POST["initial_price"]

        dict_vars = {"auction": auction,"categories":Category.objects.all(),"test":str(auction.category)}

        # dict_vars.update({"comments": Comment.objects.filter(auction=article).order_by("-created").all(),
        #                   "auctions_ids_in_watch_list": auctions_ids_in_watch_list})
        return render(request,"auctions/edit_listing.html", dict_vars)

    dict_vars = {"categories": Category.objects.all()}

    return render(request, "auctions/edit_listing.html", dict_vars)

def save_edit(request,article_id):
    if request.method == "POST":
        auction=Auction.objects.get(pk=article_id)
        if request.POST["title"]:
            auction.title = request.POST["title"]
        if request.POST["description"]:
            auction.description = request.POST["description"]
        if request.POST["category"]:
            auction.category_id = request.POST["category"]
        if request.POST["initial_price"]:
            auction.initial_price = request.POST["initial_price"]
        if request.POST["article_img"]:
            auction.url = request.POST["article_img"]
        if request.FILES.get("article_img_local"):
            auction.image = request.FILES.get("article_img_local")

        auction.save()

        return HttpResponseRedirect(reverse('listed_article', args=[auction.id]))

    dict_vars = {"categories": Category.objects.all()}

    return render(request, "auctions/edit_listing.html", dict_vars)

@login_required
def winning_listing(request):
    title = "My buys"

    auctions = {}

    if request.user.is_authenticated:
        auctions = Auction.objects.filter(final_buyer=request.user.pk).all()
    dict_vars = {"title": title, "auctions": auctions}

    return render(request, "auctions/index.html", dict_vars)


@login_required
def my_listing(request):
    title = "My listing"

    auctions = {}

    if request.user.is_authenticated:
        auctions = Auction.objects.filter(owner=request.user.pk).all()

    dict_vars = {"title": title, "auctions": auctions}

    return render(request, "auctions/index.html", dict_vars)


def make_comment(request, article_id):
    if request.method == "POST":
        article = Auction.objects.get(pk=article_id)
        comment = Comment(user=request.user, auction=article, text=request.POST["comment_text"])
        if len(comment.text) == 0: return HttpResponseRedirect(reverse("listed_article", args=[article_id]))
        comment.save()
        return HttpResponseRedirect(reverse("listed_article", args=[article_id]))


def categories(request):
    categories = Category.objects.all()
    dict_vars = {"categories": categories}
    return render(request, "auctions/categories.html", dict_vars)


def listed_article_by_category(request, category_id):
    category = Category.objects.get(pk=category_id)
    dict_vars = {"title": category.name,
                 "auctions": category.auctions.filter(active=True)}

    return render(request, "auctions/index.html", dict_vars)


def sportfields(request):
    try:
        title = 'Active listings'

        sportfields = {}
        sportfields = SportField.objects.filter(active=True).all()

        dict_vars = {"title": title, "sportfields": sportfields}

        return render(request, "auctions/sportfields.html", dict_vars)
    except:
        return render(request, "auctions/error.html", dict_vars)


###################################################################################
"""
    Request System
"""

@login_required
def create_request(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        date_time =request.POST["date_time"]
        category_id = request.POST["category"]
        num_joins=1
        # url = request.POST["article_img"]
        # initial_price = request.POST["initial_price"]
        current_user = "su"
        # pic = request.FILES.get('article_img_local')
        req = Request(title=title, description=description,
                      num_joins=num_joins, bringup_time=date_time,active=True,
                      category=Request_Category.objects.get(pk=category_id))
        #    pic_name=str(auction.pk)+".jpg"
        #    aucpic=AucPic(name=pic_name,image=pic)
        req.save()
        #    aucpic.save()

        w = Request_WatchList(request=req, user=request.user)
        w.save()
        return HttpResponseRedirect(reverse('listed_request', args=[req.id], ))

    dict_vars = {"categories": Request_Category.objects.all()}

    return render(request, "request/create_listing.html", dict_vars)

# def listed_request(request, request_id):
#     req = Request.objects.get(pk=request_id)
#
#     requests_ids_in_watch_list = {}
#     if request.user.is_authenticated:
#         requests_ids_in_watch_list = WatchList.objects.filter(user=request.user).values_list('auction', flat=True)
#
#     if request.method == "POST":
#         bid = Bid(user=request.user, auction=article, price=request.POST["new_bid"])
#         bid.save()
#         return HttpResponseRedirect(reverse("listed_article", args=[article_id]))
#
#     dict_vars = {"article": article, "last_bid": last_bid, "bids_count": bids_count}
#     dict_vars.update({"comments": Comment.objects.filter(auction=article).order_by("-created").all(),
#                       "auctions_ids_in_watch_list": auctions_ids_in_watch_list})
#     return render(request, "auctions/listed_article.html", dict_vars)



def listed_request(request, request_id):
    req = Request.objects.get(pk=request_id)
    # last_bid = Bid.objects.filter(req=article).order_by("created").last()
    # bids_count = Bid.objects.filter(req=article).count()
    requests_ids_in_watch_list = {}
    requests_ids_in_joined_list = {}
    if request.user.is_authenticated:
        requests_ids_in_watch_list = Request_WatchList.objects.filter(user=request.user).values_list('request', flat=True)
        requests_ids_in_joined_list = Request_Joined_List.objects.filter(user=request.user).values_list('request', flat=True)
    if request.method == "POST":
        # bid = Bid(user=request.user, req=article, price=request.POST["new_bid"])
        # bid.save()
        # req.num_joins=req.num_joins+1
        # req.save()
        return HttpResponseRedirect(reverse("listed_request", args=[request_id]))

    dict_vars = {"request": req}
    dict_vars.update({"requests_ids_in_watch_list":requests_ids_in_watch_list,
                      "requests_ids_in_joined_list":requests_ids_in_joined_list,
                      "comments": Request_Comment.objects.filter(request=req).order_by("-created").all()
                      })
    return render(request, "request/listed_article.html", dict_vars)

@login_required
def watch_request(request):
    if request.method == "POST":
        request_id = request.POST["request_id"]
        req = Request.objects.get(pk=request_id)
        if Request_WatchList.objects.filter(request=req, user=request.user).all().first() is None:
            w = Request_WatchList(request=req, user=request.user)
            w.save()
        else:
            w = Request_WatchList.objects.get(request=req, user=request.user)
            w.delete()
        return HttpResponseRedirect(reverse("listed_request", args=[request_id]))

    title = 'My Request Watchlist'
    ids = Request_WatchList.objects.filter(user=request.user).values_list('request', flat=True)
    reqs = Request.objects.filter(id__in=ids)
    dict_vars = {"title": title, "requests": reqs, "remove_article": True}

    return render(request, "request/index.html", dict_vars)

@login_required
def successful_request(request):
    title = "My successful request"

    if request.user.is_authenticated:
        reqs = Request_Joined_List.objects.filter(user=request.user).all()
        # reqs = Request.objects.filter(reqs.request.success==True)
    dict_vars = {"title": title, "requests": reqs}

    return render(request, "request/successful.html", dict_vars)


@login_required
def joined_request(request):
    if request.method == "POST":
        request_id = request.POST["request_id"]
        req = Request.objects.get(pk=request_id)
        if Request_Joined_List.objects.filter(request=req, user=request.user).all().first() is None:
            j = Request_Joined_List(request=req, user=request.user)
            j.save()
            req.num_joins=req.num_joins+1
            req.save()
        else:
            j = Request_Joined_List.objects.get(request=req, user=request.user)
            j.delete()
            req.num_joins=req.num_joins-1
            req.save()
        return HttpResponseRedirect(reverse("listed_request", args=[request_id]))

    title = 'My Joined Request'
    ids = Request_Joined_List.objects.filter(user=request.user).values_list('request', flat=True)
    reqs = Request.objects.filter(id__in=ids)
    dict_vars = {"title": title, "requests": reqs, "remove_article": True}

    return render(request, "request/index.html", dict_vars)


def request_comment(request, request_id):
    if request.method == "POST":
        req = Request.objects.get(pk=request_id)
        comment = Request_Comment(user=request.user, request=req, text=request.POST["comment_text"])
        if len(comment.text) == 0: return HttpResponseRedirect(reverse("listed_request", args=[request_id]))
        comment.save()
        return HttpResponseRedirect(reverse("listed_request", args=[request_id]))


def request_categories(request):
    categories = Request_Category.objects.all()
    dict_vars = {"categories": categories}
    return render(request, "request/categories.html", dict_vars)


def listed_request_by_category(request, category_id):
    category = Request_Category.objects.get(id=category_id)
    dict_vars = {"title": category.name,
                 "requests": category.requests.filter(active=True)}

    return render(request, "request/index.html", dict_vars)

def appoint(request,sportfield_id):
   if request.method == "POST":
       afield=SportField.objects.get(pk=sportfield_id)
       afield.active=False
       afield.cur_user=request.user
       aptm = Appointment(founder=request.user, field=afield,description="Default Rent",active=True)
       aptm.save()
       afield.save()
   sportfields = SportField.objects.all()
   return render(request,"sports/sportsindex.html",{"sportfields": sportfields}
)

def deappoint(request,sportfield_id):
   if request.method == "POST":
       afield=SportField.objects.get(pk=sportfield_id)
       afield.active=True
       afield.cur_user=None
       afield.save()
   sportfields = SportField.objects.all()
   return render(request,"sports/sportsindex.html",{"sportfields": sportfields}
)

def chat(request):
    chats=Chatting.objects.all()
    dict_vars={"chats":chats}
    if request.method == "POST":
        chat = Chatting(user=request.user, text=request.POST["chat_text"])
        if len(chat.text)==0: return render(request,"sports/chattingroom.html",dict_vars)

        chat.save()
    return render(request,"sports/chattingroom.html",dict_vars)

def personal(request):
    tar_user=request.user
    
    dict_vars={"user":tar_user}
    return render(request,"personal.html",dict_vars)