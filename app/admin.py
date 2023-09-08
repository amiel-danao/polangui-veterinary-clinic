from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
# Register your models here.
from django.apps import apps
from app.forms import UserChangeForm, UserCreationForm
from django import forms
from app.models import (Appointment, Brand, Category, Breed, CustomUser, Customer, Device, DeviceToken, ImmunizationHistory, MedicalHistory, Pet, Vaccine, Product, ProductCategory, ProductMeta,
 Order, OrderItem, Transaction)
from django.contrib.auth.models import Group
from admin_interface.admin import Theme
# admin.site.unregister((Theme, Group))

# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     pass

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    readonly_fields = ('id', )
    list_display = ('email', 'firstname',
                    'middlename', 'lastname', 'mobile')
    search_fields = ('email', 'firstname', 'middlename', 'lastname')

    # def has_add_permission(self, request) -> bool:
    #     return False


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner', 'breed', 'species')
    # list_display = [field.name for field in Pet._meta.get_fields() if not field.name in [
    #     'id', 'medicalhistory', 'immunizationhistory', 'image', 'allergies', 'existing_conditions', 'device']]
    search_fields = ('owner__firstname', 'owner__middlename', 'owner__lastname', 'name')
    list_filter = ('species', 'breed', 'gender')
    # def has_add_permission(self, request, obj=None):
    #     return False


# @admin.register(Breed)
# class BreedAdmin(admin.ModelAdmin):
#     list_display = ['breed_name', 'species']


# @admin.register(Vaccine)
# class VaccineAdmin(admin.ModelAdmin):
#     list_display = ('name', 'brand', 'capacity', 'side_effects', 'effect_duration', 'intake_type')


# @admin.register(MedicalHistory)
# class MedicalHistoryAdmin(admin.ModelAdmin):
#     list_display = [
#         vaccine_field.name for vaccine_field in MedicalHistory._meta.get_fields()]
    
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = [
        appointment.name for appointment in Appointment._meta.get_fields()]
    
# @admin.register(Item)
# class ItemAdmin(admin.ModelAdmin):
#     list_display = [
#         item.name for item in Item._meta.get_fields()]
    
# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = [
#         product.name for product in Product._meta.get_fields()]


# @admin.register(Device)
# class DeviceAdmin(admin.ModelAdmin):
#     # form = DeviceForm
#     list_display = [
#         device_field.name for device_field in Device._meta.get_fields()]

# @admin.register(ImmunizationHistory)
# class ImmunizationHistoryAdmin(admin.ModelAdmin):
#     list_display = [
#         vaccination_field.name for vaccination_field in ImmunizationHistory._meta.get_fields() if not vaccination_field.name in [
#         'owner_actions', 'veterinary_actions', 'attachment']]
#     search_fields = ('pet__name', 'vaccine__name')
#     list_display_links = ('pet',)

#     def formfield_for_dbfield(self, db_field, **kwargs):
#         formfield = super(ImmunizationHistoryAdmin, self).formfield_for_dbfield(db_field, **kwargs)
#         text_area_fields = ('owner_actions', 'veterinary_actions')
#         if db_field.name in text_area_fields:
#             formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)
#         return formfield



# @admin.register(CustomUser)
# class CustomUserAdmin(BaseUserAdmin):
#     readonly_fields = ('last_login', 'date_joined')
#     form = UserChangeForm
#     add_form = UserCreationForm

#        # The fields to be used in displaying the User model.
#     # These override the definitions on the base UserAdmin
#     # that reference specific fields on auth.User.
#     list_display = ('email', 'firstname', 'lastname', 'is_superuser')
#     list_filter = ('is_superuser',)
#     fieldsets = (
#         (None, {'fields': ('email', 'picture')}),
#         ('Personal info', {'fields': ('firstname', 'middlename', 'lastname')}),
#         ('Permissions', {'fields': ('is_superuser', 'is_staff')}),
#     )
#     # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
#     # overrides get_fieldsets to use this attribute when creating a user.
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'firstname', 'middlename', 'lastname', 'picture', 'is_staff', 'is_superuser', 'password1', 'password2'),
#         }),
#     )
#     search_fields = ('email',)
#     ordering = ('email',)
#     filter_horizontal = ()

# @admin.register(DeviceToken)
# class DeviceTokenAdmin(admin.ModelAdmin):
#     pass

# Replace your_app_name it is just a placeholder
app_config = apps.get_app_config('app')
models = app_config.get_models()


for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass

admin.site.unregister((ProductCategory, Brand, MedicalHistory, Vaccine, Product, ImmunizationHistory, CustomUser, Theme, Device, DeviceToken, Group, Category, ProductMeta, Order, OrderItem, Transaction ))


admin.site.site_header = "Polangui Veterinary Clinic"
admin.site.site_title = "Polangui Veterinary Clinic"
admin.site.index_title = ""
