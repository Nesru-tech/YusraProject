from django.db import models
from django.urls import reverse


# ========== Tours and Packages ==========
class TourPackage(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("book_tour", args=[str(self.id)])


class UmraPackage(models.Model):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_from = models.DateField()
    image = models.ImageField(upload_to="umra_images/", blank=True, null=True)

    def __str__(self):
        return self.name


class VacationTour(models.Model):
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    duration = models.CharField(max_length=50)  # e.g., "5 days", "1 week"
    available_from = models.DateField()
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="vacation_tours/", blank=True, null=True)

    def __str__(self):
        return self.title




class DomesticTour(models.Model):  # <- this class MUST be defined
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default="Ethiopia")
    duration = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_from = models.DateField()
    image = models.ImageField(upload_to='tours/images/', blank=True, null=True)

    def __str__(self):
        return self.title
# ========== Media ==========
class SlideImage(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="slides/")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class GalleryImage(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="gallery/")
    description = models.TextField()
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title




class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)  # ✅ Required

    def __str__(self):
        return f"{self.name} - {self.subject}"

# ========== Booking System ==========
class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.name


class Booking(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="bookings"
    )
    package = models.ForeignKey(
        TourPackage, on_delete=models.CASCADE, related_name="bookings"
    )
    date = models.DateField()
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.customer.name} - {self.package.name} on {self.date}"


# ========== Notifications ==========
class Notification(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    target_group = models.CharField(
        max_length=50,
        choices=[
            ("Manager", "Manager"),
            ("Staff", "Staff"),
        ],
    )

    def __str__(self):
        return self.title
