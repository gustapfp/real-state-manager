from datetime import date

from structlog import get_logger

from real_state_manager.real_estate.models import Reservation

logger = get_logger()


class RealEstateHelper:
    def is_available_to_rent(
        self,
        property_id: str,
        check_in: date,
        check_out: date,
    ) -> bool:
        """Check if a property is available to rent between two dates

        Args:
            property_id (str): Property ID
            check_in (date): Desired check-in date
            check_out (date): Desired check-out date

        Returns:
            bool: True if the property is available
            to rent between the two dates, False otherwise
        """
        try:
            reservations = Reservation.objects.filter(
                property__id=property_id,
                check_in__lte=check_out,
                check_out__gte=check_in,
            )
            return len(reservations) == 0
        except Exception as e:
            logger.exception(
                "Unable to check if property is available to rent",
                error=e,
            )
            return False


helper = RealEstateHelper()
