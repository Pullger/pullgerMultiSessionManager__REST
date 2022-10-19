from rest_framework import serializers


class SessionsListSerializer(serializers.BaseSerializer):

    def to_representation(self, instance):
        return {
            'uuid': instance['uuid_session'],
            'connector': str(instance['connector']),
            'authorization': str(instance['authorization']),
            'used_account': str(instance['used_account']),
            'active': str(instance['active']),
            'in_use': str(instance['in_use']),
            'ready': str(instance['ready']),
            'live': str(instance['live']),
        }
