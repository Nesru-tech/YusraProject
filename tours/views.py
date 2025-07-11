from datetime import datetime

from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .models import (
    Booking, ContactMessage, Customer, GalleryImage, Notification, SlideImage,
    TourPackage, UmraPackage, VacationTour, DomesticTour
)

# ==============================
# Role Check Functions
# ==============================
def is_manager(user):
    return user.groups.filter(name="Manager").exists()

def is_staff(user):
    return user.groups.filter(name="Staff").exists()

# ==============================
# Custom Login Form (with Remember Me)
# ==============================
class CustomLoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Username"
        })
        self.fields["password"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Password",
            "id": "password-field"
        })

# ==============================
# Custom Login View with Role Redirect
# ==============================
class RoleBasedLoginView(LoginView):
    authentication_form = CustomLoginForm

    def get_success_url(self):
        user = self.request.user
        if user.groups.filter(name="Manager").exists():
            return "/dashboard/manager/"
        elif user.groups.filter(name="Staff").exists():
            return "/dashboard/staff/"
        return "/"

# ==============================
# Dashboards
# ==============================
@login_required
@user_passes_test(is_manager)
def manager_dashboard(request):
    user_groups = request.user.groups.values_list("name", flat=True)
    notifications = Notification.objects.filter(
        target_group__in=user_groups
    ).order_by("-created_at")[:5]

    context = {
        "total_bookings": Booking.objects.count(),
        "total_customers": Customer.objects.count(),
        "total_packages": TourPackage.objects.count(),
        "notifications": notifications,
    }
    return render(request, "tours/manager_dashboard.html", context)

@login_required
@user_passes_test(is_staff)
def staff_dashboard(request):
    context = {
        "my_bookings": Booking.objects.filter(customer__email=request.user.email),
    }
    return render(request, "tours/staff_dashboard.html", context)

@login_required
def login_redirect_view(request):
    if is_manager(request.user):
        return redirect("manager_dashboard")
    elif is_staff(request.user):
        return redirect("staff_dashboard")
    return redirect("home")

@login_required
def user_notifications(request):
    user_groups = request.user.groups.values_list("name", flat=True)
    notifications = Notification.objects.filter(target_group__in=user_groups)
    return render(request, "tours/notifications.html", {"notifications": notifications})

# ==============================
# Public Pages
# ==============================
def home(request):
    slides = SlideImage.objects.filter(is_active=True).order_by("-created_at")
    domestic_tours = DomesticTour.objects.all()[:3]

    query = request.GET.get("search", "")
    tour_results = TourPackage.objects.none()
    umrah_results = UmraPackage.objects.none()
    vacation_results = VacationTour.objects.none()
    domestic_results = DomesticTour.objects.none()
    results_found = False

    if query:
        tour_results = TourPackage.objects.filter(name__icontains=query)
        umrah_results = UmraPackage.objects.filter(name__icontains=query)
        vacation_results = VacationTour.objects.filter(title__icontains=query)
        domestic_results = DomesticTour.objects.filter(title__icontains=query)

        results_found = any([
            tour_results.exists(),
            umrah_results.exists(),
            vacation_results.exists(),
            domestic_results.exists(),
        ])

    search_results = [
        {"label": "Umrah Packages", "results": umrah_results, "model": "umrah"},
        {"label": "Vacation Tours", "results": vacation_results, "model": "vacation"},
        {"label": "Domestic Tours", "results": domestic_results, "model": "domestic"},
    ]

    return render(request, "tours/home.html", {
        "slides": slides,
        "domestic_tours": domestic_tours,
        "query": query,
        "results_found": results_found,
        "search_results": search_results,
    })

def gallery(request):
    images = GalleryImage.objects.all().order_by("-upload_date")
    return render(request, "tours/gallery.html", {"images": images})

def vacation_tours(request):
    vacation_tours = VacationTour.objects.all().order_by("available_from")
    return render(request, "tours/vacation.html", {"vacation_tours": vacation_tours})

def vacation_detail(request, id):
    tour = get_object_or_404(VacationTour, id=id)
    return render(request, "tours/vacation_detail.html", {"tour": tour})

def domestic_tours_view(request):
    tours = DomesticTour.objects.all()
    query = request.GET.get('q')
    if query:
        tours = tours.filter(Q(title__icontains=query) | Q(location__icontains=query))
    sort_by = request.GET.get('sort')
    if sort_by:
        tours = tours.order_by(sort_by)
    paginator = Paginator(tours, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'tours/domestic_tour.html', {'vacation_tours': page_obj})

def domestic_tour_detail(request, id):
    tour = get_object_or_404(DomesticTour, id=id)
    return render(request, 'tours/domestic_tour_detail.html', {'tour': tour})

def umra_package_list(request):
    packages = UmraPackage.objects.all()
    selected_country = request.GET.get("country", "")
    selected_date = request.GET.get("date", "")
    selected_sort = request.GET.get("sort", "")

    if selected_country:
        packages = packages.filter(country=selected_country)
    if selected_date:
        try:
            date_obj = datetime.strptime(selected_date, "%Y-%m-%d").date()
            packages = packages.filter(available_from__gte=date_obj)
        except ValueError:
            pass
    if selected_sort == "price_asc":
        packages = packages.order_by("price")
    elif selected_sort == "price_desc":
        packages = packages.order_by("-price")
    elif selected_sort == "date_asc":
        packages = packages.order_by("available_from")
    elif selected_sort == "date_desc":
        packages = packages.order_by("-available_from")

    all_countries = UmraPackage.objects.values_list("country", flat=True).distinct()
    return render(request, "tours/umra.html", {
        "umra_packages": packages,
        "all_countries": all_countries,
        "selected_country": selected_country,
        "selected_date": selected_date,
        "selected_sort": selected_sort,
    })

def umrah_detail(request, id):
    package = get_object_or_404(UmraPackage, id=id)
    return render(request, "tours/umrah_detail.html", {"package": package})

def tour_detail(request, id):
    tour = get_object_or_404(TourPackage, id=id)
    return render(request, "tours/tour_detail.html", {"tour": tour})

def about(request):
    return render(request, 'tours/about.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        phone_number = request.POST.get("phone_number", "").strip()
        subject = request.POST.get("subject", "").strip()
        message = request.POST.get("message", "").strip()

        ContactMessage.objects.create(
            name=name,
            email=email,
            phone_number=phone_number,
            subject=subject,
            message=message,
        )

        email_subject = f"New message from {name}"
        email_body = (
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Phone: {phone_number}\n"
            f"Subject: {subject}\n\n"
            f"Message:\n{message}"
        )

        try:
            send_mail(
                subject=email_subject,
                message=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[
                    "nesredinjuneidi16@gmail.com",
                    "fayyajemal@gmail.com",
                    "yusratourandtravel@gmail.com"
                ],
                fail_silently=False,
            )
            messages.success(request, "✅ Your message has been sent successfully!")
        except Exception as e:
            messages.error(request, f"❌ Failed to send email: {e}")

        return redirect("contact")

    return render(request, "tours/contact.html")

def health_view(request):
    return render(request, "tours/health.html")

def health_thankyou(request):
    return render(request, "tours/thank_you.html")
