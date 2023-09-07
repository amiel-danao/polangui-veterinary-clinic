from django.db.models import Q
from django.utils.timezone import get_current_timezone
from datetime import datetime
from django.utils.timezone import make_aware
from app.context_processors import SCHEDULE_DATEFORMAT
from django_tables2 import SingleTableView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.shortcuts import render, redirect
from app.context_processors import CONTEXT
from app.forms import AppointmentForm, MedicalHistoryForm, NewUserForm, PetForm
from app.models import SPECIES_CHOICES, Appointment, DeviceToken, Breed, CustomUser, Customer, Device, ImmunizationHistory, MedicalHistory, Pet
from app.tables import AppointmentTable
from .serializers import BreedSerializer, CustomUserSerializer, CustomerImageSerializer, CustomerSerializer, DeviceSerializer, DeviceTokenSerializer, ImmunizationHistorySerializer, MedicalHistorySerializer, PetImageSerializer, PetSerializer
from rest_framework import viewsets, mixins, generics
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.exceptions import ParseError
from django.shortcuts import get_object_or_404
from rest_framework import status
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import resolve, reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import LoginView
import math
import time
import os
from agora_token_builder import RtcTokenBuilder
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, UpdateView
from rest_framework.generics import UpdateAPIView


dirname = os.path.dirname(__file__)
filename = "clinic-firebase-adminsdk-f45f4-e1db7a11eb.json"
filepath = os.path.join(
    dirname, f'../{filename}')

if not firebase_admin._apps:
    cred = credentials.Certificate(filepath)
    firebase_admin.initialize_app(cred)

database = firestore.client()

query_watch = None


@api_view(['GET', ])
def get_breeds(request):
    if request.method == 'GET':
        breeds = Breed.objects.all()
        species = request.query_params.get('species', None)
        if species is not None:
            breeds = breeds.filter(species=species)

        breeds_serializer = BreedSerializer(breeds, many=True)
        return JsonResponse(breeds_serializer.data, safe=False)


@api_view(['POST', ])
def pet_update(request):
    if request.method == 'POST':
        pet_data = JSONParser().parse(request)
        pet_serializer = PetSerializer(data=pet_data)
        if pet_serializer.is_valid():
            pet_serializer.save()
            return JsonResponse(pet_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(pet_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_my_pets(owner):
    pets = []
    if owner is not None:
        pets = Pet.objects.filter(owner=owner)
    return pets


@api_view(['GET', ])
def pet_list(request):
    if request.method == 'GET':
        owner = request.query_params.get('owner', None)
        pets = get_my_pets(owner=owner)

        pets_serializer = PetSerializer(pets, many=True)
        return JsonResponse(pets_serializer.data, safe=False)
        # 'safe=False' for objects serialization


@api_view(['GET', ])
def customer_list(request):
    if request.method == 'GET':
        customers = Customer.objects.all()

        customers_serializer = CustomerSerializer(customers, many=True)
        return JsonResponse(customers_serializer.data, safe=False)


class PetViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer


# class DeviceViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
#     queryset = Device.objects.all()
#     serializer_class = DeviceSerializer


class DeviceList(generics.ListAPIView):
    serializer_class = DeviceSerializer

    def get_queryset(self):
        owner_id = self.request.query_params.get('owner')
        result = Device.objects.all()
        if owner_id is not None:
            result = Device.objects.filter(owner__id=owner_id)

        pet_id = self.request.query_params.get('pet')
        if pet_id is not None:
            result = result.filter(pet__id=pet_id)

        return result

class DeviceTokenViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = DeviceToken.objects.all()
    serializer_class = DeviceTokenSerializer


class CustomerViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class UploadPetImageViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    queryset = Pet.objects.all()
    serializer_class = PetImageSerializer
    parser_classes = [MultiPartParser]


class UploadCustomerImageViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    queryset = Customer.objects.all()
    serializer_class = CustomerImageSerializer
    parser_classes = [MultiPartParser]





@api_view(['GET', ])
def get_medical_by_pet(request):
    if request.method == 'GET':
        medical_history = MedicalHistory.objects.all()
        petId = request.query_params.get('pet', None)
        if petId is not None:
            medical_history = medical_history.filter(pet__id=petId)

        medical_history_serializer = MedicalHistorySerializer(
            medical_history, many=True)
        return JsonResponse(medical_history_serializer.data, safe=False)


@api_view(['GET', ])
def get_immunization_by_pet(request):
    if request.method == 'GET':
        immunization_history = ImmunizationHistory.objects.all()
        petId = request.query_params.get('pet', None)
        if petId is not None:
            immunization_history = immunization_history.filter(pet__id=petId)

        immunization_history_serializer = ImmunizationHistorySerializer(
            immunization_history, many=True)
        return JsonResponse(immunization_history_serializer.data, safe=False)


@api_view(['PUT'])
def medical_detail(request, pk):
    try:
        medical_history = MedicalHistory.objects.get(pk=pk)
    except MedicalHistory.DoesNotExist:
        return JsonResponse({'message': 'The medical_history does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        medical_history_data = JSONParser().parse(request)
        medical_history_serializer = MedicalHistorySerializer(
            medical_history, data=medical_history_data)
        if medical_history_serializer.is_valid():
            medical_history_serializer.save()
            return JsonResponse(medical_history_serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(medical_history_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # elif request.method == 'DELETE':
    #     medical_history.delete()
    #     return JsonResponse({'message': 'MedicalHistory was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


def chat_all(request):
    if request.user is None or request.user.is_authenticated is False:
        return redirect('admin:index')

    template = loader.get_template('pages/chat.html')
    all_custmomers = Customer.objects.filter(~Q(email=request.user.email))
    receiver = None
    message_gc_id = None
    try:
        receiver = Customer.objects.first()
        message_gc_id = f'{request.user.id}-{receiver.id}'
    except Exception:
        pass

    pets = get_my_pets(receiver)

    context = {
        "pets": pets,
        "receiver": receiver,
        "contacts": all_custmomers,
        "message_gc_id": message_gc_id
    }

    if request.method == 'POST':
        send_message(request=request, receiver_id=receiver)

    return HttpResponse(template.render(context, request))


class AppointmentListView(LoginRequiredMixin, SingleTableView):
    model = Appointment
    table_class = AppointmentTable
    template_name = 'pages/appointment.html'
    per_page = 8

    def post(self, request, *args, **kwargs):
        
        pet = Pet.objects.filter(id=request.POST.get('pet')).first()
        # owner = Customer.objects.filter(email=request.user.email).first()
        date = make_aware(datetime.strptime(
                    request.POST.get('date'), SCHEDULE_DATEFORMAT), timezone=get_current_timezone())
        Appointment.objects.create(pet=pet, date=date, purpose=request.POST.get('purpose'))
        return self.get(request, *args, **kwargs)

    # def post(self, request, *args, **kwargs):
    #     self.object_list = self.get_queryset()
    #     context = self.get_context_data()
    #     owner = Customer.objects.filter(email=request.email).first()
    #     Appointment.objects.create(pet=request.POST.get('pet'), owner=owner, purpose=request.POST.get('purpose'))
    #     return self.render_to_response(context)

    def get_table_data(self):

        return Appointment.objects.filter(pet__owner__email=self.request.user.email)
    
    def get_context_data(self, **kwargs):
        context = super(AppointmentListView, self).get_context_data(**kwargs)
        
        context['form'] = AppointmentForm(owner=self.request.user)
            
        return context

def chat(request, message_gc_id):
    if request.user is None or request.user.is_authenticated is False:
        return redirect('admin:index')

    template = loader.get_template('pages/chat.html')
    all_customers = Customer.objects.filter(~Q(email=request.user.email))
    receiver = None
    receiver_id = ''

    try:
        receiver_id = message_gc_id.split('-')[1]
        receiver = Customer.objects.filter(id=receiver_id).first()
    except Exception:
        pass

    pets = get_my_pets(receiver)

    context = {
        "pets": pets,
        "receiver": receiver,
        "contacts": all_customers,
        "message_gc_id": message_gc_id
    }

    if request.method == 'POST':
        send_message(request=request, receiver_id=receiver_id)

    return HttpResponse(template.render(context, request))


def send_message(request, receiver_id):
    input_message = None
    if request is None or request.user is None or receiver_id is None:
        return
    message_gc_id = f'{request.user.id}-{receiver_id}'
    try:
        input_message = request.POST.get('input_message')

        if input_message is not None:
            current_milliseconds = str(math.trunc(time.time() * 1000))
            new_message = {
                u'content': input_message,
                u'timestamp': current_milliseconds,
                u'idFrom': request.user.id,
                u'idTo': receiver_id,
                u'type': 0
            }

            batch = database.batch()

            message_thread_reference = database.collection(
                u'messages').document(message_gc_id)
            batch.set(message_thread_reference, {
                u'timestamp': firestore.SERVER_TIMESTAMP}, merge=True)

            message_reference = database.collection(u'messages').document(message_gc_id).collection(
                message_gc_id).document(current_milliseconds)

            batch.set(message_reference, new_message, merge=True)

            batch.commit()
    except Exception as exception:
        print(exception)


@api_view(['GET', ])
def veterinary_list(request):
    if request.method == 'GET':
        veterinaries = CustomUser.objects.all()

        veterinaries_serializer = CustomUserSerializer(veterinaries, many=True)
        return JsonResponse(veterinaries_serializer.data, safe=False)


def video_call(request, message_gc_id):
    if request.user is None or request.user.is_authenticated is False:
        return redirect('admin:index')

    template = loader.get_template('pages/video_call.html')
    
    receiver_id = ''
    receiver = "Other"
    try:
        receiver_id = message_gc_id.split('-')[1]
        receiver = Customer.objects.filter(id=receiver_id).first()
    except Exception:
        pass
    #Build token with account
    expiration_time_in_seconds = 3600
    currentTimestamp = time.time()
    privilege_expired_ts = currentTimestamp + expiration_time_in_seconds;
    token = RtcTokenBuilder.buildTokenWithAccount(CONTEXT['app_id'], CONTEXT['app_certificate'], message_gc_id, request.user.id, 1, privilege_expired_ts)

    context = {
        'message_gc_id': message_gc_id,
        'receiver': receiver
        # 'token': token
    }

    return HttpResponse(template.render(context, request))


class MyLoginView(LoginView):
    # form_class=LoginForm
    redirect_authenticated_user=True
    template_name='registration/login.html'

    def get_success_url(self):
        # write your logic here
        # if self.request.user.is_superuser:
        return reverse('index')# '/progress/'
        # return '/'


def register_request(request):
    context = {}
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            Customer.objects.create(email=user.email)
            login(request, user)
            return redirect("index")
        context['form_errors'] = form.errors
        messages.error(
            request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    context["register_form"] = form
    return render(request=request, template_name="registration/register.html", context=context)


def index(request):
    if request.user is None or request.user.is_authenticated is False:
        return redirect('/accounts/login')
    context = {}
    return render(request, 'pages/chat.html', context)

@login_required
def user_pets(request):
    user = request.user
    customer = Customer.objects.filter(email=user.email).first()
    if(customer is None):
        return render(request, 'pages/pet.html', {})

    owned_pets = Pet.objects.filter(owner_id=customer.id)
    search_query = request.GET.get('q', '')

    if search_query:
        owned_pets = owned_pets.filter(name__icontains=search_query)
    
    pet_list = []
    for pet in owned_pets:
        pet_info = {
            'name': pet.name,
            'date_of_birth': pet.date_of_birth,
            'gender': pet.gender,
            'weight': pet.weight,
            'height': pet.height,
            'species': pet.species,
            'allergies': pet.allergies,
            'existing_conditions': pet.existing_conditions,
            'image': pet.image.url if pet.image else None,
            'breed_id': pet.breed_id,
        }
        pet_list.append(pet_info)

        medical_histories = MedicalHistory.objects.filter(pet=pet)
        medical_history_list = []
        for history in medical_histories:
            history_info = {
                'id': history.id,
                'date': history.date,
                'description': history.description,
                'veterinarian': history.veterinarian,
                'diagnosis': history.diagnosis,
                'tests_performed': history.tests_performed,
                'test_results': history.test_results,
                'action': history.action,
                'medication': history.medication,
            }
            medical_history_list.append(history_info)
        
        pet_info['medical_histories'] = medical_history_list
    
    context = {
        'pet_list': pet_list,
        'q': search_query
    }
    
    return render(request, 'pages/pet.html', context)

@login_required
def pet_list(request):
    user = request.user
    if (user.is_superuser != 1):
        return HttpResponse('Unauthorized', status=401)

    search_query = request.GET.get('q', '')
    owned_pets = Pet.objects.all()

    if search_query:
        owned_pets = owned_pets.filter(name__icontains=search_query)
    
    pet_list = []
    for pet in owned_pets:
        pet_info = {
            'id': pet.id,
            'name': pet.name,
            'date_of_birth': pet.date_of_birth,
            'gender': pet.gender,
            'weight': pet.weight,
            'height': pet.height,
            'species': pet.species,
            'allergies': pet.allergies,
            'existing_conditions': pet.existing_conditions,
            'image': pet.image.url if pet.image else None,
            'breed_id': pet.breed_id,
            'url': reverse('update_pet', kwargs={'pk': str(pet.id)}),#reverse('api:pet-detail', kwargs={'pk': str(pet.id)})
            # 'medical_url': reverse('add_medical_history', kwargs={'pk': str(pet.id)})
        }
        pet_list.append(pet_info)

        medical_histories = MedicalHistory.objects.filter(pet=pet)
        medical_history_list = []
        for history in medical_histories:
            history_info = {
                'id': history.id,
                'date': history.date,
                'description': history.description,
                'veterinarian': history.veterinarian,
                'diagnosis': history.diagnosis,
                'tests_performed': history.tests_performed,
                'test_results': history.test_results,
                'action': history.action,
                'medication': history.medication,                
            }
            medical_history_list.append(history_info)
        
        pet_info['medical_histories'] = medical_history_list
    
    species_data = SPECIES_CHOICES
    cat_breeds = Breed.objects.filter(species='Cat')
    dog_breeds = Breed.objects.filter(species='Dog')
    medical_form = MedicalHistoryForm()

    context = {
        'pet_list': pet_list,
        'species_data': species_data,
        'cat_breeds': cat_breeds,
        'dog_breeds': dog_breeds,
        'medical_form': medical_form,
        'q': search_query
    }
    
    return render(request, 'pages/pet_admin.html', context)

class UpdatePetView(UpdateView):
    model = Pet
    form_class = PetForm
    # template_name = 'post_form.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        # Assuming your Post model has an 'id' field, include it in the response
        data = {
            'id': self.object.id,
            'title': self.object.title,
            'content': self.object.content,
        }
        return JsonResponse(data)
    
class PetUpdateView(UpdateAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    lookup_field = 'pk'  # Specify the lookup field (in this case, primary key)

@api_view(['POST'])
def add_medical_history(request):
    
    
    if request.method == 'POST':
        form = MedicalHistoryForm(request.data)
        

        if form.is_valid():
            # try:
            #     pet = Pet.objects.get(pk=pk)
            # except Pet.DoesNotExist:
            #     return JsonResponse({'message': 'The pet does not exist'}, status=status.HTTP_404_NOT_FOUND)
            # Create a new MedicalHistory instance and associate it with the pet
            medical_history = form.save(commit=False)
            medical_history.save()
            
            return HttpResponseRedirect(reverse('pets_admin'))
        else:
            return JsonResponse(form.errors, status=status.HTTP_400_BAD_REQUEST)

    return JsonResponse({'message': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
@api_view(['DELETE'])
@login_required
def delete_medical_history(request, pk):
    try:
        medical = MedicalHistory.objects.get(pk=pk)
    except MedicalHistory.DoesNotExist:
        return JsonResponse({'message': 'The medical does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    medical.delete()
    return JsonResponse({'message': 'Medical History was deleted successfully'}, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'DELETE', 'PATCH'])
@login_required
def pet_detail(request, pk):
    try:
        pet = Pet.objects.get(pk=pk)
    except Pet.DoesNotExist:
        return JsonResponse({'message': 'The pet does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        pet_serializer = PetSerializer(pet)
        return JsonResponse(pet_serializer.data)

    elif request.method == 'PUT':
        pet_data = request.data#JSONParser().parse(request.data)
        pet_serializer = PetSerializer(pet, data=pet_data)
        if pet_serializer.is_valid():
            pet_serializer.save()
            return JsonResponse(pet_serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(pet_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        pet_data = request.data#JSONParser().parse(request.data)
        pet_serializer = PetSerializer(pet, data=pet_data)
        if pet_serializer.is_valid():
            pet_serializer.save()
            return JsonResponse(pet_serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(pet_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        pet.delete()
        return JsonResponse({'message': 'Pet was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)