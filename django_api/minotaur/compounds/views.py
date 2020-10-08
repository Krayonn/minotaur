from django.shortcuts import render
from compounds.models import Compound
from compounds.serializer import CompoundSerializer
from compounds.serializer import AssaySerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json

class CompoundList(APIView):
    # Lists all Compounds
    def get(self, request, format=None):
        compounds = Compound.objects.all()
        serializer = CompoundSerializer(compounds, many=True)
        return Response(serializer.data)

class CompoundDetail(APIView):
    # retreives compound with given pk - private key
    def get(self, request, pk, format=None):
        try:
            compound = Compound.objects.get(pk=pk)
        except Compound.DoesNotExist:
            raise Http404
        serializer = CompoundSerializer(compound)
        return Response(serializer.data)

def load_data(request):

    compounds = list(Compound.objects.all())
    compound_serializer = CompoundSerializer(compounds, many=True)
    compounds_data = compound_serializer.data
    compounds_data_json = json.dumps(compounds_data, indent=4)
    print(compounds_data_json)

    if request.method == 'POST' and 'loadData' in request.POST:
        with open('compounds/fixtures/compounds_test.json') as data_file:
            json_data = json.loads(data_file.read())

            for compound_data in json_data:
                compound = Compound.create(**compound_data)


    return render(request, 'compounds/loadData.html', {'compounds':compounds_data_json})
