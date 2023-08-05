# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from irekua_database.models import Collection

from irekua_rest_api.serializers.users import users
from . import data_collections


MODEL = Collection.administrators.through  # pylint: disable=E1101


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
    collection = data_collections.SelectSerializer(
        many=False,
        read_only=True)

    class Meta:
        model = MODEL
        fields = (
            'url',
            'id',
            'collection',
            'user',
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MODEL
        fields = (
            'user',
        )

    def create(self, validated_data):
        collection = self.context['collection']
        validated_data['collection'] = collection
        return super().create(validated_data)
