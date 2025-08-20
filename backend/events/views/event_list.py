from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from events.models.event import Event
from events.serializers.event_list import EventListSerializer
from rest_framework.pagination import PageNumberPagination


class EventListPagination(PageNumberPagination):

    page_size = 20
    page_size_query_param = "page_size"


class EventListView(generics.ListAPIView):

    queryset = Event.objects.filter(status="published").order_by("start_time")
    serializer_class = EventListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["start_time", "location", "organizer"]
    pagination_class = EventListPagination
    permission_classes = []  