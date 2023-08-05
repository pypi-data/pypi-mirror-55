# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from irekua_database.models import CollectionUser

from irekua_rest_api.serializers.users import users
from irekua_rest_api.serializers.users import roles


class SelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionUser
        fields = (
            'url',
            'id',
        )


class ListSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username')
    role = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='name')

    class Meta:
        model = CollectionUser
        fields = (
            'url',
            'id',
            'user',
            'role',
            'metadata',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    user = users.SelectSerializer(many=False, read_only=True)
    role = roles.SelectSerializer(many=False, read_only=True)

    class Meta:
        model = CollectionUser
        fields = (
            'url',
            'user',
            'role',
            'metadata',
            'created_on',
            'modified_on',
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionUser
        fields = (
            'user',
            'role',
            'metadata',
        )

    def create(self, validated_data):
        collection = self.context['collection']
        validated_data['collection'] = collection
        return super().create(validated_data)


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionUser
        fields = (
            'metadata',
        )


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionUser
        fields = (
            'role',
        )
