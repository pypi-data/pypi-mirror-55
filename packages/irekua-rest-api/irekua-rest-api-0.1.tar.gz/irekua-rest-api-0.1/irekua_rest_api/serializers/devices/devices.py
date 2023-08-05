# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from irekua_database.models import Device

from irekua_rest_api.serializers.object_types import devices
from . import brands


class SelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = (
            'url',
            'id',
        )


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = (
            'url',
            'id',
            'device_type',
            'brand',
            'model',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    device_type = devices.SelectSerializer(
        many=False,
        read_only=True)
    brand = brands.SelectSerializer(
        many=False,
        read_only=True)

    class Meta:
        model = Device
        fields = (
            'url',
            'id',
            'device_type',
            'brand',
            'model',
            'metadata_schema',
            'configuration_schema',
            'created_on',
            'modified_on',
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = (
            'device_type',
            'brand',
            'model',
            'metadata_schema',
            'configuration_schema',
        )
