# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import Permission
from rest_framework import serializers

from irekua_database.models import Role


class SelectPermissionSerializer(serializers.ModelSerializer):
    codename = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field='codename',
        queryset=Permission.objects.filter(content_type__model='collection'))

    class Meta:
        model = Permission
        fields = (
            'codename',
        )


class SelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = (
            'url',
            'name',
        )


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = (
            'url',
            'name',
            'description',
            'icon',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    permissions = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='codename')

    class Meta:
        model = Role
        fields = (
            'url',
            'name',
            'description',
            'permissions',
            'icon',
            'modified_on',
            'created_on',
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = (
            'name',
            'description',
            'icon',
        )


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = (
            'description',
            'icon',
        )
