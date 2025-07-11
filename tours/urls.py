from django.contrib.auth import views as auth_views
from django.urls import include, path

from . import views
from .views import RoleBasedLoginView, login_redirect_view

urlpatterns = [
    # ===== Public Pages =====
    path("", views.home, name="home"),
    path("gallery/", views.gallery, name="gallery"),
    path("contact/", views.contact, name="contact"),
    path("about/", views.about, name="about"),
    path("health/", views.health_view, name="health"),
    path("health/thank-you/", views.health_thankyou, name="health_thankyou"),

    # ===== Vacation Tours =====
    path("vacation/", views.vacation_tours, name="vacation"),
    path("vacation/<int:id>/", views.vacation_detail, name="vacation_detail"),

    # ===== Domestic Tours =====
    path("domestic/", views.domestic_tours_view, name="domestic_tours"),
    path("domestic/<int:id>/", views.domestic_tour_detail, name="domestic_tour_detail"),

    # ===== Umrah Packages =====
    path("umrah-packages/", views.umra_package_list, name="umra_package_list"),
    path("umrah/<int:id>/", views.umrah_detail, name="umrah_detail"),

    # ===== Tour Packages =====
    path("tour/<int:id>/", views.tour_detail, name="tour_detail"),

    # ===== Authentication =====
    path("redirect/", login_redirect_view, name="login_redirect"),
    path("accounts/login/", RoleBasedLoginView.as_view(), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
    path("accounts/", include("django.contrib.auth.urls")),  # Includes password reset/change/etc.

    # ===== Dashboards =====
    path("dashboard/manager/", views.manager_dashboard, name="manager_dashboard"),
    path("dashboard/staff/", views.staff_dashboard, name="staff_dashboard"),

    # ===== Notifications =====
    path("notifications/", views.user_notifications, name="notifications"),
]
