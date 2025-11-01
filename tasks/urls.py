from django.urls import path
# import form views:
from tasks.views import UpdateTask,ManagerView,CreateTaskView, ViewProject,CreateProject, DeleteTaskView, Test , CreateEmployeeRegister ,User , dashboard , DetailsTaskView
from core.views import no_permission
urlpatterns = [
    path('test/',Test),
    path('create-employee/',CreateEmployeeRegister.as_view()),
    path('create-project/',CreateProject.as_view(),name="create-project"),
    path('view-project/',ViewProject.as_view(),name="view-project"),
    path('create-task/',CreateTaskView.as_view(),name="create_task"),
    path('task/<int:pk>/',DetailsTaskView.as_view(),name="task"),
    path('manager/',ManagerView.as_view(),name="manager-dashboard"),
    path('user/',User,name="user-dashboard"),
    # path('delete-task/<int:id>/',delete_task,name="delete_task_item"),
    path('delete-task/<int:id>/',DeleteTaskView.as_view(),name="delete_task_item"),
    path('update-task/<int:id>/',UpdateTask.as_view(),name="update-task"),
    path('no-permission/',no_permission,name="no-permission"),
    path('dashboard/',dashboard , name="dashboard")
]
