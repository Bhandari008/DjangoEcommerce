from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .import views
from shop.views import SearchResultsListView

app_name = 'shop'

urlpatterns = [
    path('store/',views.product_store,name='product_store'),
    path('',views.product_list,name='product_list'),
    path('search/',SearchResultsListView.as_view(),name='search_results'),
    path('<slug:category_slug>/',views.product_list,name='product_list_by_category'),   
    path('<int:id>/<slug:slug>/',views.product_detail,name='product_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    