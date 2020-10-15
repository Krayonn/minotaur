from django.shortcuts import render
from compounds.models import Compound
from compounds.models import Assay
from compounds.serializer import CompoundSerializer
from compounds.serializer import AssaySerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, filters, generics
from django_filters.rest_framework import DjangoFilterBackend
import json
import sqlite3

class CompoundList(generics.ListAPIView):
    # Lists all Compounds
    queryset = Compound.objects.all()
    serializer_class = CompoundSerializer
    # Add filtering via query params
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['compound_id', 'num_rings']

class CompoundDetail(generics.RetrieveAPIView):
    # retreives compound with given pk - private key
    queryset = Compound.objects.all()
    serializer_class = CompoundSerializer
    # Filters based on compound_id given in url paths
    lookup_field = 'compound_id'

class AssayList(generics.ListAPIView):
    # retreives assays for compound with given id
    def get(self, request, compound_id, format=None):
        assays = self.get_queryset()
        serializer = AssaySerializer(assays, many=True)
        return Response(serializer.data)

    #rewriting get_queryset function to include filtering
    def get_queryset(self):
        # get compound id from path parameters
        compound_id = self.kwargs['compound_id']
        try:
            compound = Compound.objects.get(pk=compound_id)
            assays = compound.assay_results.all()
        except Compound.DoesNotExist:
            raise Http404
        except Assay.DoesNotExist:
            raise Http404

        queryset = assays

        # Filter target
        target = self.request.query_params.get('target', None)
        if target is not None:
            queryset = queryset.filter(target=target)

        # Filter result type
        result = self.request.query_params.get('result', None)
        if result is not None:
            queryset = queryset.filter(result=result)
        return queryset

class AssayDetail(APIView):
    # retreives compound with given pk - private key
    # Could have done with RetrieveAPIView but this checks existance of both compound and assay
    def get(self, request, compound_id, result_id, format=None):
        try:
            compound = Compound.objects.get(pk=compound_id)
            assay = compound.assay_results.get(pk=result_id)
        except Compound.DoesNotExist:
            raise Http404
        except Assay.DoesNotExist:
            raise Http404
        serializer = AssaySerializer(assay)
        return Response(serializer.data)


def load_data(request):
    context = {}
    if request.method == 'POST' and 'loadData' in request.POST:

        # Flush existing data from database
        conn = sqlite3.connect('db.sqlite3')
        c = conn.cursor()

        # delete all rows from table
        c.execute('DELETE FROM compounds_compound;',);
        c.execute('DELETE FROM compounds_assay;',);

        print('We have deleted', c.rowcount, 'records from the table.')

        #commit the changes to db
        conn.commit()
        #close the connection
        conn.close()
        # load in data from json file
        with open('compounds/fixtures/compounds.json') as data_file:
            json_data = json.loads(data_file.read())

            for compound_data in json_data:
                compound = Compound.create(**compound_data)

        context = {'data_loaded':'Data has been loaded in successfully'}
    compounds = list(Compound.objects.all())
    compound_serializer = CompoundSerializer(compounds, many=True)
    compounds_data = compound_serializer.data
    compounds_data_json = json.dumps(compounds_data, indent=4)
    # print(compounds_data_json)

    return render(request, 'compounds/loadData.html', context)
