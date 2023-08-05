# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from irekua_database.models import LicenceType


class SelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = LicenceType
        fields = (
            'url',
            'name',
        )


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = LicenceType
        fields = (
            'url',
            'name',
            'description',
            'icon',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LicenceType
        fields = (
            'url',
            'name',
            'description',
            'metadata_schema',
            'document_template',
            'years_valid_for',
            'icon',
            'can_view',
            'can_download',
            'can_view_annotations',
            'can_annotate',
            'can_vote_annotations',
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LicenceType
        fields = (
            'name',
            'description',
            'metadata_schema',
            'document_template',
            'years_valid_for',
            'icon',
            'can_view',
            'can_download',
            'can_view_annotations',
            'can_annotate',
            'can_vote_annotations',
        )


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LicenceType
        fields = (
            'description',
            'icon',
        )
