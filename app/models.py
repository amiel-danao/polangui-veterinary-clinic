import uuid

from django.db import models
from django.forms import ValidationError
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from app.managers import CustomUserManager
from django.utils.http import int_to_base36
from smart_selects.db_fields import GroupedForeignKey, ChainedForeignKey
from dirtyfields import DirtyFieldsMixin
from django.core.management import call_command


ID_LENGTH = 30
DEVICE_ID_LENGTH = 15

# cred = credentials.Certificate(os.path.join(os.path.dirname(os.path.dirname(__file__)), "clinic-firebase-adminsdk-4g25g-b8cd5d3052.json"))
# FIREBASE_APP = firebase_admin.initialize_app(cred)
# FIREBASE_DB = firestore.client()


def id_gen() -> str:
    """Generates random string whose length is `ID_LENGTH`"""
    return int_to_base36(uuid.uuid4().int)[:ID_LENGTH]


class Brand(models.Model):
    title = models.CharField(max_length=75)
    summary = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    content = models.TextField(blank=True, null=True)


class Category(models.Model):
    # Field name made lowercase.
    parentid = models.ForeignKey(
        'self', models.DO_NOTHING, db_column='parentId', blank=True, null=True)
    title = models.CharField(max_length=75)
    # Field name made lowercase.
    metatitle = models.CharField(
        db_column='metaTitle', max_length=100, blank=True, null=True)
    slug = models.CharField(max_length=100)
    content = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Categories'


class Item(models.Model):
    # Field name made lowercase.
    productid = models.ForeignKey(
        'Product', models.DO_NOTHING, db_column='productId')
    # Field name made lowercase.
    brandid = models.ForeignKey(Brand, models.DO_NOTHING, db_column='brandId')
    # Field name made lowercase.
    # supplierid = models.ForeignKey('Customer', models.DO_NOTHING, db_column='supplierId')
    # Field name made lowercase.
    # orderid = models.ForeignKey('Order', models.DO_NOTHING, db_column='orderId')
    # sku = models.CharField(max_length=100)
    # mrp = models.FloatField()
    discount = models.FloatField()
    price = models.FloatField()
    quantity = models.PositiveSmallIntegerField()
    sold = models.SmallIntegerField()
    available = models.BooleanField()
    defective = models.BooleanField()
    # Field name made lowercase.
    # createdby = models.BigIntegerField(db_column='createdBy')
    # Field name made lowercase.
    # updatedby = models.BigIntegerField(db_column='updatedBy', blank=True, null=True)
    # Field name made lowercase.
    # createdat = models.DateTimeField(auto_now_add=True)
    # Field name made lowercase.
    updated_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)


class Order(models.Model):
    # Field name made lowercase.
    userid = models.ForeignKey(
        'Customer', models.DO_NOTHING, db_column='userId')
    type = models.SmallIntegerField()
    status = models.SmallIntegerField()
    # Field name made lowercase.
    subtotal = models.FloatField(db_column='subTotal')
    # Field name made lowercase.
    itemdiscount = models.FloatField(db_column='itemDiscount')
    tax = models.FloatField()
    shipping = models.FloatField()
    total = models.FloatField()
    promo = models.CharField(max_length=50, blank=True, null=True)
    discount = models.FloatField()
    # Field name made lowercase.
    grandtotal = models.FloatField(db_column='grandTotal')
    # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')
    # Field name made lowercase.
    updatedat = models.DateTimeField(
        db_column='updatedAt', blank=True, null=True)
    content = models.TextField(blank=True, null=True)


class OrderItem(models.Model):
    # Field name made lowercase.
    productid = models.ForeignKey(
        'Product', models.DO_NOTHING, db_column='productId')
    # Field name made lowercase.
    itemid = models.ForeignKey(Item, models.DO_NOTHING, db_column='itemId')
    # Field name made lowercase.
    orderid = models.ForeignKey(Order, models.DO_NOTHING, db_column='orderId')
    sku = models.CharField(max_length=100)
    price = models.FloatField()
    discount = models.FloatField()
    quantity = models.SmallIntegerField()
    # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')
    # Field name made lowercase.
    updatedat = models.DateTimeField(
        db_column='updatedAt', blank=True, null=True)
    content = models.TextField(blank=True, null=True)


class Product(models.Model):
    title = models.CharField(max_length=75, blank=False)
    summary = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=75, blank=False)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    content = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class ProductCategory(models.Model):
    # Field name made lowercase.
    productid = models.OneToOneField(
        Product, models.DO_NOTHING, db_column='productId', primary_key=True)
    # Field name made lowercase.
    categoryid = models.ForeignKey(
        Category, models.DO_NOTHING, db_column='categoryId')

    class Meta:
        db_table = 'product_category'
        unique_together = (('productid', 'categoryid'),)
        verbose_name_plural = 'Product Categories'


class ProductMeta(models.Model):
    # Field name made lowercase.
    productid = models.ForeignKey(
        Product, models.DO_NOTHING, db_column='productId')
    key = models.CharField(max_length=50)
    content = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = (('productid', 'key'),)


class Transaction(models.Model):
    # Field name made lowercase.
    userid = models.ForeignKey(
        'Customer', models.DO_NOTHING, db_column='userId')
    # Field name made lowercase.
    orderid = models.ForeignKey(Order, models.DO_NOTHING, db_column='orderId')
    code = models.CharField(max_length=100)
    type = models.SmallIntegerField()
    mode = models.SmallIntegerField()
    status = models.SmallIntegerField()
    # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')
    # Field name made lowercase.
    updatedat = models.DateTimeField(
        db_column='updatedAt', blank=True, null=True)
    content = models.TextField(blank=True, null=True)


class Breed(models.Model):
    breed_name = models.CharField(
        max_length=80, primary_key=True, unique=True, blank=False)
    SPECIES_CHOICES = (
        ('Cat', 'Cat'),
        ('Dog', 'Dog'),
    )
    species = models.CharField(max_length=10, choices=SPECIES_CHOICES)

    def __str__(self):
        return self.breed_name


class Customer(models.Model):
    id = models.CharField(max_length=ID_LENGTH,
                          primary_key=True, default=id_gen)
    # Field name made lowercase.
    firstname = models.CharField(max_length=50, blank=True, null=True)
    # Field name made lowercase.
    middlename = models.CharField(max_length=50, blank=True, null=True)
    # Field name made lowercase.
    lastname = models.CharField(max_length=50, blank=True, null=True)
    mobile = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(
        max_length=254, unique=True, blank=False, null=False)
    picture = models.ImageField(
        upload_to='images/', blank=True, null=True, default='')

    def __str__(self):
        if not self.firstname and not self.lastname:
            return self.email
        return f'{self.firstname} {self.lastname}'

    @property
    def get_photo_url(self):
        if self.picture and hasattr(self.picture, 'url'):
            return self.picture.url
        else:
            return "/static/logo/app_icon.png"

SPECIES_CHOICES = (
    ('Cat', 'Cat'),
    ('Dog', 'Dog'),
)

class Pet(models.Model):
    id = models.CharField(max_length=ID_LENGTH,
                          primary_key=True, default=id_gen, editable=False)
    owner = models.ForeignKey(Customer, blank=False,
                              null=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=False, null=False)
    date_of_birth = models.DateTimeField(default=timezone.now)
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    weight = models.FloatField(validators=[MinValueValidator(0)], default=0)
    height = models.FloatField(validators=[MinValueValidator(0)], default=0)
    
    species = models.CharField(
        max_length=10, default='Cat', choices=SPECIES_CHOICES)
    breed = models.ForeignKey(
        Breed,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    allergies = models.CharField(max_length=50, blank=True)
    existing_conditions = models.CharField(max_length=80, blank=True)
    image = models.ImageField(
        upload_to='images/', blank=True, null=True, default='')

    def __str__(self):
        return f'{self.name} - ({self.owner.email})'

    class Meta:
        unique_together = ('name', 'owner',)

    @property
    def get_photo_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return "/static/logo/app_icon.png"

class MedicalHistory(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length=200, blank=True)
    veterinarian = models.CharField(max_length=50, blank=False, null=False)
    diagnosis = models.CharField(max_length=200, blank=False)
    tests_performed = models.CharField(max_length=200, blank=True, null=True)
    test_results = models.CharField(max_length=200, blank=False)
    action = models.CharField(max_length=200, blank=True, null=True)
    medication = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Medical Histories'
        unique_together = ('pet', 'date', 'veterinarian')

    def __str__(self):
        return self.pet.name + ' - ' + str(self.date)

class Device(models.Model):
    device_id = models.CharField(max_length=DEVICE_ID_LENGTH, primary_key=True)
    owner = models.ForeignKey(
        Customer, on_delete=models.CASCADE, blank=True, null=True)
    pet = ChainedForeignKey(
        Pet,
        chained_field="owner",
        chained_model_field="owner",
        show_all=False,
        auto_choose=False,
        sort=True, blank=True, null=True)
    
    @property
    def map_icon_url(self):
        if self.pet.image and hasattr(self.pet.image, 'url'):
            return self.pet.image.url
        else:
            return "/static/logo/app_icon.png"


class Vaccine(models.Model):
    name = models.CharField(
        max_length=80, primary_key=True, unique=True, blank=False)
    brand = models.CharField(max_length=80, blank=True)
    capacity = models.FloatField(validators=[MinValueValidator(0)], default=0)
    side_effects = models.CharField(max_length=80, blank=True)
    effect_duration = models.FloatField(
        validators=[MinValueValidator(0)], default=0)
    intake_type = models.CharField(max_length=80, blank=True)

    def __str__(self):
        return self.name

def validate_past_date(date):
    if date.date() < timezone.now().date():
        raise ValidationError("Date cannot be in the past")

class ImmunizationHistory(DirtyFieldsMixin, models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, null=False)
    pet_age = models.PositiveSmallIntegerField(default=1)
    vaccine = models.ForeignKey(Vaccine, blank=False, null=True, on_delete=models.SET_NULL)
    date = models.DateTimeField(default=timezone.now, validators=[validate_past_date])
    veterinarian = models.CharField(max_length=50, blank=False, default='Dr. Ong')
    dose = models.PositiveSmallIntegerField(default=1, validators=(MinValueValidator(1),), blank=False)
    owner_actions = models.CharField(default='None', max_length=500, blank=False)
    veterinary_actions = models.CharField(default='None', max_length=500, blank=False)
    attachment = models.ImageField(upload_to='records/', blank=True)

    class Meta:
        unique_together = ('pet', 'pet_age', 'vaccine', 'dose')
        verbose_name_plural = 'Immunization Histories'

    def __str__(self):
        return f'{self.pet}-{self.vaccine}'

    def save(self, *args, **kwargs):
        if self.is_dirty():
            try:
                if self.pet.owner is not None:
                    print('data was modified!')
                    
                    call_command('save_notification', self.pk)
                    # call_command(save_notification.Command(), pk=self.pk)
            except Exception as e:
                pass
        return super().save(*args, **kwargs)


    
class DeviceToken(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=False)
    token = models.CharField(max_length=500, blank=False, default='')

    class Meta:
        unique_together = ('customer', 'token')
    def __str__(self):
        return f'{self.customer.id} - {self.token}'


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(max_length=ID_LENGTH,
                          primary_key=True, default=id_gen, editable=False)
    email = models.EmailField(_("email address"), unique=True, blank=False)
    firstname = models.CharField(max_length=50, blank=True, null=True)
    # Field name made lowercase.
    middlename = models.CharField(max_length=50, blank=True, null=True)
    # Field name made lowercase.
    lastname = models.CharField(max_length=50, blank=True, null=True)
    picture = models.ImageField(
        upload_to='images/', blank=True, null=True, default='')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = "User"

    @property
    def get_photo_url(self):
        if self.picture and hasattr(self.picture, 'url'):
            return self.picture.url
        else:
            return "/static/logo/app_icon.png"

    def __str__(self):
        if self.firstname is None and self.lastname is None:
            return self.email
        return f'{self.firstname} {self.lastname}'

class Purpose(models.IntegerChoices):
    CHECK_UP = 1, "Check Up"
    GROOMING = 2, "Grooming"

class Payment(models.IntegerChoices):
    FULLY_PAID = 1, "Fully Paid"
    BALANCE = 2, "Balance"
    PROMISORY_NOTE = 3, "Prmisory Note"

class Appointment(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, blank=False)
    date = models.DateTimeField(default=timezone.now, blank=False)
    purpose = models.PositiveSmallIntegerField(choices=Payment.choices, default=Purpose.CHECK_UP)
    payment_method = models.PositiveSmallIntegerField(choices=Payment.choices, default=Payment.BALANCE)

    def __str__(self):
        return f'{self.id}-{self.pet}-{self.date}'