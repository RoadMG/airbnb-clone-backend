from django.utils import timezone
from rest_framework import serializers
from .models import Booking


class CreateExperienceBookingSerializer(serializers.ModelSerializer):

    experience_date = serializers.DateField()

    class Meta:
        model = Booking
        fields = (
            "experience_date",
            "guests",
        )

    def validate_experience_date(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Cant' book in the past!")
        return value

    def validate(self, data):
        if Booking.objects.filter(
            experience_date=data["experience_date"],
        ).exists():
            raise serializers.ValidationError(
                "Those (or some) of dates are already taken."
            )
        return data


class CreateRoomBookingSerializer(serializers.ModelSerializer):

    check_in = serializers.DateField()
    check_out = serializers.DateField()

    class Meta:
        model = Booking
        fields = (
            "check_in",
            "check_out",
            "guests",
        )

    def validate_check_in(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Can't book in the past!")

        return value

    def validate_check_out(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Can't book in the past!")

        return value

    def validate(self, data):
        room = self.context.get["room"]
        if data["check_out"] <= data["check_in"]:
            raise serializers.ValidationError(
                "Check in should be smaller than check out."
            )
        if Booking.objects.filter(
            room=room,
            check_in__lte=data["check_out"],
            check_out__gte=data["check_in"],
        ).exists():
            raise serializers.ValidationError(
                "Those (or some) of dates are already taken."
            )
        return data


class PublicRoomBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "pk",
            "check_in",
            "check_out",
            "guests",
        )


class PublicExperienceBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "pk",
            "experience_date",
            "guests",
        )


class ExperienceBookingDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"
