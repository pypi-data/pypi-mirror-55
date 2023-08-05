# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from irekua_database.models import EventType

from . import terms


class SelectSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='rest-api:eventtype-detail')
    name = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=False,
        queryset=EventType.objects.all())

    class Meta:
        model = EventType
        fields = (
            'url',
            'name',
        )


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = (
            'url',
            'name',
            'description',
            'icon',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    term_types = terms.SelectSerializer(
        many=True,
        read_only=True)

    class Meta:
        model = EventType
        fields = (
            'url',
            'name',
            'description',
            'icon',
            'term_types',
            'created_on',
            'modified_on'
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = (
            'name',
            'description',
            'icon',
        )


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = (
            'description',
            'icon',
        )
