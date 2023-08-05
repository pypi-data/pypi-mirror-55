# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from irekua_database.models import DeviceBrand


class SelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceBrand
        fields = (
            'url',
            'name',
        )


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceBrand
        fields = (
            'url',
            'name',
            'logo',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DeviceBrand
        fields = (
            'url',
            'name',
            'website',
            'logo',
            'created_on',
            'modified_on',
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceBrand
        fields = (
            'name',
            'website',
            'logo',
        )
