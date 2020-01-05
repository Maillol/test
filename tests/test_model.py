import unittest
from datetime import date

from hotels.model import Hotel, RoomNotFound, NoFreeRoom


class TestHotelGetRoom(unittest.TestCase):

    def setUp(self):
        self.hotel = Hotel(
            'california', '22 rue des ours')
        self.hotel.add_room(1, nb_bed=2)
        self.hotel.add_room(2, nb_bed=4)

    def test_l_hotel_doit_avoir_une_chambre_numero_1_avec_2_place(self):
        room = self.hotel.get_room(1)
        self.assertEqual(room.nb_bed, 2)
        self.assertEqual(room.number, 1)

    def test_l_hotel_doit_avoir_une_chambre_numero_2_avec_4_place(self):
        ...

    def test_l_hotel_ne_doit_pas_avoir_de_chambre_numero_3(self):
        with self.assertRaises(RoomNotFound) as context:
            self.hotel.get_room(3)

        self.assertEqual(
            str(context.exception), "La chambre 3 n'éxiste pas")

    def test_on_ne_peut_pas_ajouter_une_chambre_qui_existe(self):
        ...


class TestHotelBook(unittest.TestCase):

    def setUp(self):
        self.hotel = Hotel(
            'california', '22 rue des ours')
        self.hotel.add_room(1, nb_bed=2)
        self.hotel.add_room(2, nb_bed=4)
        self.hotel.book(
            start_date=date(2018, 10, 3),
            duration=3,
            nb_bed=2)

    def test_on_ne_peut_pas_reserver_de_chambre_avec_2_place_a_la_meme_date(self):
        with self.assertRaises(NoFreeRoom):
            self.hotel.book(
                start_date=date(2018, 10, 4),
                duration=3,
                nb_bed=2)

    def test_on_peut_reserver_une_chambre_de_4_place_a_la_meme_date(self):
        ...

    def test_on_peut_reserver_une_chambre_de_2_place_a_une_autre_date(self):
        ...
