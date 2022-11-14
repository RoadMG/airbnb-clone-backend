from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from medias.serializers import PhotoSerializer
from . import models
from users import serializers as UserSerializer
from categories import serializers as CategorySerializer
from wishlists import models as WishlistModels


class PerkSerializer(ModelSerializer):
    class Meta:
        model = models.Perk
        fields = (
            "name",
            "details",
            "explanation",
        )


class ExperiencesListSerializer(ModelSerializer):
    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    photo = PhotoSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = models.Experience
        fields = (
            "pk",
            "rating",
            "is_owner",
            "country",
            "city",
            "name",
            "price",
            "description",
            "photo",
        )

    def get_rating(self, experience):
        return experience.rating()

    def get_is_owner(self, experience):
        request = self.context["request"]
        return experience.host == request.user


class ExperienceDetailSerializer(ModelSerializer):
    host = UserSerializer.TinyUserSerializer(read_only=True)
    category = CategorySerializer.CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField()
    is_host = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    photos = PhotoSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = models.Experience
        fields = "__all__"

    def get_rating(self, experience):
        return experience.rating()

    def get_is_host(self, experience):
        request = self.context["request"]
        return experience.host == request.user

    def get_is_liked(self, experience):
        request = self.context["request"]
        return WishlistModels.Wishlist.objects.filter(
            user=request.user,
            experiences__pk=experience.pk,
        ).exists()
