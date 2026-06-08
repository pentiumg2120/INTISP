from rest_framework import serializers

from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = Note
        fields = ["id", "content", "password", "max_views", "created_at"]
        read_only_fields = ["id", "created_at"]

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        note = Note.objects.create(**validated_data)
        if password:
            note.set_password(password)
            note.save()
        return note
