# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from irekua_database.models import AnnotationType


class SelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnotationType
        fields = (
            'url',
            'name',
            'icon',
        )


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnotationType
        fields = (
            'url',
            'name',
            'description',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AnnotationType
        fields = (
            'url',
            'name',
            'description',
            'annotation_schema',
            'icon',
            'created_on',
            'modified_on'
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnotationType
        fields = (
            'name',
            'description',
            'annotation_schema',
            'icon',
        )


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnotationType
        fields = (
            'description',
            'icon',
        )
