from django.shortcuts import render
from compounds.models import Compound
from compounds.models import Assay
from compounds.serializer import CompoundSerializer
from compounds.serializer import AssaySerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
import sqlite3

class CompoundList(APIView):
    # Lists all Compounds
    def get(self, request, format=None):
        compounds = Compound.objects.all()
        serializer = CompoundSerializer(compounds, many=True)
        return Response(serializer.data)

class CompoundDetail(APIView):
    # retreives compound with given pk - private key
    def get(self, request, c_pk, format=None):
        try:
            compound = Compound.objects.get(pk=c_pk)
        except Compound.DoesNotExist:
            raise Http404
        serializer = CompoundSerializer(compound)
        return Response(serializer.data)

class AssayList(APIView):
    # Lists all Compounds
    def get(self, request, c_pk, format=None):
        compounds = Compound.objects.all()
        serializer = CompoundSerializer(compounds, many=True)
        return Response(serializer.data)
    def get(self, request, c_pk, format=None):
        try:
            compound = Compound.objects.get(pk=c_pk)
        except Compound.DoesNotExist:
            raise Http404
        assays = compound.assay_results.all()
        serializer = AssaySerializer(assays, many=True)
        return Response(serializer.data)

class AssayDetail(APIView):
    # retreives compound with given pk - private key
    def get(self, request, c_pk, a_pk, format=None):
        try:
            compound = Compound.objects.get(pk=c_pk)
            assay = compound.assay_results.get(pk=a_pk)
        except Compound.DoesNotExist:
            raise Http404
        except Assay.DoesNotExist:
            raise Http404
        serializer = AssaySerializer(assay)
        return Response(serializer.data)

def load_data(request):

    if request.method == 'POST' and 'loadData' in request.POST:

        # FLush existing data from database

        conn = sqlite3.connect('db.sqlite3')
        c = conn.cursor()

        # delete all rows from table
        # would be better to drop table but then not sure how to recreate it
        # c.execute('DROP TABLE compounds_compound;',);

        c.execute('DELETE FROM compounds_compound;',);
        c.execute('DELETE FROM compounds_assay;',);

        print('We have deleted', c.rowcount, 'records from the table.')

        #commit the changes to db
        conn.commit()
        #close the connection
        conn.close()
        with open('compounds/fixtures/compounds.json') as data_file:
            json_data = json.loads(data_file.read())

            for compound_data in json_data:
                compound = Compound.create(**compound_data)

    compounds = list(Compound.objects.all())
    compound_serializer = CompoundSerializer(compounds, many=True)
    compounds_data = compound_serializer.data
    compounds_data_json = json.dumps(compounds_data, indent=4)
    # print(compounds_data_json)

    context = {'compounds':compounds_data_json}
    # context = {}
    # print(context)
    return render(request, 'compounds/loadData.html', context)
