"""Functional tests for the Note REST API.

Tests our custom retrieve() logic: password protection and burn-after-reading.
"""

from rest_framework import status
from rest_framework.test import APITestCase


class TestNoteAPI(APITestCase):
    BASE = "/api/notes/"

    def _create(self, content, **kwargs):
        """Helper to create a note and return the response."""
        return self.client.post(
            self.BASE, {"content": content, **kwargs}, format="json"
        )

    # ── Happy path ────────────────────────────────────────────────────

    def test_create_and_retrieve_note(self):
        """POST creates a note; GET returns it."""
        created = self._create("Hello", max_views=5)
        assert created.status_code == status.HTTP_201_CREATED

        response = self.client.get(f"{self.BASE}{created.data['id']}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["content"] == "Hello"

    # ── Password protection ───────────────────────────────────────────

    def test_password_protection(self):
        """Protected note: 403 without password, 403 wrong, 200 correct."""
        created = self._create("Secret", password="the-key")
        url = f"{self.BASE}{created.data['id']}/"

        assert self.client.get(url).status_code == status.HTTP_403_FORBIDDEN
        assert self.client.get(f"{url}?password=wrong").status_code == status.HTTP_403_FORBIDDEN
        assert self.client.get(f"{url}?password=the-key").status_code == status.HTTP_200_OK

    # ── Burn-after-reading ────────────────────────────────────────────

    def test_burn_after_reading(self):
        """Note is deleted once current_views reaches max_views."""
        created = self._create("Ephemeral", max_views=2)
        url = f"{self.BASE}{created.data['id']}/"

        # Read 1 — survives (1 < 2)
        assert self.client.get(url).status_code == 200
        # Read 2 — returns data, then deleted (2 >= 2)
        assert self.client.get(url).status_code == 200
        # Read 3 — gone
        assert self.client.get(url).status_code == 404

    def test_note_survives_until_limit(self):
        """Note with max_views=3 survives reads 1 and 2, burns on read 3."""
        created = self._create("Multi-read", max_views=3)
        url = f"{self.BASE}{created.data['id']}/"

        assert self.client.get(url).status_code == 200  # views: 1/3
        assert self.client.get(url).status_code == 200  # views: 2/3
        assert self.client.get(url).status_code == 200  # views: 3/3 → deleted
        assert self.client.get(url).status_code == 404  # gone
