# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from irekua_database.models import AnnotationTool


class SelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnotationTool
        fields = (
            'url',
            'name',
        )


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnotationTool
        fields = (
            'url',
            'name',
            'version',
            'description',
            'logo',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AnnotationTool
        fields = (
            'url',
            'id',
            'name',
            'version',
            'description',
            'logo',
            'website',
            'configuration_schema',
            'created_on',
            'modified_on'
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnotationTool
        fields = (
            'name',
            'version',
            'description',
            'logo',
            'website',
            'configuration_schema',
        )
