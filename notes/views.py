from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from .models import Note
from .serializers import NoteSerializer

class NoteViewSet(mixins.CreateModelMixin, 
                  mixins.RetrieveModelMixin, 
                  viewsets.GenericViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        password = request.query_params.get('password')

        # 1. Сначала проверяем пароль
        # Если пароль в БД есть, а в запросе нет или он неверный — 403.
        if instance.password_hash and not instance.check_note_password(password):
            return Response(
                {"detail": "Password required or incorrect"}, 
                status=status.HTTP_403_FORBIDDEN
            )

        # 2. Если пароль верный (или его нет), подготавливаем данные
        serializer = self.get_serializer(instance)
        data = serializer.data

        # 3. ТОЛЬКО ТЕПЕРЬ увеличиваем счетчик и удаляем
        instance.current_views += 1
        if instance.current_views >= instance.max_views:
            instance.delete()
        else:
            instance.save()
            
        return Response(data)