import django_filters

from .models import CapstoneApprovedTitle


class TitleFilter(django_filters.FilterSet):
    capstone_title = django_filters.CharFilter(lookup_expr="icontains")
    sort_by = django_filters.ChoiceFilter(
        choices=[
            ("date_added", "Sort By: Date Added"),
            ("title", "Sort By: Capstone Title"),
        ],
        method="sorted_by",
    )

    class Meta:
        model = CapstoneApprovedTitle
        fields = ["capstone_title"]

    def sorted_by(self, queryset, name, value):
        if value == "date_added":
            return queryset.order_by("created_at")
        elif value == "title":
            return queryset.order_by("capstone_title")
        return queryset
