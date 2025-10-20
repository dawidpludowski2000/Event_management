from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from events.models import Event
from events.serializers.event_list import EventListSerializer

from config.core.api_response import success  


class EventListPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"


class EventListView(generics.ListAPIView):
    queryset = Event.objects.filter(status="published").order_by("start_time")
    serializer_class = EventListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["start_time", "location", "organizer"]
    pagination_class = EventListPagination
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        page = self.paginate_queryset(self.get_queryset())
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
           
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(self.get_queryset(), many=True)

        return success(data=serializer.data)  # ✅ opakowanie na success
