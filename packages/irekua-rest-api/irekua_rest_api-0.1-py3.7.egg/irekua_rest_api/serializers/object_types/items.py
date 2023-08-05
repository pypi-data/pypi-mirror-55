# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from irekua_database.models import ItemType

from . import events
from . import mime_types


class SelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemType
        fields = (
            'url',
            'name',
        )


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemType
        fields = (
            'url',
            'name',
            'description',
            'icon',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    event_types = events.DetailSerializer(
        many=True,
        read_only=True)
    mime_types = mime_types.SelectSerializer(
        many=True,
        read_only=True)

    class Meta:
        model = ItemType
        fields = (
            'url',
            'name',
            'description',
            'mime_types',
            'icon',
            'event_types',
            'created_on',
            'modified_on',
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemType
        fields = (
            'name',
            'description',
            'icon',
        )


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemType
        fields = (
            'description',
            'icon',
        )
