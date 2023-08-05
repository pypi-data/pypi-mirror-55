# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from irekua_database.models import SecondaryItem

from irekua_rest_api.serializers import object_types
from . import items


class SelectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SecondaryItem
        fields = (
            'url',
            'id',
        )


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecondaryItem
        fields = (
            'url',
            'id',
            'item',
            'item_type'
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    item_type = object_types.items.SelectSerializer(many=False, read_only=True)
    item = items.SelectSerializer(many=False, read_only=True)

    class Meta:
        model = SecondaryItem
        fields = (
            'url',
            'id',
            'hash',
            'item_type',
            'item',
            'media_info',
            'created_on',
            'modified_on',
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecondaryItem
        fields = (
            'hash',
            'item_file',
            'item_type',
            'item',
            'media_info',
        )

    def create(self, validated_data):
        item = self.context['item']
        validated_data['item'] = item
        return super().create(validated_data)


class DownloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecondaryItem
        fields = (
            'item_file',
        )
