from django.urls import path, include
from .views import addAdvisor, registerUser, loginUser, getAdvisorList, bookAdvisor, getBookedCalls

urlpatterns = [
    path('admin/advisor', addAdvisor),
    path('user/register', registerUser),
    path('user/login', loginUser),
    path('user/<int:user_id>/advisor', getAdvisorList),
    path('user/<int:user_id>/advisor/<int:advisor_id>', bookAdvisor),
    path('user/<int:user_id>/advisor/booking', getBookedCalls),
    
]