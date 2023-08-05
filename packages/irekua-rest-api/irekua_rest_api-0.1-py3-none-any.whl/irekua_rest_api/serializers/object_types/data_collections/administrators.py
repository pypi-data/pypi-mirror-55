# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from irekua_database.models import CollectionType

from irekua_rest_api.serializers.users import users
from . import types


MODEL = CollectionType.administrators.through  # pylint: disable=E1101


class SelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = MODEL
        fields = (
            'url',
            'id',
        )


class ListSerializer(serializers.ModelSerializer):
    user = serializers.CharField(
        read_only=True,
        source='user.username')

    class Meta:
        model = MODEL
        fields = (
            'url',
            'id',
            'user',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    user = users.SelectSerializer(
        many=False,
        read_only=True)
    collection_type = types.SelectSerializer(
        many=False,
        read_only=True,
        source='collectiontype')

    class Meta:
        model = MODEL
        fields = (
            'url',
            'id',
            'collection_type',
            'user',
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MODEL
        fields = (
            'user',
        )

    def create(self, validated_data):
        collection_type = self.context['collection_type']
        validated_data['collectiontype'] = collection_type
        return super().create(validated_data)
