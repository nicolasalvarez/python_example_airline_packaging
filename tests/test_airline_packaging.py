from datetime import datetime, timedelta

import pytest

from airline_packaging.airline_packaging import (
    CLIENTS,    
    DESTINATIONS,
    PACKAGES,
    PACKAGE_FEE,
    ORIGINS,
    Client,
    Destination,
    Origin,
    InvalidClientException,
    InvalidDestinationException,
    InvalidOriginException,
    Package,
    PackageStatus,
)


TODAY = datetime.now().date()
YESTERDAY = datetime.now().date() - timedelta(days=1)


def test_add_client():
    client = Client("John Doe")
    assert client.username == "John Doe"
    assert client in CLIENTS

    # Fake DB transaction
    CLIENTS.remove(client)
    assert len(CLIENTS) == 0


def test_add_origin():
    city_name = "La Pampa"
    org_city = Origin(city_name)
    assert org_city.name == city_name

    # Fake DB transaction
    ORIGINS.remove(org_city)
    assert len(ORIGINS) == 0


def test_add_destination():
    city_name = "Jujuy"
    dest_city = Destination(city_name)
    assert dest_city.name == city_name

    # Fake DB transaction
    DESTINATIONS.remove(dest_city)
    assert len(DESTINATIONS) == 0


def populate_db(clients: bool, origins: bool, destinations: bool):
    """
    Popute the "database" with some data.
    """
    if clients:
        for username in ["user_1", "user_2", "user_3", "user_n"]:
            client = Client(username)
            CLIENTS.append(client)

    if origins:
        for city in ["Buenos Aires", "Cordoba", "Mendoza", "Origin N"]:
            org_city = Origin(city)
            ORIGINS.append(org_city)

    if destinations:
        for city in ["Buenos Aires", "Salta", "Santa Fe", "Misiones", "Destination M"]:
            dest_city = Origin(city)
            DESTINATIONS.append(dest_city)


def delete_db():
    """
    Function used to delete the fake database.
    To be used as a fake transaction.
    """
    CLIENTS.clear()
    PACKAGES.clear()
    ORIGINS.clear()
    DESTINATIONS.clear()


def test_send_package():
    populate_db(clients=True, origins=True, destinations=True)
    # Pick random client and cities
    client = CLIENTS[0]
    org_city = ORIGINS[0]
    dest_city = DESTINATIONS[0]

    package = Package(client, org_city, dest_city)

    assert package in PACKAGES
    assert package.client == client
    assert package.origin == org_city
    assert package.destination == dest_city
    assert package.fee == PACKAGE_FEE
    assert package.status == PackageStatus.LABEL_CREATED

    # Ship package. Only check that its status has changed
    package.ship_package()
    assert package.status == PackageStatus.SHIPPED

    delete_db()


def test_send_package_invalid_client():
    populate_db(clients=False, origins=True, destinations=True)

    # Create a client but delete if from "DB"
    client = Client("invalid_client")
    CLIENTS.clear()

    # Pick cities
    org_city = ORIGINS[0]
    dest_city = DESTINATIONS[0]

    with pytest.raises(InvalidClientException):
        Package(client, org_city, dest_city)


def test_send_package_invalid_org_city():
    populate_db(clients=True, origins=False, destinations=True)

    org_city = Origin("invalid_org_city")
    ORIGINS.clear()

    # Pick random client and dest cities
    client = CLIENTS[0]    
    dest_city = DESTINATIONS[0]

    with pytest.raises(InvalidOriginException):
        Package(client, org_city, dest_city)

    delete_db()


def test_send_package_invalid_dest_city():
    populate_db(clients=True, origins=True, destinations=False)

    dest_city = Origin("invalid_dest_city")
    DESTINATIONS.clear()

    # Pick random client and org cities
    client = CLIENTS[0]    
    org_city = ORIGINS[0]

    with pytest.raises(InvalidDestinationException):
        Package(client, org_city, dest_city)

    delete_db()


def populate_packages(date: datetime.date, amount: int):
    """
    Create/ship packages.

    Args:
        date: date when the packege was sent
        amount: number of packages sent
    """
    for _ in range(amount):
        client = CLIENTS[0]
        org_city = ORIGINS[0]
        dest_city = DESTINATIONS[0]
        package = Package(client, org_city, dest_city)
        package.date = date
        package.ship_package()


@pytest.mark.parametrize("packages_date,no_packages,report_date,expected",
                         [
                             (TODAY, 5, TODAY,
                              {
                                  "date": TODAY,
                                  "total_packages": 5,
                                  "total_revenue": 5 * PACKAGE_FEE
                                  }),
                             (TODAY, 5, YESTERDAY,
                              {
                                  "date": YESTERDAY,
                                  "total_packages": 0,
                                  "total_revenue": 0
                                  }
                              ),
                             (YESTERDAY, 10, YESTERDAY,
                              {
                                  "date": YESTERDAY,
                                  "total_packages": 10,
                                  "total_revenue": 10 * PACKAGE_FEE
                                  }
                              ),
                             (YESTERDAY, 10, TODAY,
                              {
                                  "date": TODAY,
                                  "total_packages": 0,
                                  "total_revenue": 0
                                  }
                              ),
                          ]
                         )
def test_report(freezer, packages_date, no_packages, report_date, expected):
    populate_db(clients=True, origins=True, destinations=True)
    # Pick random client and cities and send packages
    populate_packages(packages_date, no_packages)

    assert Package.generate_report(report_date) == expected

    delete_db()
