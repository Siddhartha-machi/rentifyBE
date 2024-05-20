from django.core.management.base import BaseCommand
from django.db.models import Q

from names_generator import generate_name
from phone_gen import PhoneNumber

from rentifyAuth.models import *


class Command(BaseCommand):
    def handle(self, **options):
        action = options["action"]

        if action == "load":
            return self._load()
        elif action == "del":
            return self._del()
        else:
            print("Unknown action found!")

    def _load(self):
        buyers = self._gen_user("buyer", 30)
        sellers = self._gen_user("seller", 30)

        for i in range(30):
            User.objects.create_user(
                email=sellers[i]["email"],
                password=sellers[i]["password"],
                role=sellers[i]["role"],
                first_name=sellers[i]["first_name"],
                last_name=sellers[i]["last_name"],
                contact=sellers[i]["contact"],
            )
            User.objects.create_user(
                email=buyers[i]["email"],
                password=buyers[i]["password"],
                role=buyers[i]["role"],
                first_name=buyers[i]["first_name"],
                last_name=buyers[i]["last_name"],
                contact=buyers[i]["contact"],
            )

        print("Buyer and seller data loaded succssfully.")

    def _del(self):
        User.objects.filter(~Q(role="admin")).delete()
        print("Deleted all buyers and sellers.")

    def add_arguments(self, parser):
        parser.add_argument(
            "action",
            type=str,
            help="Add 'load' flag to load data and 'del' to delete the data",
        )

    def _gen_user(self, role, count):
        data = []
        for i in range(count):
            first_name, last_name = generate_name(style="capital").split(" ")
            data.append(
                {
                    "email": f"{first_name}.{last_name}@rentify.com".lower(),
                    "password": f"{first_name}#{i + 10}",
                    "role": role,
                    "first_name": first_name,
                    "last_name": last_name,
                    "contact": PhoneNumber("IN").get_number(),
                }
            )
        return data
