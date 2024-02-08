import datetime
from enum import Enum

PACKAGE_FEE = 10

# Given that no framework should be used, the following dics are gonna be the "database tables":
CLIENTS = []
PACKAGES = []
ORIGINS = []
DESTINATIONS = []


class InvalidClientException(Exception):
    """
    Exception raised when a Client doesn't exist in the database
    """


class InvalidOriginException(Exception):
    """
    Exception raised when a Origin City doesn't exist in the database
    """


class InvalidDestinationException(Exception):
    """
    Exception raised when a Destination City doesn't exist in the databse
    """


class Client:
    """
    An airline's client.
    """
    def __init__(self, username: str) -> None:
        self.username = username
        CLIENTS.append(self)


class City:
    """
    City.
    """
    def __init__(self, name: str) -> None:
        self.name = name


class Origin(City):
    """
    City that is an Origin for the Airline
    """
    def __init__(self, name: str):
        super().__init__(name)
        ORIGINS.append(self)


class Destination(City):
    """
    City that is an Destination for the Airline
    """
    def __init__(self, name: str):
        super().__init__(name)
        DESTINATIONS.append(self)


class PackageStatus(Enum):
    """
    Package Statuses
    """
    LABEL_CREATED = "Label Created"
    SHIPPED = "Shipped"


class Package:
    """
    Package that can be sent with the airline.

    A Package should have a registered client and valid origin and destination.
    """
    def __init__(self, client: Client, origin: Origin, destination: Destination):
        self.date = None

        if client not in CLIENTS:
            raise InvalidClientException

        if origin not in ORIGINS:
            raise InvalidOriginException

        if destination not in DESTINATIONS:
            raise InvalidDestinationException

        self.date = datetime.datetime.utcnow()
        self.origin = origin
        self.destination = destination
        self.client = client
        self.fee = PACKAGE_FEE  # Currently is fixed but it could change for different packages.
        self.status = PackageStatus.LABEL_CREATED

        PACKAGES.append(self)

    def ship_package(self):
        """
        Ships the package
        """
        self.status = PackageStatus.SHIPPED

    @staticmethod
    def generate_report(date: datetime.date):
        """
        Generates a report with the total number of packages
        transported and the total amount collected for a given day.

        Args:
            date: The date for which the report must be generated.

        Returns:
            A dict with the following data:
                {"date": date,
                "total_packages": int,
                "total_revenue": int
                }
        """
        total_packages = 0
        total_revenue = 0
        for package in PACKAGES:
            if package.date == date:
                total_packages += 1
                total_revenue += package.fee

        report = {
            "date": date,
            "total_packages": total_packages,
            "total_revenue": total_revenue
            }

        return report
