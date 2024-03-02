from django_filters import FilterSet
from django_filters.filters import CharFilter
from rest_framework.exceptions import ValidationError

from ambassadors.choices import CONTENT_STATUS_CHOICES
from ambassadors.models import Content


class UniversalChoiceFilter(CharFilter):
    """
    Универсальный класс для фильтрации по Choice полю.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def filter(self, qs, value):
        """
        Метод фильтрации.
        """
        model = self.parent.Meta.model
        field = model._meta.get_field(self.field_name)
        choices = dict(field.choices)

        if value and value in choices.values():
            reverse_choices = {v: k for k, v in choices.items()}
            value = reverse_choices.get(value)
        else:
            raise ValidationError(
                f"Недопустимое значение для поля: {value}")

        return super().filter(qs, value)


class BaseChoiceFilter(FilterSet):
    """Базовый класс для фильтрации по полю status."""
    status = UniversalChoiceFilter()

    class Meta:
        abstract = True


class ContentStatusFilter(BaseChoiceFilter):
    """Класс для фильтрации Контента по полю status."""

    class Meta(BaseChoiceFilter.Meta):
        model = Content
        fields = ['status']
        status_choices = CONTENT_STATUS_CHOICES

# class ContentFilter(filters.FilterSet):
#     """Запасной вариант, если не использовать логику с базовым классом """
#     status = CharFilter(method='filter_status')
#
#     def filter_status(self, queryset, name, value):
#         # Получение технического значения из человекочитаемого
#         reverse_choices = {v: k for k, v in Content.CONTENT_STATUS_CHOICES}
#         technical_value = reverse_choices.get(value)
#         if technical_value is not None:
#             return queryset.filter(**{name: technical_value})
#         else:
#             raise ValueError(f"Недопустимое значение для статуса: {value}")
#
#     class Meta:
#         model = Content
#         fields = []
