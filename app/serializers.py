from rest_framework import serializers

from .models import DeviceToken, Breed, Customer, Device, ImmunizationHistory, MedicalHistory, Pet, CustomUser


class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = '__all__'


class DeviceSerializer(serializers.ModelSerializer):
    map_icon_url = serializers.CharField()
    class Meta:
        model = Device
        fields = ('device_id', 'owner', 'pet', 'map_icon_url')
        read_only_fields = ('map_icon_url',)


class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ('id', 'date_of_birth', 'name', 'gender', 'weight',
                  'height', 'species', 'breed', 'allergies', 'existing_conditions')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for key, value in data.items():
            try:
                if not value:
                    data[key] = ""
            except KeyError:
                pass
        return data


class PetImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ('id', 'image')


class CustomerImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'picture')


class MedicalHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalHistory
        fields = '__all__'

class DeviceTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceToken
        fields = '__all__'


class ImmunizationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ImmunizationHistory
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'email', 'firstname',
                  'middlename', 'lastname', 'mobile', 'picture')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for key, value in data.items():
            try:
                if not value:
                    data[key] = ""
            except KeyError:
                pass
        return data


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'picture',
                  'firstname', 'middlename', 'lastname')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for key, value in data.items():
            try:
                if not value:
                    data[key] = ""
            except KeyError:
                pass
        return data
