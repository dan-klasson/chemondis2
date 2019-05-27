from rest_framework import serializers


class IsOnTheHourValidator:

    def __init__(self, fields):
        self.fields = fields

    def __call__(self, dic):
        for field in self.fields:
            dt = dic.get(field)
            if dt.minute != 0 or dt.second != 0:
                raise serializers.ValidationError(
                    {field: ["Datetime must be on the hour."]}
                )
