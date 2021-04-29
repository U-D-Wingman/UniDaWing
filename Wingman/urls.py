# -*- codeing = utf-8 -*-
# @Time : 2021-04-27 0:15
# @Author: Puyang Chen
# @File : urls.py
# @Software: PyCharm
#_*_ coding="utf-8" _*_

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("my_listing", views.my_listing, name="my_listing"),
    path("listed_article/<int:article_id>", views.listed_article, name="listed_article"),
    path("watch_list", views.watch_list, name="watch_list"),
    path("close_auction", views.close_auction, name="close_auction"),
    path("edit_auction/<int:article_id>", views.edit_auction, name="edit_auction"),
    path("save_edit/<int:article_id>", views.save_edit, name="save_edit"),
    path("winning_listing", views.winning_listing, name="winning_listing"),
    path("comment_on/<int:article_id>", views.make_comment, name="make_comment"),
    path("categories", views.categories, name="categories"),
    path("listed_article_by_category/<int:category_id>", views.listed_article_by_category, name="listed_article_by_category"),
    path("sportfields",views.sportfields,name="sportfields"),
    path("auctionindex",views.auctionindex,name="auctionindex"),
    path("sportsindex",views.sportsindex,name="sportsindex"),
    path("deliveries",views.delivery,name="deliveries"),

    path("requsetindex",views.requestindex,name="requestindex"),
    path("create_request",views.create_request,name="create_request"),
    path("listed_request/<int:request_id>",views.listed_request,name="listed_request"),
    path("watch_request",views.watch_request,name="watch_request"),
    path("successful_request",views.successful_request,name="successful_request"),
    path("joined_request",views.joined_request,name="joined_request"),
    path("request_comment/<int:request_id>",views.request_comment,name="request_comment"),
    path("request_categories",views.request_categories,name="request_categories"),
    path("listed_request_by_category/<int:category_id>",views.listed_request_by_category,name="listed_request_by_category"),

    path("appoint/<int:sportfield_id>",views.appoint,name="appoint"),
    path("deappoint/<int:sportfield_id>",views.deappoint,name="deappoint"),
    path("chats",views.chat,name="chats"),
    path("personal",views.personal,name="personal")

]

