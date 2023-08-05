# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from irekua_database.models import SiteType


class SelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteType
        fields = (
            'url',
            'name',
        )


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteType
        fields = (
            'url',
            'name',
            'description',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SiteType
        fields = (
            'url',
            'name',
            'description',
            'metadata_schema'
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteType
        fields = (
            'name',
            'description',
            'metadata_schema'
        )


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteType
        fields = (
            'description',
        )
