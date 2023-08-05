# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from irekua_database.models import CollectionType


class SelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionType
        fields = (
            'url',
            'name',
        )


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionType
        fields = (
            'url',
            'name',
            'logo',
            'description',
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionType
        fields = (
            'name',
            'logo',
            'description',
            'metadata_schema',
            'anyone_can_create',
            'restrict_site_types',
            'restrict_annotation_types',
            'restrict_item_types',
            'restrict_licence_types',
            'restrict_device_types',
            'restrict_event_types',
            'restrict_sampling_event_types',
        )


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionType
        fields = (
            'logo',
            'description',
            'anyone_can_create',
            'restrict_site_types',
            'restrict_annotation_types',
            'restrict_item_types',
            'restrict_licence_types',
            'restrict_device_types',
            'restrict_event_types',
            'restrict_sampling_event_types',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CollectionType
        fields = (
            'url',
            'name',
            'description',
            'logo',
            'metadata_schema',
            'anyone_can_create',
            'restrict_site_types',
            'restrict_annotation_types',
            'restrict_item_types',
            'restrict_licence_types',
            'restrict_device_types',
            'restrict_event_types',
            'restrict_sampling_event_types',
            'created_on',
            'modified_on',
        )
