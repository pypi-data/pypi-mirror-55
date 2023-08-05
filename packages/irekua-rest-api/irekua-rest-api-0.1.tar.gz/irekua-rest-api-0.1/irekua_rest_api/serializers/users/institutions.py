# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from irekua_database.models import Institution


class SelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = (
            'url',
            'id',
        )


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = (
            'url',
            'id',
            'institution_name',
            'institution_code',
            'subdependency',
            'logo',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Institution
        fields = (
            'url',
            'id',
            'institution_name',
            'institution_code',
            'subdependency',
            'country',
            'postal_code',
            'address',
            'website',
            'logo',
            'created_on',
            'modified_on',
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = (
            'institution_name',
            'institution_code',
            'subdependency',
            'country',
            'postal_code',
            'address',
            'website',
            'logo',
        )
