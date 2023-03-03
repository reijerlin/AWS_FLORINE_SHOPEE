from rest_framework import serializers
from mainapp.models import ALLORDERS


class ALLORDERSSerializer(serializers.ModelSerializer):
    class Meta:
        model = ALLORDERS
        fields = '__all__'
        #fields = ('id', 'song', 'singer', 'last_modify_date', 'created')