import pillow_heif
import re
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date, datetime
from .images_urls import *
from PIL import Image
from django.core.exceptions import ValidationError

IMAGE_VC = "?v=1"
def validate_allowed_countries(value):
    number_str = str(value)

    patterns = [
        r'^\+20(10|11|12|15)\d{8}$',
        r'^\+9665\d{8}$',
        r'^\+9715\d{8}$',
    ]

    if not any(re.match(p, number_str) for p in patterns):
        raise ValidationError("The phone number must be from Egypt, Saudi Arabia or the UAE in the correct international format.")

class UserProfile(AbstractUser):
    USER_TYPE_CHOICES = [
        ('patient', 'مريض'),
        ('doctor', 'طبيب'),
        ('admin', 'مدير'),
        ('clinic_admin', 'مدير عيادة'),
    ]

    GENDER_CHOICES = [
        ('male', 'ذكر'),
        ('female', 'أنثى'),
    ]

    # Basic information
    user_type = models.CharField(max_length=15, choices=USER_TYPE_CHOICES)
    national_id = models.CharField(max_length=14, unique=True, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, null=True, blank=True)

    # Account status
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True, blank=True, null=True)
    last_seen = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.full_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def age(self):
        if self.birth_date:
            today = date.today()
            return today.year - self.birth_date.year - (
                        (today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return None

class ProfilePicture(models.Model):
    user = models.ForeignKey(UserProfile, blank=True, null=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_profile, blank=True, null=True, max_length=6000)

    created_at = models.DateTimeField(auto_now=False, auto_now_add=True, blank=True, null=True)
    construction_user = models.ForeignKey(UserProfile, blank=True, null=True, on_delete=models.SET_NULL, related_name='ProfilePicture_construction_user')
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False, blank=True, null=True)
    last_updated_user = models.ForeignKey(UserProfile, blank=True, null=True, on_delete=models.SET_NULL, related_name='ProfilePicture_last_updated_user')

    def save(self, *args, **kwargs):
        if self.image:
            allowed_formats = ['JPEG', 'PNG', 'WEBP', 'HEIC']

            try:
                image = Image.open(self.image)
                if image.format not in allowed_formats:
                    raise ValidationError("Image type not supported")
            except Exception:
                try:
                    heif_file = pillow_heif.open_heif(self.image)
                    image = Image.frombytes(
                        heif_file.mode,
                        heif_file.size,
                        heif_file.data,
                        "raw",
                    )
                except Exception:
                    raise ValidationError("Failed to read image")

    def image_url(self):
        if self.image:
            return f"{self.image.url}{IMAGE_VC}"
        return ""

    def __str__(self):
        user_id = 0
        if self.user:
            user_id = self.user.id
        return f'img_id={self.id}&user_id={user_id}&create={self.updated_at.strftime("%m/%d/%Y, %I:%M %p")}&lest_update={self.updated_at.strftime("%m/%d/%Y, %I:%M %p")}'

class Emails(models.Model):
    user = models.ForeignKey(UserProfile, blank=True, null=True, on_delete=models.CASCADE, related_name='Emails_user')
    email = models.EmailField()
    is_credibility = models.BooleanField(default=False)
    is_main = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False, blank=True, null=True)

    def __str__(self):
        return f"{str(self.email)}"

    class Meta:
        ordering = ['-created_at', '-updated_at']

class Countries(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, name='name', db_index=True)
    city = models.CharField(max_length=100, blank=True, null=True, name='city', db_index=True)
    Region = models.CharField(max_length=100, blank=True, null=True, name='Region', db_index=True)
    key_networks = models.JSONField(default=list, blank=True, null=True)
    code = models.CharField(max_length=20, blank=True, null=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False, blank=True, null=True)

    def __str__(self):
        return f'{str(self.name)}'

    class Meta:
        ordering = ['-created_at', '-updated_at']
    def add_key(self, code):
        if code not in self.key:
            self.key.append(code)
            self.save()

    def remove_key(self, code):
        if code in self.key:
            self.key.remove(code)
            self.save()

class Mobiles(models.Model):
    user = models.ForeignKey(UserProfile, blank=True, null=True, on_delete=models.CASCADE, related_name='Mobiles_user')
    network = models.ForeignKey(Countries, blank=True, null=True, on_delete=models.SET_NULL, related_name='Mobiles_network')
    mobile = PhoneNumberField(blank=True, region="EG", validators=[validate_allowed_countries])

    is_credibility = models.BooleanField(default=False)
    is_main = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False, blank=True, null=True)

    def __str__(self):
        return f'{str(self.mobile)}'

    class Meta:
        ordering = ['-created_at', '-updated_at']

class Address(models.Model):
    country = models.ForeignKey(Countries, blank=True, null=True, on_delete=models.CASCADE, related_name='Address_country')
    user = models.ForeignKey(UserProfile, blank=True, null=True, on_delete=models.CASCADE, related_name='Address_user')
    latitude = models.FloatField(default=0, null=True, blank=True, name='latitude')
    longitude = models.FloatField(default=0, null=True, blank=True, name='longitude')
    address = models.CharField(max_length=500, blank=True, null=True, name='address')
    building = models.CharField(max_length=10, blank=True, null=True, name='building')
    floor = models.CharField(max_length=10, blank=True, null=True, name='floor')
    apartment = models.CharField(max_length=10, blank=True, null=True, name='apartment')
    street = models.CharField(max_length=3000, blank=True, null=True, name='street')
    additional_info = models.CharField(max_length=3000, blank=True, null=True, name='additional_info')
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False, blank=True, null=True)

    class Meta:
        ordering = ['-created_at', '-updated_at']

class Patient(models.Model):
    BLOOD_TYPE_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]

    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='patient_profile')

    # Basic medical information
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPE_CHOICES, blank=True)
    height = models.FloatField(null=True, blank=True, validators=[MinValueValidator(50)])
    weight = models.FloatField(null=True, blank=True, validators=[MinValueValidator(1)])

    # Emergency Information
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = PhoneNumberField(blank=True, region="EG", validators=[validate_allowed_countries])
    emergency_contact_relation = models.CharField(max_length=50, blank=True)

    # Medical history
    chronic_diseases = models.TextField(blank=True, help_text="الأمراض المزمنة مفصولة بفاصلة")
    allergies = models.TextField(blank=True, help_text="الحساسية من أدوية أو مواد معينة")
    current_medications = models.TextField(blank=True, help_text="الأدوية التي يتناولها حالياً")
    medical_history = models.TextField(blank=True, help_text="التاريخ الطبي والعمليات السابقة")

    # Preference settings
    preferred_language = models.CharField(max_length=10, choices=[('ar', 'العربية'), ('en', 'English')], default='ar')

    # statistics
    total_appointments = models.IntegerField(default=0)
    completed_appointments = models.IntegerField(default=0)
    cancelled_appointments = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"مريض: {self.user.full_name}"

    @property
    def bmi(self):
        if self.height and self.weight:
            height_m = self.height / 100
            return round(self.weight / (height_m ** 2), 2)
        return None

class UserBrowsers(models.Model):
    user = models.ForeignKey(UserProfile, blank=True, null=True, on_delete=models.CASCADE, related_name='UserBrowsers_user')
    token = models.TextField(blank=True, null=True)
    ln = models.CharField(max_length=60, blank=True, null=True)
    type = models.CharField(max_length=60, blank=True, null=True)
    os = models.CharField(max_length=60, blank=True, null=True)
    device = models.CharField(max_length=60, blank=True, null=True)
    brand = models.CharField(max_length=60, blank=True, null=True)
    model = models.CharField(max_length=60, blank=True, null=True)
    version = models.CharField(max_length=60, blank=True, null=True)
    encrypted_code = models.CharField(max_length=2000, blank=True, null=True)
    close_pass = models.BooleanField(default=False)
    is_done = models.BooleanField(default=False)
    website = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False, blank=True, null=True)

    def __str__(self):
        return f'user: {self.user} || type : {self.type} || token : {self.token}'

    class Meta:
        ordering = ['-created_at', '-updated_at']

class UserPasswords(models.Model):
    user = models.ForeignKey(UserProfile, blank=True, null=True, on_delete=models.CASCADE, related_name='UserPasswords_user')
    browser = models.ForeignKey(UserBrowsers, blank=True, null=True, on_delete=models.CASCADE, related_name='UserPasswords_browser')
    password = models.TextField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False, blank=True, null=True)

    def __str__(self):
        return f'user: {self.user.first_name}'

    class Meta:
        ordering = ['-created_at', '-updated_at']

class CredibilityCodes(models.Model):
    email = models.ForeignKey(Emails, default=None, blank=True, null=True, on_delete=models.CASCADE, related_name='CredibilityCodes_email')
    mobile = models.ForeignKey(Mobiles, default=None, blank=True, null=True, on_delete=models.CASCADE, related_name='CredibilityCodes_mobile')
    code = models.CharField(max_length=1000, null=True, blank=True)
    resat_pass_code = models.CharField(max_length=1000, null=True, blank=True)
    is_done = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    resat_pass = models.BooleanField(default=False)
    expired = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)

    number_attempts = models.BigIntegerField(default=0)

    created_at = models.DateTimeField(auto_now=False, auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False, blank=True, null=True)

    def __str__(self):
        if self.email:
            title_object = f"email: {self.email.email}"
        elif self.mobile:
            title_object = f"mobile: {self.mobile.mobile}"
        else:
            title_object = f""
        return f"code: {self.code}, {title_object}, Number attempts {self.number_attempts}, "

    class Meta:
        ordering = ['-created_at', '-updated_at']


