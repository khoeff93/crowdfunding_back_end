from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from .models import Fundraiser, Pledge
from .serializers import FundraiserSerializer, PledgeSerializer

class FundraiserList(APIView):

    def get(self, request):
        fundraisers = Fundraiser.objects.all()
        serializer = FundraiserSerializer(fundraisers, many=True)
        return Response(serializer.data)
    
    def post(self, request):
# this function will get called to check the function is valid before saving it to our database.
        serializer = FundraiserSerializer(data=request.data)
# .data is passing through all the serialized data - this line deserializes/decodes the data
        if serializer.is_valid():
# is_valid is a built in function - it checks if the data is valid then save to database.
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTPP_400_BAD_REQUEST
        )

class FundraiserDetail(APIView):
# Fundraiser detail, I want the option to show more detailed information.
    def get(self, request, pk):
        fundraiser = get_object_or_404(Fundraiser, pk=pk)
        # pk = primary key
        serializer = FundraiserSerializer(fundraiser)
        return Response(serializer.data)

class PledgeList(APIView):

    def get(self, request):
        pledges = Pledge.objects.all()
        serializer = PledgeSerializer(pledges, many=True)
        return Response(serializer.data)
    
    def post(self, request):

        serializer = PledgeSerializer(data=request.data)
        if serializer.is_valid():
           serializer.save()
           return Response(
               serializer.data,
               status=status.HTTP_201_CREATED
           )
        return Response(
           serializer.errors,
           status=status.HTTP_400_BAD_REQUEST
       )