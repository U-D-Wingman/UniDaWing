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
    path("winning_listing", views.winning_listing, name="winning_listing"),
    path("comment_on/<int:article_id>", views.make_comment, name="make_comment"),
    path("categories", views.categories, name="categories"),
    path("listed_article_by_category/<int:category_id>", views.listed_article_by_category, name="listed_article_by_category"),
    path("sportfields",views.sportfields,name="sportfields"),
    path("auctionindex",views.auctionindex,name="auctionindex"),
    path("sportsindex",views.sportsindex,name="sportsindex"),
    path("deliveries",views.delivery,name="deliveries")
]

