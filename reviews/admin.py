from django.contrib import admin
from reviews.models import Review


class WordFiler(admin.SimpleListFilter):
    title = "Filter by words!!"
    parameter_name = "word"

    def lookups(self, request, model_admin):
        return [
            ("good", "Good"),
            ("great", "Great"),
            ("awsome", "Awsome"),
        ]

    def queryset(self, request, reviews):
        word = self.value()
        if word:
            return reviews.filter(payload__contains=word)
        else:
            reviews


class ReviewIdentifier(admin.SimpleListFilter):
    title = "Good or Bad review"
    parameter_name = "rating"

    def lookups(self, request, model_admin):
        return [("good", "Good ones"), ("bad", "Bad ones")]

    def queryset(self, request, reviews):
        word = self.value()

        if word == "good":
            return reviews.filter(rating__gte=3)
        if word == "bad":
            return reviews.filter(rating__lte=2)
        else:
            return reviews


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "payload",
    )

    list_filter = (
        WordFiler,
        ReviewIdentifier,
        "rating",
        "user__is_host",
        "room__category",
        "room__pet_friendly",
    )
