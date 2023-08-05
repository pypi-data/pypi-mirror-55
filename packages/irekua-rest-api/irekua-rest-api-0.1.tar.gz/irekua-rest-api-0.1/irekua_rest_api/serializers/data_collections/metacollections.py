# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from irekua_database.models import MetaCollection

from irekua_rest_api.serializers.users import users


class SelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetaCollection
        fields = (
            'url',
            'name',
        )


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetaCollection
        fields = (
            'url',
            'name',
            'description',
        )


class DetailSerializer(serializers.ModelSerializer):
    created_by = users.SelectSerializer(
        many=False,
        read_only=True)

    class Meta:
        model = MetaCollection
        fields = (
            'url',
            'name',
            'description',
            'created_by',
            'created_on',
            'modified_on',
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetaCollection
        fields = (
            'name',
            'description',
        )

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['created_by'] = user
        return super().create(validated_data)


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetaCollection
        fields = (
            'description',
        )
