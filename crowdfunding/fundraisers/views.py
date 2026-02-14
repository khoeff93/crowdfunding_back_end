from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework import status
from rest_framework import status, permissions
from rest_framework.generics import get_object_or_404
from .models import Fundraiser, Pledge
# from .serializers import FundraiserSerializer, PledgeSerializer
from .serializers import FundraiserSerializer, PledgeSerializer, FundraiserDetailSerializer
from .permissions import IsOwnerOrReadOnly

class FundraiserList(APIView):
    
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]

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
            serializer.save(owner=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTPP_400_BAD_REQUEST
        )

class FundraiserDetail(APIView):

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]

# Fundraiser detail, I want the option to show more detailed information.
    def get(self, request, pk):
        fundraiser = get_object_or_404(Fundraiser, pk=pk)
        # pk = primary key
        # serializer = FundraiserSerializer(fundraiser)
        self.check_object_permissions(request,fundraiser)
        serializer = FundraiserDetailSerializer(fundraiser)
        return Response(serializer.data)

    def put(self, request,pk):
        fundraiser = get_object_or_404(Fundraiser,pk=pk)
        serializer = FundraiserDetailSerializer(
            instance=fundraiser,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        """Delete a fundraiser"""
        fundraiser = get_object_or_404(Fundraiser, pk=pk)

         # Check object-level permissions
        self.check_object_permissions(request, fundraiser)

        fundraiser.delete()
        # 204 means success with no content to return
        return Response({'message': 'Delete successful'}, status=status.HTTP_204_NO_CONTENT)

class PledgeList(APIView):

    def get(self, request):
        pledges = Pledge.objects.all()
        serializer = PledgeSerializer(pledges, many=True)
        return Response(serializer.data)
    
    def post(self, request):

        serializer = PledgeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(supporter=request.user)
            return Response(
               serializer.data,
               status=status.HTTP_201_CREATED
           )
        return Response(
           serializer.errors,
           status=status.HTTP_400_BAD_REQUEST
       )