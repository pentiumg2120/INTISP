"""Unit tests for NoteSerializer — password handling in create()."""

import pytest

from notes.serializers import NoteSerializer


@pytest.mark.django_db
class TestNoteSerializer:
    def test_create_without_password(self):
        """No password → password_hash stays None."""
        serializer = NoteSerializer(data={"content": "hello", "max_views": 3})
        assert serializer.is_valid(), serializer.errors
        note = serializer.save()
        assert note.password_hash is None

    def test_create_with_password(self):
        """Password is hashed via set_password() during create."""
        serializer = NoteSerializer(data={"content": "secret", "password": "key"})
        assert serializer.is_valid(), serializer.errors
        note = serializer.save()
        assert note.password_hash is not None
        assert note.password_hash != "key"
        assert note.check_note_password("key") is True
