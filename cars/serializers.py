from rest_framework import serializers
from .models import Car
from .utils import check_if_car_exists


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ('id', 'make', 'model', 'avg_rating')

    def validate(self, posted_car_data):
        verified_car_data = check_if_car_exists(posted_car_data)
        if verified_car_data:
            return verified_car_data
        raise serializers.ValidationError("Car of this make and model doesn't exist in the nhtsa database")


class RatingSerializer(serializers.ModelSerializer):
    car_id = serializers.IntegerField(source='id')

    class Meta:
        model = Car
        fields = ('car_id', 'rating')

    def validate_rating(self, rating):
        if not isinstance(rating, (int, float)):
            raise serializers.ValidationError("Your rating must be a number")
        if rating > 5 or rating < 1:
            raise serializers.ValidationError("Your rating must be between 1 and 5")
        return rating

    def update(self, instance, validated_data):
        rating = validated_data['rating']
        if instance.rating:
            instance.rating.append(float(rating))
        else:
            instance.rating = [float(rating)]
        instance.save()
        return instance


class PopularSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ('id', 'make', 'model', 'rates_number')
