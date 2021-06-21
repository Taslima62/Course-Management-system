
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="home"),
    path("contact/", views.contact, name="contact"),
    
    path("my_class/", views.my_class, name="my_class"),
    path("login/",views.signin,name="login"),
    path("signup/",views.signup,name="signup"),
    path("logout/",views.user_logout,name="logout"),
    path("thank/",views.thank,name="thank"),
    path("change_password/",views.change_password,name="change_password"),

    path("create_class/",views.create_class,name="create_class"),
    path("join_class/",views.join_class,name="join_class"),
    path("edit_profile/",views.edit_profile,name="edit_profile"),
    path("enter_class/<int:course>/",views.enter_class,name="enter_class"),
    path("ask_question/",views.ask_question,name="ask_question"),
    path("ask_short_question/",views.ask_short_question,name="ask_short_question"),
    path("short_questions/",views.short_questions,name="short_questions"),
    path("answers/<int:question_id>/",views.answers,name="answers"),
    path("vote/<int:answers_id>/",views.vote,name="vote"),
    path("unmarked_answers/<int:question_id>/",views.unmarked_answers,name="unmarked_answers"),

    path("reply/",views.reply,name="reply"),
    path("dashboard/",views.dashboard,name="dashboard"),
    path("my_question/",views.my_question,name="my_question"),
    path("my_answer/",views.my_answer,name="my_answer"),
    path("delete/<int:question_id>/",views.delete,name="delete"),
    path("delete_answer/<int:answer_id>/",views.delete_answer,name="delete_answer"),
    path("test/",views.test,name="test"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)