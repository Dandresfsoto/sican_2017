from rest_framework import serializers
from usuarios.models import User
from matrices.models import Beneficiario
from inbox.models import Mensaje

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','fullname','email','get_photo')

class MensajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','user','created','leido','de','para','texto','adjuntos')


class BeneficiarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beneficiario
        fields = ('nombres','apellidos','diplomado_name','get_diploma_url_rest')