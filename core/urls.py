from django.urls import path
from . import views

urlpatterns = [
    path('',                views.login_view,   name='login'),
    path('chiqish/',        views.logout_view,  name='logout'),
    path('bosh/',           views.dashboard,    name='dashboard'),
    path('royxat/',         views.royxat,       name='royxat'),
    path('sert/<str:tur>/<int:pk>/', views.sert_yuklash, name='sert_yuklash'),
    path('sert/ochir/<int:pk>/',     views.sert_ochir,   name='sert_ochir'),
    path('kpi/',            views.kpi,          name='kpi'),
    # Admin
    path('admin/users/',         views.users_list,   name='users_list'),
    path('admin/user/yangi/',    views.user_add,     name='user_add'),
    path('admin/user/ochir/<int:pk>/', views.user_delete, name='user_delete'),
    path('admin/tuzilma/',       views.tuzilma,      name='tuzilma'),
    path('admin/sertlar/',       views.admin_sertlar,name='admin_sertlar'),
    # Import
    path('import/',                  views.import_page,        name='import_page'),
    path('import/talabalar/',        views.import_talabalar,   name='import_talabalar'),
    path('import/xodimlar/',         views.import_xodimlar,    name='import_xodimlar'),
    path('import/oqituvchilar/',     views.import_oqituvchilar,name='import_oqituvchilar'),
    path('import/users/',            views.import_users,       name='import_users'),
    path('shablon/<str:tur>/',       views.shablon_yuklash,    name='shablon'),
]
