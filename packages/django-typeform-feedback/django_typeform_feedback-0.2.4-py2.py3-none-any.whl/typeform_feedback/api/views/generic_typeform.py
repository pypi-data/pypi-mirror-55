from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from ...models import GenericTypeformFeedback
from ..serializers import GenericTypeformUrlSerializer


class GenericTypeformApiView(generics.RetrieveAPIView):

    serializer_class = GenericTypeformUrlSerializer
    permission_classes = (IsAuthenticated, )
    lookup_field = 'quiz_slug'
    lookup_url_kwarg = 'quiz_slug'
    queryset = GenericTypeformFeedback.objects.all()
