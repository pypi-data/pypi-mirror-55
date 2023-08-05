# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from irekua_database.models import DeviceType


class SelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceType
        fields = (
            'url',
            'name',
        )


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceType
        fields = (
            'url',
            'name',
            'description',
            'icon',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DeviceType
        fields = (
            'url',
            'name',
            'description',
            'icon',
            'created_on',
            'modified_on',
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceType
        fields = (
            'name',
            'description',
            'icon',
        )


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceType
        fields = (
            'description',
            'icon',
        )
