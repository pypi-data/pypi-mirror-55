# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from irekua_database.models import Annotation
from irekua_database.models import AnnotationTool

from irekua_rest_api.serializers.terms.terms import ListSerializer as TermListSerializer
from irekua_rest_api.serializers.terms.terms import ComplexTermSerializer
from irekua_rest_api.serializers.users.users import ListSerializer as UserListSerializer


class SelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annotation
        fields = (
            'url',
            'id',
        )


class ListSerializer(serializers.ModelSerializer):
    labels = TermListSerializer(many=True)
    created_by = UserListSerializer()

    class Meta:
        model = Annotation
        fields = (
            'url',
            'id',
            'item',
            'event_type',
            'annotation',
            'annotation_type',
            'created_on',
            'created_by',
            'labels'
        )


class DetailSerializer(serializers.ModelSerializer):
    labels = ComplexTermSerializer(many=True)

    class Meta:
        model = Annotation
        fields = (
            'url',
            'id',
            'annotation_tool',
            'item',
            'event_type',
            'labels',
            'annotation_type',
            'annotation',
            'annotation_configuration',
            'certainty',
            'quality',
            'commentaries',
            'created_on',
            'modified_on',
            'created_by',
            'modified_by',
        )


class AnnotationToolSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    version = serializers.CharField(required=True)
    description = serializers.CharField(required=False)
    logo = serializers.CharField(required=False)
    website = serializers.CharField(required=False)
    configuration_schema = serializers.JSONField(required=False)


class CreateSerializer(serializers.ModelSerializer):
    annotation_tool = AnnotationToolSerializer()

    class Meta:
        model = Annotation
        fields = (
            'event_type',
            'annotation',
            'labels',
            'certainty',
            'quality',
            'commentaries',
            'annotation_tool',
            'annotation_configuration',
            'annotation_type',
        )

    def create(self, validated_data):
        item = self.context['item']
        user = self.context['request'].user

        annotation_tool_info = validated_data.pop('annotation_tool')

        name = annotation_tool_info.pop('name')
        version = annotation_tool_info.pop('version')
        annotation_tool, _ = AnnotationTool.objects.get_or_create(
            name=name,
            version=version,
            defaults=annotation_tool_info)
        annotation_tool.save()

        validated_data['item'] = item
        validated_data['created_by'] = user
        validated_data['modified_by'] = user
        validated_data['annotation_tool'] = annotation_tool

        labels = validated_data.pop('labels')
        annotation = Annotation(**validated_data)
        annotation.save()

        annotation.labels.set(labels)
        annotation.save()
        return annotation


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annotation
        fields = (
            'annotation',
            'labels',
            'certainty',
            'quality',
            'commentaries',
            'annotation_configuration',
        )

    def update(self, instance, validated_data):
        user = self.context['request'].user

        validated_data['modified_by'] = user
        return super().update(instance, validated_data)
