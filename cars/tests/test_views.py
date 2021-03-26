from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from cars.models import Car



class CarViewSetTestCase(APITestCase):

    cars_list_url = reverse('cars-list')
    car_pk_dict = {'pk': 1}
    cars_detail_url = reverse('cars-detail', kwargs=car_pk_dict)

    def setUp(self):
        Car.objects.create(make="Honda", model="Civic")
        Car.objects.create(make="Toyota", model="Corolla")

    def test_car_list_get(self):
        response = self.client.get(self.cars_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[-1]['make'], 'Toyota')
        self.assertEqual(response.data[-1]['model'], 'Corolla')
        self.assertEqual(response.data[-1]['avg_rating'], None)

    def test_car_list_post_title_method(self):
        response = self.client.post(self.cars_list_url, data={"make": "ford", "model": "focus"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(self.cars_list_url)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[-1]['make'], 'Ford')
        self.assertEqual(response.data[-1]['model'], 'Focus')
        self.assertEqual(response.data[-1]['avg_rating'], None)

    def test_car_list_post_car_doesnt_exist(self):
        response = self.client.post(self.cars_list_url, data={"make": "wartburg", "model": "nonexistentmodel"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_car_detail_delete(self):
        number_of_cars = Car.objects.all().count()
        response = self.client.delete(self.cars_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Car.objects.all().count(), number_of_cars-1)
        self.assertFalse(Car.objects.filter(**self.car_pk_dict).exists())

    def test_car_detail_delete_car_doesnt_exist(self):
        self.client.delete(self.cars_detail_url)
        response = self.client.delete(self.cars_detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_car_detail_get(self):
        response = self.client.get(self.cars_detail_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_car_detail_put(self):
        response = self.client.put(self.cars_detail_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class RateViewSetTestCase(APITestCase):
    rate_list_url = reverse('rate-list')

    def setUp(self):
        Car.objects.create(make="Honda", model="Civic")
        Car.objects.create(make="Toyota", model="Corolla")

    def test_rate_list_post(self):
        response = self.client.post(self.rate_list_url, data={"car_id": 1, "rating": 5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        car_rating = Car.objects.values('rating').get(id=1)['rating']
        self.assertEqual(car_rating[0], 5.0)

    def test_rate_list_post_nonexistent_car(self):
        response = self.client.post(self.rate_list_url, data={"car_id": 199, "rating": 5})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_rate_list_post_invalid_rating(self):
        response = self.client.post(self.rate_list_url, data={"car_id": 1, "rating": 6})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['rating'][0], "Your rating must be between 1 and 5")


class PopularViewSetTestCase(APITestCase):
    popular_list_url = reverse('popular-list')

    def setUp(self):
        Car.objects.create(make="Volkswagen", model="Golf", rating=[5, 3, 4, 3])
        Car.objects.create(make="Volkswagen", model="Passat", rating=[3, 5, 3, 2, 3])

    def test_popular_list_get(self):
        response = self.client.get(self.popular_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['make'], 'Volkswagen')
        self.assertEqual(response.data[0]['model'], 'Passat')
        self.assertEqual(response.data[0]['rates_number'], 5)