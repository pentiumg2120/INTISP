import uuid

from django.contrib.auth.hashers import check_password, make_password
from django.db import models


class Note(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField()
    password_hash = models.CharField(max_length=128, null=True, blank=True)
    max_views = models.PositiveIntegerField(default=1)
    current_views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def set_password(self, password):
        if password:
            self.password_hash = make_password(password)

    def check_note_password(self, password):
        if not self.password_hash:
            return True
        return check_password(password, self.password_hash)

    def __str__(self):
        return f"Note {self.id} ({self.current_views}/{self.max_views})"
