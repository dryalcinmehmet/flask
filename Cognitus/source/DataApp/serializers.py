from rest_framework import serializers
from DataApp.models import Data

class DataSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Data
        fields = ('text','label')





