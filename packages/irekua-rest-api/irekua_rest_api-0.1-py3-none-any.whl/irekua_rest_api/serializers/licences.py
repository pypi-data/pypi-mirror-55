# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from irekua_database.models import Licence

from irekua_rest_api.serializers.object_types import licences
from irekua_rest_api.serializers.users import users


class SelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Licence
        fields = (
            'url',
            'id',
        )


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Licence
        fields = (
            'url',
            'id',
            'licence_type',
            'created_on',
            'is_active',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    licence_type = licences.SelectSerializer(many=False, read_only=True)
    signed_by = users.SelectSerializer(many=False, read_only=True)

    class Meta:
        model = Licence
        fields = (
            'url',
            'id',
            'licence_type',
            'created_on',
            'document',
            'metadata',
            'signed_by',
            'is_active',
            'collection'
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Licence
        fields = (
            'licence_type',
            'document',
            'metadata',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            collection = self.context['collection']
        except KeyError:
            collection = None

        self.collection = collection

        try:
            self.fields['licence_type'].queryset = (
                self.collection.collection_type.licence_types)
        except (KeyError, AttributeError):
            pass

    def create(self, validated_data):
        user = self.context['request'].user
        collection = self.context['collection']

        validated_data['signed_by'] = user
        validated_data['collection'] = collection

        return super().create(validated_data)
