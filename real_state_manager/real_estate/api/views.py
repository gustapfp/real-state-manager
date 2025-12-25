from rest_framework import authentication
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from structlog import get_logger

from real_state_manager.guests.models import Guest
from real_state_manager.real_estate.api.serializers import PropertySerializer
from real_state_manager.real_estate.api.serializers import ReservationSerializer
from real_state_manager.real_estate.api.serializers import ReservationUpdateSerializer
from real_state_manager.real_estate.api.utils import helper
from real_state_manager.real_estate.models import Property
from real_state_manager.real_estate.models import Reservation

logger = get_logger()


class PropertyView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Get all properties for the authenticated user

        Args:
            request (_type): Request object

        Returns:
            _type_: Response object
        """
        try:
            properties = Property.objects.filter(user=request.user)  # pyright: ignore[reportAttributeAccessIssue]
            serializer = PropertySerializer(properties, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception("Unable to retrieve properties for user", error=e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """Create a new property for the authenticated user

        Args:
            request (_type): Request object

        Returns:
            _type_: Response object
        """
        try:
            serializer = PropertySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            logger.error("Invalid data for property creation", errors=serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception("Unable to create property", error=e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReservationView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, cpf: str):
        """Get all reservations for a guest

        Args:
            request (_type): Request object
            cpf (str): Guest CPF

        Returns:
            _type_: Response object
        """
        try:
            reservations = Reservation.objects.filter(guest__cpf=cpf)
            serializer = ReservationSerializer(reservations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception("Unable to retrieve reservations for guest", error=e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, cpf: str):
        """Create a new reservation for a guest

        Args:
            request (_type): Request object
            cpf (str): Guest CPF

        Returns:
            _type_: Response object
        """
        try:
            guest = Guest.objects.get(cpf=cpf)

            serializer = ReservationSerializer(data=request.data)
            if serializer.is_valid() and helper.is_available_to_rent(
                request.data["property"],
                request.data["check_in"],
                request.data["check_out"],
            ):
                serializer.save(guest=guest)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            logger.warning(
                "Property is not available to rent",
                property_id=request.data["property"],
                check_in=request.data["check_in"],
                check_out=request.data["check_out"],
                guest_cpf=cpf,
            )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Guest.DoesNotExist:
            logger.exception("Guest not found", cpf=cpf)
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.exception("Unable to create reservation", error=e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request):
        """Update a reservation

        Args:
            request (_type): Request object

        Returns:
            _type_: Response object
        """
        try:
            reservation = Reservation.objects.get(id=request.data["property"])
            serializer = ReservationUpdateSerializer(reservation, data=request.data)
            if serializer.is_valid() and helper.is_available_to_rent(
                request.data["property"],
                request.data["check_in"],
                request.data["check_out"],
            ):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            logger.error(
                "Invalid data for reservation update",
                errors=serializer.errors,
            )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Reservation.DoesNotExist:
            logger.exception(
                "Reservation not found",
                reservation_id=request.data["property"],
            )
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.exception("Unable to update reservation", error=e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
