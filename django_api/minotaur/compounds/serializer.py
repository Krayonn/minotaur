from rest_framework import serializers
from compounds.models import Compound, Assay

class AssaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Assay
        fields = '__all__' # returns all fields

class CompoundSerializer(serializers.ModelSerializer):
    assay_results = AssaySerializer(many=True)
    class Meta:
        model = Compound
        fields = ['compound_id','smiles', 'molecular_weight', 'a_log_p', 'num_rings', 'image', 'assay_results']
        # fields = '__all__' # returns all fields
