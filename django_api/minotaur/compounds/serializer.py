from rest_framework import serializers
from compounds.models import Compund

class: CompundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compound
        fields = '__all__' # returns all fields
