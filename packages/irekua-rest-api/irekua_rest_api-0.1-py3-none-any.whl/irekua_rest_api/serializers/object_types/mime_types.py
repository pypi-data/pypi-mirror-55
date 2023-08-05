# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from irekua_database.models import MimeType


class SelectSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='rest-api:mimetype-detail')
    class Meta:
        model = MimeType
        fields = (
            'url',
            'mime_type',
            'media_info_schema'
        )


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MimeType
        fields = (
            'url',
            'mime_type',
            'media_info_schema',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MimeType
        fields = (
            'url',
            'mime_type',
            'media_info_schema',
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MimeType
        fields = (
            'mime_type',
            'media_info_schema',
        )


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MimeType
        fields = (
            'mime_type',
            'media_info_schema',
        )
