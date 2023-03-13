from django.utils.translation import gettext_lazy as _
from django.urls import reverse
import django_tables2 as tables
from .models import Appointment, Purpose


class AppointmentTable(tables.Table):

    class Meta:
        orderable = False
        model = Appointment
        template_name = "django_tables2/bootstrap.html"
        fields = ("pet", "date", "purpose" )
        attrs = {'class': 'table table-hover shadow records-table'}
        # row_attrs = {
        #     "onClick": lambda record: f"document.location.href='{reverse('system:order-detail', kwargs={'pk': record.pk})}';"
        # }

    def render_purpose(self, value, record):
        return Purpose(record.purpose).label
    
    def render_pet(self, value, record):
        return record.pet.name