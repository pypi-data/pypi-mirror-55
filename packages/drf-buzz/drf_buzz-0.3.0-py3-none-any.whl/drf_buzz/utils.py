from django.utils.translation import gettext_lazy as _

from rest_framework import serializers


def get_serializer_for(codes):
    class DRFBuzzSerializer(serializers.Serializer):
        code = serializers.ChoiceField(choices=codes, required=True, help_text=_("An error code."))
        description = serializers.CharField(required=True, help_text=_("An error description."))
        fields = serializers.DictField(
            required=False, help_text=_("A dictionary mapping field names to a list of error messages.")
        )

    return DRFBuzzSerializer()
