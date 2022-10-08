from rest_framework import serializers


class SessionsListSerializer(serializers.BaseSerializer):

    def to_representation(self, instance):
        return {
            'uuid': instance['uuid'],
            'connector': str(instance['connector']),
            'authorization': str(instance['authorization']),
            'usedAccount': str(instance['usedAccount']),
            'active': str(instance['active']),
            'inUse': str(instance['inUse']),
            'ready': str(instance['ready']),
            'live': str(instance['live']),
        }