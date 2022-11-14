from django.db import transaction

from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from . import models, serializers
from categories import models as CategoryModels


class Perks(APIView):
    def get(self, request):
        all_perks = models.Perk.objects.all()
        serializer = serializers.PerkSerializer(all_perks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.PerkSerializer(data=request.data)
        if serializer.is_valid():
            perk = serializer.save()
            return Response(serializers.PerkSerializer(perk).data)
        else:
            return Response(serializer.errors)


class PerkDetail(APIView):
    def get_object(self, perks_pk):
        try:
            return models.Perk.objects.get(pk=perks_pk)
        except models.Perk.DoesNotExist:
            raise NotFound

    def get(self, request, perks_pk):
        perk = self.get_object(perks_pk)
        serializer = serializers.PerkSerializer(perk)
        return Response(serializer.data)

    def put(self, request, perks_pk):
        perk = self.get_object(perks_pk)
        serializer = serializers.PerkSerializer(
            perk,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_perk = serializer.save()
            return Response(serializers.PerkSerializer(updated_perk).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, perks_pk):
        perk = self.get_object(perks_pk)
        perk.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Experiecnes(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        experience = models.Experience.objects.all()
        serializer = serializers.ExperiencesListSerializer(
            experience,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.ExperienceDetailSerializer(data=request.data)

        if serializer.is_valid():
            category_pk = request.data.get("category")

            if not category_pk:
                raise ParseError("Category is required.")
            try:
                category = CategoryModels.Category.objects.get(pk=category_pk)
                if category.kind == CategoryModels.Category.CategoryKindChoices.ROOMS:
                    raise ParseError("The category kind should be experience.")
            except CategoryModels.Category.DoesNotExist:
                raise ParseError("Category not found.")

            experience = serializer.save(
                host=request.user,
                category=category,
            )
            serializer = serializers.ExperienceDetailSerializer(
                experience, context={"request": request}
            )
            return Response(serializer.data)

        else:
            return Response(serializer.errors)


class ExperiencesDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return models.Experience.objects.get(pk=pk)
        except models.Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        experience = self.get_object(pk)
        serializer = serializers.ExperienceDetailSerializer(
            experience,
            context={"request": request},
        )
        return Response(serializer.data)

    def put(self, request, pk):
        experience = self.get_object(pk)

        if experience.host != request.user:
            raise PermissionDenied

        serializer = serializers.ExperienceDetailSerializer(
            experience,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            category_pk = request.data.get("category")
            if category_pk:
                try:
                    category = CategoryModels.Category.objects.get(pk=category_pk)
                    if (
                        category.kind
                        == CategoryModels.Category.CategoryKindChoices.ROOMS
                    ):
                        raise ParseError("The category kind should be experiences")
                except CategoryModels.Category.DoesNotExist:
                    raise ParseError("Cateogry does not found")
            else:
                category = None

            updated_experiecnes = serializer.save(
                category=category,
                partial=True,
            )
            serializer = serializers.ExperienceDetailSerializer(
                updated_experiecnes,
                context={"request": request},
            )
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        pass
