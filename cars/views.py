from django.db.models.functions import Length

from rest_framework.response import Response
from rest_framework import status, viewsets, mixins

from .models import Car
from .serializers import CarSerializer, RatingSerializer, PopularSerializer


class CarViewSet(viewsets.GenericViewSet,
                 mixins.CreateModelMixin,
                 mixins.ListModelMixin,
                 mixins.DestroyModelMixin):
    serializer_class = CarSerializer
    queryset = Car.objects.all()


class RatingViewSet(viewsets.GenericViewSet,
                    mixins.CreateModelMixin):
    serializer_class = RatingSerializer

    def create(self, request, *args, **kwargs):
        try:
            car = Car.objects.get(id=request.data['car_id'])
            serializer = RatingSerializer(car, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Car.DoesNotExist:
            return Response({"detail": "No car with this id exists in the database."},
                            status=status.HTTP_400_BAD_REQUEST)


class PopularViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin):
    serializer_class = PopularSerializer
    queryset = Car.objects.all().order_by(Length('rating').desc())
