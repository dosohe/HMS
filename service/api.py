from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from service import models, serializers
from service.business_logic.guest_ready import GuestReadyCommission


class ReservationSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin, 
    mixins.RetrieveModelMixin,
):
    queryset = models.Reservation.objects.all()
    serializer_class = serializers.Reservation
    lookup_field = "slug"

    @action(detail=False, methods=["get"])
    def total_commission(self, request):
        try: 
            com = GuestReadyCommission(request.query_params).commission
        except Exception as err:
            return Response({"error": f"{err}"}, status=422)
        return Response(com, status=200)

    @action(detail=False, methods=["get"])
    def monthly_commission(self, request):
        try: 
            com = GuestReadyCommission(request.query_params).dict_commission
        except Exception as err:
            return Response({"error": f"{err}"}, status=422)
        return Response(com, status=200)

