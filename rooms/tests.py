from rest_framework.test import APITestCase
from . import models
from users import models as UserModel


class TestAmenities(APITestCase):
    NAME = "Amenity Test"
    DESC = "Amenity Des"

    URL = "/api/v1/rooms/amenities/"

    def setUp(self):
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESC,
        )

    # def 이름 설정 시 앞에 "test_"를 안붙여주면 django는 test로 인식을 안함

    def test_all_amenities(self):
        # data를 데이터 베이스에 있는 것을 사용하지 않고 새로 만들어서 쓰기 때문에 빈 array를 출력함
        response = self.client.get(self.URL)
        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            "Status code isn't 200.",
        )

        self.assertIsInstance(
            data,
            list,
        )
        self.assertEqual(
            len(data),
            1,
        )
        self.assertEqual(
            data[0]["name"],
            self.NAME,
        )
        self.assertEqual(
            data[0]["description"],
            self.DESC,
        )

    def test_create_amenities(self):

        new_amenity_name = "New Amenity"
        new_amenity_description = "New Amenity desc"

        response = self.client.post(
            self.URL,
            data={
                "name": new_amenity_name,
                "description": new_amenity_description,
            },
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            "Not 200 status code",
        )

        self.assertEqual(
            data["name"],
            new_amenity_name,
        )
        self.assertEqual(
            data["description"],
            new_amenity_description,
        )

        response = self.client.post(self.URL)

        self.assertEqual(response.status_code, 400)
        self.assertIn("name", data)


class TestAmenity(APITestCase):
    NAME = "Test Amenity"
    DESC = "Test Amenity description"

    def setUp(self):
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESC,
        )

    def test_amenity_not_fount(self):
        response = self.client.get("/api/v1/rooms/amenities/1")

        self.assertEqual(response.status_code, 200)

    def test_get_amenity(self):

        response = self.client.get("/api/v1/rooms/amenities/1")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(
            data["name"],
            self.NAME,
        )
        self.assertEqual(
            data["description"],
            self.DESC,
        )

    def test_put_amenity(self):
        # code challenge
        put_amenity_name = "The name of put amenity"
        put_amenity_desc = "The desc of put amenity"
        response = self.client.put(
            "/api/v1/rooms/amenities/1",
            data={
                "name": put_amenity_name,
                "description": put_amenity_desc,
            },
        )
        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            "Not 200 status code",
        )
        self.assertEqual(
            data["name"],
            put_amenity_name,
        )
        self.assertEqual(
            data["description"],
            put_amenity_desc,
        )

        response = self.client.put("/api/v1/rooms/amenities/1")
        data = response.json()
        self.assertIn("name", data)

    def test_delete_amenity(self):
        response = self.client.delete("/api/v1/rooms/amenities/1")

        self.assertEqual(response.status_code, 204)


class TestRoom(APITestCase):
    def setUp(self):
        user = UserModel.User.objects.create(
            username="test",
        )

        user.set_password("123")
        user.save()
        self.user = user

    def test_create_room(self):
        response = self.client.post("/api/v1/rooms/")

        self.assertEqual(response.status_code, 403)

        self.client.force_login(
            self.user,
        )
