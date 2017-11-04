from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name='student'
urlpatterns = [
    #home/ or / or student/
    url(r'student_login/$', views.studentlogin, name='student_off'),
    url(r'auth/$', views.auth_view ,name='auth'),
    url(r'edit_details/$', views.view_edit ,name='edit_page'),
    url(r'logout/$',views.logout,name='logout'),
    url(r'users/(?P<username>[A-Za-z_0-9]+)/$', views.profile, name='profile'),
#    url(r'loggedin/$',views.loggedin,name='loggedin'),
  #  url(r'invalid/$',views.invalid_login,name='invalid'),
    url(r'^home/',views.studentlogin, name='student'),
    url(r'^$', views.studentlogin, name='student'),
 #register new student
    url(r'register/$', views.studentregistration, name='student_register'),
    url(r'listproject/',views.listproject,name='list_project'),
    url(r'changed/', views.successfull_change,name='passchgsucc'),
    url(r'change_password/$', views.change_password, name='passchg'),
    url(r'offer_letter/', views.get_offer, name='offer'),
    url(r'success/',views.update_details,name="update"),
    url(r'taken_name/',views.already_taken,name="taken"),
    url(r'profile/(?P<username>[A-Za-z_0-9]+)/$', views.view_stud_details, name="stud_details"),
    url(r'download/', views.download, name="download"),
    url(r'resume/(?P<username>[A-Za-z_0-9]+)/$', views.resumed, name="resumed"),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
