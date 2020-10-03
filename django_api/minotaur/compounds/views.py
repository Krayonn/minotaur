from django.shortcuts import render
from compunds.models import Compound
from compunds.serializers import CompoundSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class CompoundList(APIView):
    # Lists all Compounds
    def get(self, request, format=None):
        compounds = Compound.objects.all()
        serializer = CompundSerializer(compounds, many=True)
        return Response(serializer.data)

class CompoundDetail(APIView):
    # retreives compound with given pk - private key
    def get(self, request, pk, format=None):
        try:
            compound = Compound.objects.get(pk=pk)
        except Compound.DoesNotExist:
            raise Http404
        serializer = CompundSerializer(compound)
        return Response(serializer.data)
