'''定义learning_logs的URL模式'''

from django.urls import path
from . import views

urlpatterns = [
    #主页 
    path('', views.index, name = 'index'),
    
    #显示所有的主题
    path('topics/', views.topics, name = 'topics'),
    
    #显示主题的详细页面
    path('topics/(?P<topic_id>\d+)/', views.topic, name = 'topic'),
    
    #用于添加新主题的网页
    path('new_topic/', views.new_topic, name = 'new_topic'),
    
    #用于添加新条目的页面
    path('new_entry/(?P<topic_id>\d+)/', views.new_entry, name = 'new_entry'),
    
    #用于编辑条目的页面
    path('edit_entry/(?P<entry_id>\d+)/', views.edit_entry, name = 'edit_entry'),
    
    ]
