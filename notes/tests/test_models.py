"""Unit tests for Note model — password hashing and verification."""

import pytest

from notes.models import Note


@pytest.mark.django_db
class TestNotePassword:
    def test_set_and_check_password(self):
        """set_password hashes the password; check_note_password verifies it."""
        note = Note.objects.create(content="secret")
        note.set_password("correct")
        assert note.check_note_password("correct") is True
        assert note.check_note_password("wrong") is False

    def test_no_password_always_passes(self):
        """Without a password_hash the note is public — any password is accepted."""
        note = Note.objects.create(content="public")
        assert note.check_note_password("anything") is True
        assert note.check_note_password(None) is True
