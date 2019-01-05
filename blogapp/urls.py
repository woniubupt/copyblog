from django.conf.urls import url

from blogapp.views import user_views, blog_views

urlpatterns = [
    url(r'^register/$', user_views.register, name='blogregister'),
    url(r'^login/$', user_views.login, name='bloglogin'),
    url(r'^addblog/$', blog_views.addBlog, name='addblog'),
    url(r'^bloglist/$', blog_views.list, name='bloglist'),
    url(r'^detailblog/$', blog_views.detailBlog, name='detailblog'),
    url(r'^editblog/$', blog_views.editBlog, name='editblog'),
    url(r'^delblog/$', blog_views.delBlog, name='delblog'),
    url(r'^search/$', blog_views.search, name='search'),
    url(r'^logout/$', user_views.logout, name='logout'),
]

