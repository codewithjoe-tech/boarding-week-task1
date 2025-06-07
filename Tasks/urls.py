from django.urls import path


from . views import TaskView

urlpatterns = [
    path('tasks' , TaskView.as_view()),
    path('task/<pk>', TaskView.as_view()),
]
