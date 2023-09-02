from django.urls import path
from .views import *

urlpatterns = [
    path('', AdvertisementList.as_view(), name='advertisement_list'),
    path('myadvertisements/', MyAdvertisementList.as_view(), name='myadvertisement_list'),
    path('advertisement/<int:pk>/edit/', AdvertisementUpdate.as_view(), name='advertisement_edit'),
    path('advertisement/<int:pk>/reaction/', ReactionCreate.as_view(), name='reaction_edit'),
    path('advertisement/create/', AdvertisementCreate.as_view(), name='advertisement_create'),
    path('reactions/', ReactionList.as_view(), name='reaction_list'),
    path('reaction/<int:pk>/accept/', set_reaction_accept, name='reaction_accept'),
    path('reaction/<int:pk>/refused/', set_reaction_refused, name='reaction_accept'),
    path('reaction/<int:pk>/delete/', set_reaction_delete, name='reaction_accept'),
    path('categorys/', CategoryList.as_view(), name='category_list'),
    path('categorys/<int:pk>/', CategoryBlog.as_view(), name='category_blog'),
    path('categorys/<int:pk>/edit/', CategoryUpdate.as_view(), name='category_edit'),
    path('categorys/create/', CategoryCreate.as_view(), name='category_create'),
    path('news/', NewsList.as_view(), name='news_list'),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
]
