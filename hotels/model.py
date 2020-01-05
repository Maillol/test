from datetime import date, timedelta
from typing import Set


class RoomNotFound(Exception):
    """
    Exception levée lorsqu'une chambre n'existe pas.
    """


class NoFreeRoom(Exception):
    """
    Exception levée lorsqu'il n'y a pas de chambre de libre.
    """


class Room:

    def __init__(self, number: int, nb_bed: int):
        self.number = number
        self.nb_bed = nb_bed
        self.dates: Set[date] = set()


class Hotel:
    """
    Hotel pour simuler des réservation de chambre.

    Paramètres:
      - name: Le nom de l'hotel
      - address: L'adresse de l'hotel

    Exemple:

    >>> hotel = Hotel('Napoleon', 'Rue du col Bayard')
    >>> hotel.name
    'Napoleon'
    >>> hotel.add_room(1, nb_bed=2)
    >>> room = hotel.get_room(1)
    >>> room.nb_bed
    2
    """

    def __init__(self,
                 name: str,
                 address: str):
        self.name = name
        self.address = address
        self.rooms = []

    def add_room(self, number: int, nb_bed: int):
        """
        Ajouter une chambre à l'hotel.

        Paramètres:
          - numbre: Le numéro de chambre
          - nb_bed: Le nombre de couchage que contiendra la chambre
        """
        self.rooms.append(Room(number, nb_bed))

    def get_room(self, number: int) -> Room:
        """
        Retourne la chambre correspondante au numéro de chambre donnée.

        Si le numéro de chambre n'existe pas une exception RoomNotFound
        est lancée.
        """
        for room in self.rooms:
            if room.number == number:
                return room
        raise RoomNotFound(f"La chambre {number} n'éxiste pas")

    def book(self, start_date: date, duration: int, nb_bed: int):
        """
        Réserve une chambre dans l'hotel.

        Paramètres:
          - start_date: Date du premier jour de la réservation.
          - duration: La durée du séjour en jour.
          - nb_bed: Nombre de couchages.
        """
        for room in self.rooms:
            if start_date not in room.dates and room.nb_bed == nb_bed:
                for day in range(duration + 1):
                    room.dates.add(start_date + timedelta(days=day))
                return

        raise NoFreeRoom(f"Pas de chambre libre")
