from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from reservations.serializers.reservation_create import ReservationCreateSerializer
from events.models.event import Event
from reservations.models import Reservation


class ReservationCreateView(APIView):
    
    permission_classes = [IsAuthenticated]

    
    def post(self, request, event_id): 

        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({"detail": "Wydarzenie nie istnieje."}, status=status.HTTP_404_NOT_FOUND)
        
    
        serializer = ReservationCreateSerializer(

            data={"event": event.id},
            context={"request": request}
        )

        if not serializer.is_valid():
            
            print("❌ Błąd walidacji:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
        
        serializer.save()

        return Response({"detail": "Rejestracja przebiegła pomyślnie."}, status=status.HTTP_201_CREATED)
    
    
   
