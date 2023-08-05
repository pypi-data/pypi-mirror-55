# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from irekua_database.models import CollectionType
from irekua_database.models import SamplingEventType

from irekua_rest_api.serializers.object_types import sampling_events
from . import types


MODEL = CollectionType.sampling_event_types.through  # pylint: disable=E1101


class SelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = MODEL
        fields = (
            'url',
            'id',
        )


class ListSerializer(serializers.ModelSerializer):
    sampling_event_type = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=True,
        source='samplingeventtype')

    class Meta:
        model = MODEL
        fields = (
            'url',
            'id',
            'sampling_event_type',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    sampling_event_type = sampling_events.types.SelectSerializer(
        many=False,
        read_only=True,
        source='samplingeventtype')
    collection_type = types.SelectSerializer(
        many=False,
        read_only=True,
        source='collectiontype')

    class Meta:
        model = MODEL
        fields = (
            'url',
            'id',
            'collection_type',
            'sampling_event_type',
        )


class CreateSerializer(serializers.ModelSerializer):
    sampling_event_type = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=False,
        queryset=SamplingEventType.objects.all(),  # pylint: disable=E1101
        source='samplingeventtype')

    class Meta:
        model = MODEL
        fields = (
            'sampling_event_type',
        )

    def create(self, validated_data):
        collection_type = self.context['collection_type']
        validated_data['collectiontype'] = collection_type
        return super().create(validated_data)
