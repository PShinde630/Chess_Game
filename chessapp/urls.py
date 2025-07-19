from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from chessapp import views  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logout_view, name='logout_view'),
    path('signup/', views.signup_view, name='signup_view'),
    path('history/', views.history, name='history'),
    path('active-users/', views.active_users_view, name='active_users_view'),
    path('challenge/', views.challenge, name='challenge'),
    path('pending-challenges/', views.pending_challenges_view, name='pending_challenges'),
    path('decline-challenge/<int:challenge_id>/', views.decline_challenge_view, name='decline_challenge'),
    path('accept-challenge/<int:challenge_id>/', views.accept_challenge_view, name='accept_challenge'),
    path('game-state/<int:game_id>/', views.game_state, name='game_state'),
    path('ongoing-game/', views.ongoing_game, name='ongoing_game'),  
    path('make-move/<int:game_id>/', views.process_view, name='process_view'),
    path('resign-game/<int:game_id>/', views.resign_game_view, name='resign_game_view'),  
    path('game/<int:game_id>/', views.game_page, name='game_page'),  
    path('rules/', views.rules_view, name='rules'),
    path('about/', views.about_view, name='about'),
    path('chesshistory/', views.chesshistory_view, name='chesshistory'),
    path('edit-game/<int:game_id>/', views.edit_journal, name='edit_journal'),
    path('delete-game/<int:game_id>/', views.delete_journal, name='delete_journal'),
]





