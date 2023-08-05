# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from irekua_database.models import SamplingEventType


class SelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = SamplingEventType
        fields = (
            'url',
            'name'
        )


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SamplingEventType
        fields = (
            'url',
            'name',
            'icon',
            'description',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SamplingEventType
        fields = (
            'url',
            'name',
            'description',
            'icon',
            'metadata_schema',
            'restrict_device_types',
            'restrict_site_types',
            'created_on',
            'modified_on',
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SamplingEventType
        fields = (
            'name',
            'description',
            'icon',
            'metadata_schema',
            'restrict_device_types',
            'restrict_site_types',
        )


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SamplingEventType
        fields = (
            'description',
            'icon',
        )
