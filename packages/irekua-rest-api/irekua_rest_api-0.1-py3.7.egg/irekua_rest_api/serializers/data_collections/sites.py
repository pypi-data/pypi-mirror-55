# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import gettext as _
from rest_framework import serializers

from irekua_database.models import CollectionSite

from irekua_rest_api.serializers import sites
from . import data_collections


class SelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionSite
        fields = (
            'url',
            'id',
        )


class ListSerializer(serializers.ModelSerializer):
    locality = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        source='site',
        slug_field='locality')

    class Meta:
        model = CollectionSite
        fields = (
            'url',
            'id',
            'site',
            'site_type',
            'locality',
            'internal_id',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    site = sites.SelectSerializer(
        many=False,
        read_only=True)
    collection = data_collections.SelectSerializer(
        many=False,
        read_only=True)

    class Meta:
        model = CollectionSite
        fields = (
            'url',
            'id',
            'collection',
            'site',
            'internal_id',
            'created_on',
            'modified_on',
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionSite
        fields = (
            'site',
            'internal_id',
        )

    def create(self, validated_data):
        collection = self.context['collection']
        validated_data['collection'] = collection
        return super().create(validated_data)
