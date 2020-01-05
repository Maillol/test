import argparse
from cmd import Cmd
import datetime
import pathlib
import pickle
from typing import Optional

from .model import Hotel, NoFreeRoom


class HotelCmd(Cmd):

    path_to_file: Optional[pathlib.Path]
    hotel: Hotel

    def __init__(self, completekey='tab', stdin=None, stdout=None):
        super().__init__(completekey, stdin, stdout)
        self.hotel = Hotel(name='Nouvel Hotel',
                           address='')
        self.prompt = f'({self.hotel.name}) '
        self.path_to_file = None

    def do_load(self, arg):
        """
        Charger un fichier.
        """
        if not arg:
            print(f"Vous devez donner un nom de fichier")
            return

        path_to_file = pathlib.Path(arg)
        if not path_to_file.is_file():
            print(f"Le fichier {arg!r} n'existe pas")
            return

        with path_to_file.open('rb') as file:
            self.hotel = pickle.load(file)
        self.path_to_file = path_to_file
        self.prompt = f'({self.hotel.name}) '

    # def complete_load(self, text, line, begidx, endidx):
    #     arg = line.strip().split(None, 1)[1]
    #     path = pathlib.Path(arg) # arg
    #     try:
    #         if path.is_dir():
    #             return [
    #                 str(file)
    #                 for file
    #                 in path.iterdir()
    #             ]
    #
    #         return [
    #             str(file)
    #             for file
    #             in path.parent.iterdir()
    #             if file.name.startswith(path.name)
    #         ]
    #     except OSError:
    #         return []

    def do_save(self, arg):
        """
        Sauvegarder les modifications dans le fichier courant ou dans le nom
        de fichier donné.

        Exemple: save mon_fichier
        """
        if not arg and not self.path_to_file:
            print('Vous devez donner un nom de fichier'
                  ' pour sauvegarder vos modifications')
            return

        if arg:
            path_to_file = pathlib.Path(arg)
        else:
            path_to_file = self.path_to_file

        with path_to_file.open('wb') as file:
            pickle.dump(self.hotel, file)
            self.path_to_file = path_to_file

    def do_rename(self, arg):
        """
        Changer le nom de l'hotel.

        Exemple: rename La Grange
        """
        if not arg:
            print("Erreur: Vous n'avez pas donné de nom")
        else:
            self.hotel.name = arg
            self.prompt = f'({arg}) '

    def do_address(self, arg):
        """
        Changer ou afficher l'adresse de l'hotel.

        Exemple changer l'adresse:
            adress 22 rue du fleuve

        Exemple afficher l'adresse:
            adress
        """
        if not arg:
            print(self.hotel.address or "L'hotel n'a pas d'adresse !")
        else:
            self.hotel.address = arg

    def do_add_room(self, arg):
        """
        Ajouter une chambre en indiquant son numéro et son nombre de
        couchages.

        add_room  N°-de-chambre  nombre-de-couchages
        """
        try:
            room_number, nb_bed = arg.split()
            room_number, nb_bed = int(room_number), int(nb_bed)
        except ValueError:
            print("Erreur: Vous n'avez pas donné le numéro de chambre"
                  " suivie du nombre de couchages")
            return

        self.hotel.add_room(room_number, nb_bed)

    def do_list_rooms(self, arg):
        """
        Afficher la liste des chambres
        """
        print('|  N°  | COUCHAGES |')
        for room in self.hotel.rooms:
            print(f"| {room.number:04} | {room.nb_bed:>9} |")

    def do_book(self, arg):
        """
        Reserver une chambre

        book  date  nombre-de-nuits  nombre-de-couchages

        Exemple:
            book  2018-12-02  4  2
        """

        try:
            date, nb_night, nb_bed = arg.split()
            date, nb_night, nb_bed = \
                datetime.date.fromisoformat(date), int(nb_night), int(nb_bed)
        except ValueError:
            print("Erreur: Vous n'avez pas donné la date au format (YYYY-MM-DD), suivi du nombre de nuits,"
                  " suivie du nombre de couchages")

        try:
            self.hotel.book(date, nb_night, nb_bed)
        except NoFreeRoom:
            print('Pas de chambre libre')
        else:
            print('La chambre a été réservé')

    def do_bye(self, arg):
        """
        Quitter l'application.
        """
        return True

    # The application must quit if the End Of File is reached in order
    # to allow the command lines from file reading.
    do_EOF = do_bye

    def get_names(self):
        # This method is redefined to hide EOF command from help.
        names = super().get_names()
        names.remove('do_EOF')
        return names


def load_file_or_create(file_name: str) -> Hotel:
    """
    Load the Hotel from file or create a new hotel.
    """
    path_to_file = pathlib.Path(file_name)
    if not path_to_file.is_file():
        hotel = Hotel(name='Nouvel Hotel', address='')

    else:
        with path_to_file.open('rb') as file:
            hotel = pickle.load(file)

    return hotel


def save_hotel(file_name: str, hotel: Hotel):
    """
    Save the hotel to file.
    """
    path_to_file = pathlib.Path(file_name)

    with path_to_file.open('wb') as file:
        pickle.dump(hotel, file)


def hotel_update_cmd(args):
    hotel = load_file_or_create(args.file)
    if args.name:
        hotel.name = args.name

    if args.address:
        hotel.address = args.address

    save_hotel(args.file, hotel)


def hotel_display_cmd(args):
    hotel = load_file_or_create(args.file)
    print(hotel.name)
    print(hotel.address)
    print()
    print('|  N°  | COUCHAGES |')
    for room in hotel.rooms:
        print(f"| {room.number:04} | {room.nb_bed:>9} |")

def hotel_add_room_cmd(args):
    hotel = load_file_or_create(args.file)
    hotel.add_room(args.number, args.nb_bed)
    save_hotel(args.file, hotel)


def book_cmd(args):
    hotel = load_file_or_create(args.file)
    try:
        hotel.book(args.date, args.duration, args.nb_bed)
    except NoFreeRoom:
        print('Pas de chambre libre')
    else:
        print('La chambre a été réservé')
    save_hotel(args.file, hotel)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', default='hotel.pkl',
                        help='Fichier qui sera utilisé pour sauvegarder'
                             ' les modifications. Par defaut, %(default)s'
                             ' sera utilisé')
    parser.set_defaults(func=lambda args: parser.print_help())

    subparsers = parser.add_subparsers()

    hotel_parser = subparsers.add_parser(
        'hotel', help="Gérer les informations de l'hotel")
    hotel_parser.set_defaults(func=lambda args: hotel_parser.print_help())

    hotel_subparsers = hotel_parser.add_subparsers()

    hotel_add_room_parser = hotel_subparsers.add_parser(
        'add-room', help="Ajouter une chambre à l'hotel")
    hotel_add_room_parser.add_argument(
        'number',
        type=int,
        help="Le numéro de la chambre à ajouter")
    hotel_add_room_parser.add_argument(
        'nb_bed',
        type=int,
        help="Nombre de couchage")
    hotel_add_room_parser.set_defaults(func=hotel_add_room_cmd)

    hotel_update_parser = hotel_subparsers.add_parser(
        'update', help="Modifier l'adresse ou le nom de l'hotel")
    hotel_update_parser.add_argument(
        '--name', help="Le nouveau nom de l'hotel")
    hotel_update_parser.add_argument(
        '--address', help="Le nouveau nom de l'hotel")
    hotel_update_parser.set_defaults(func=hotel_update_cmd)

    hotel_display_parser = hotel_subparsers.add_parser(
        'display', help="Afficher des informations l'hotel")
    hotel_display_parser.set_defaults(func=hotel_display_cmd)

    book_parser = subparsers.add_parser(
        'book', help="Reserver une chambre")
    book_parser.add_argument(
        'date',
        type=datetime.date.fromisoformat,
        help="Date d'arrivé au format AAAA-MM-JJ")
    book_parser.add_argument(
        'duration',
        type=int,
        help="Nombre de nuit à reserver")

    book_parser.add_argument(
        'nb_bed',
        type=int,
        help="Nombre de couchages")
    book_parser.set_defaults(func=book_cmd)

    shell_parser = subparsers.add_parser(
        'shell', help="Lancer le mode interactive")
    shell_parser.set_defaults(func=lambda args: HotelCmd().cmdloop())

    args = parser.parse_args()
    args.func(args)
