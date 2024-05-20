from django.core.management.base import BaseCommand
from django.db.models import Q

from faker import Faker

from rentifyV1.models import *
from rentifyAuth.models import *


class Command(BaseCommand):
    def handle(self, **options):
        action = options["action"]

        try:
            if action == "load":
                return self._load()
            elif action == "del":
                return self._del()
            else:
                print("Unknown action found!")
        except Exception as e:
            print("Unknown error occured!", e)
            self._del()

    def _load(self):
        # load dependency models data first
        self._load_tags()
        self._load_locations()
        self._load_categories()

        property_data = self._gen_property_data()
        seller = User.objects.filter(role="seller")
        buyers = User.objects.filter(role="buyer")
        tags = Tag.objects.all()
        locations = Location.objects.all()
        categories = Category.objects.all()

        save_data = []
        # set all the required fields and save the data
        for i, prop in enumerate(property_data):
            save_data.append(
                Property(
                    name=prop["name"],
                    price=prop["price"],
                    location=locations[i % 10],
                    place=prop["place"],
                    street=prop["street"],
                    bedrooms=prop["bedrooms"],
                    baths=prop["baths"],
                    seller=seller[i],
                )
            )

        save_data = Property.objects.bulk_create(save_data)

        # Add the many-to-many fields data
        for i, prop in enumerate(save_data):
            prop.wishlist.set([buyers[i]])
            prop.like.set([buyers[i]])
            prop.tags.set([tags[i % 10]])
            prop.category.set([categories[i % 4]])
            prop.save()

        print("Property data loaded succssfully.")

    def _del(self):
        Property.objects.all().delete()
        Tag.objects.all().delete()
        Category.objects.all().delete()
        Location.objects.all().delete()
        print("Flushed all renitfyv1 data.")

    def add_arguments(self, parser):
        parser.add_argument(
            "action",
            type=str,
            help="Add 'load' flag to load data and 'del' to delete the data. Ex: python3 manage.py utils 'load'",
        )

    def _load_tags(self):
        lst = [
            "Hospital",
            "Bank",
            "Police Station",
            "Market",
            "Mall",
            "Theatre",
            "Amusement Park",
            "Hardware Store",
            "School",
            "University",
        ]
        Tag.objects.bulk_create([Tag(name=t) for t in lst])
        print("Loaded tags.")

    def _load_categories(self):
        categories = ["Appartment", "House", "Villa", "Rooms"]
        Category.objects.bulk_create([Category(name=c) for c in categories])
        print("Loaded categories.")

    def _load_locations(self):
        generator = Faker()
        locations = set(generator.city() for _ in range(10))
        Location.objects.bulk_create([Location(name=l) for l in locations])
        print("Loaded locations.")

    def _gen_property_data(self):
        generator = Faker("it_IT")

        data = []
        for i in range(30):
            address = generator.address().split("\n")
            data.append(
                {
                    "name": generator.name() + "Appartment",
                    "price": generator.random_number(digits=1, fix_len=True) * 1000,
                    "place": address[0],
                    "street": address[-1],
                    "bedrooms": generator.random_number(digits=1, fix_len=True),
                    "baths": generator.random_number(digits=1, fix_len=True),
                }
            )

        return data
