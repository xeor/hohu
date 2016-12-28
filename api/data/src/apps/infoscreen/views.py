from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework.response import Response


from . import serializers, models


class Infoscreen(APIView):
    def get(self, request, format=None):
        return_dict = {
            'view': reverse('inforscreen:view-list', request=request, format=format)
        }

        return Response(return_dict)


class ViewList(generics.ListCreateAPIView):
    serializer_class = serializers.ViewListSerializer
    queryset = models.View.objects.all()


class ViewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.View.objects.all()
    serializer_class = serializers.ViewDetailSerializer
