# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from irekua_database.models import Term

from irekua_rest_api.serializers.object_types import terms


class SelectSerializer(serializers.ModelSerializer):
    class Meta:
        models = Term
        fields = (
            'url',
            'id',
        )


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Term
        fields = (
            'url',
            'term_type',
            'value',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    term_type = terms.SelectSerializer(many=False, read_only=True)

    class Meta:
        model = Term
        fields = (
            'url',
            'id',
            'term_type',
            'value',
            'description',
            'metadata',
            'created_on',
            'modified_on',
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Term
        fields = (
            'value',
            'description',
            'metadata'
        )

    def create(self, validated_data):
        validated_data['term_type'] = self.context['term_type']
        return super().create(validated_data)


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Term
        fields = (
            'description',
            'metadata'
        )


class EntailmentSerializer(serializers.Serializer):
    term_type = serializers.CharField(
        source='target.term_type')
    description = serializers.CharField(
        source='target.description')
    value = serializers.CharField(
        source='target.value')
    id = serializers.IntegerField(
        source='target.id')
    scope = serializers.CharField(
        source='target.scope')


class TermSerializer(serializers.ModelSerializer):
    term_type = serializers.StringRelatedField(many=False)

    class Meta:
        model = Term
        fields = [
            'id',
            'scope',
            'term_type',
            'value',
            'description',
        ]


class ComplexTermSerializer(serializers.ModelSerializer):
    term_type = serializers.StringRelatedField(many=False)
    entailments = EntailmentSerializer(
        many=True,
        read_only=True,
        source='entailment_source')

    class Meta:
        model = Term
        fields = [
            'id',
            'scope',
            'term_type',
            'value',
            'description',
            'entailments',
        ]
