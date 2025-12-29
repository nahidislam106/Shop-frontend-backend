from __future__ import annotations

import random
from io import BytesIO

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from PIL import Image, ImageDraw, ImageFont

from shop.models import Product


PRODUCT_TEMPLATES = [
    {
        "name": "Wireless Headphones",
        "description": "Over-ear Bluetooth headphones with noise cancelling and 30h battery life.",
    },
    {
        "name": "4K Smart TV",
        "description": "Ultra HD 55-inch smart TV with HDR and built-in streaming apps.",
    },
    {
        "name": "Gaming Mouse",
        "description": "Ergonomic RGB gaming mouse with programmable buttons.",
    },
    {
        "name": "Mechanical Keyboard",
        "description": "Compact mechanical keyboard with hot-swappable switches.",
    },
    {
        "name": "Running Shoes",
        "description": "Lightweight running shoes designed for everyday training.",
    },
    {
        "name": "Coffee Maker",
        "description": "Programmable drip coffee maker with reusable filter.",
    },
    {
        "name": "Smartwatch",
        "description": "Fitness-focused smartwatch with heart-rate monitoring and GPS.",
    },
    {
        "name": "Backpack",
        "description": "Everyday backpack with laptop compartment and water-resistant fabric.",
    },
]


class Command(BaseCommand):
    help = "Seed the database with sample products and placeholder images."

    def add_arguments(self, parser):  # type: ignore[override]
        parser.add_argument(
            "--count",
            type=int,
            default=16,
            help="Number of products to create (default: 16)",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete existing products before seeding.",
        )

    def handle(self, *args, **options):  # type: ignore[override]
        count: int = options["count"]

        if options.get("clear"):
            Product.objects.all().delete()
            self.stdout.write(self.style.WARNING("Cleared existing products."))

        self.stdout.write(self.style.MIGRATE_HEADING("Seeding products..."))

        created = 0
        for i in range(count):
            template = random.choice(PRODUCT_TEMPLATES)
            base_name = template["name"]
            name = f"{base_name} #{i + 1}"

            price = random.randint(20, 300)
            discount = random.choice([0, 0, 5, 10, 15, 20, 30])
            stock = random.randint(0, 80)

            product = Product(
                name=name,
                description=template["description"],
                price=price,
                discount_percentage=discount,
                stock_quantity=stock,
            )

            # Generate a simple placeholder image locally using Pillow.
            try:
                img = Image.new("RGB", (600, 600), color=(17, 24, 39))
                draw = ImageDraw.Draw(img)

                text = base_name[:16]
                try:
                    font = ImageFont.truetype("arial.ttf", 36)
                except Exception:  # pragma: no cover - font fallback
                    font = ImageFont.load_default()

                text_width, text_height = draw.textsize(text, font=font)
                position = ((600 - text_width) / 2, (600 - text_height) / 2)
                draw.text(position, text, fill=(250, 250, 250), font=font)

                buffer = BytesIO()
                img.save(buffer, format="PNG")
                filename = f"product-{i+1}.png"
                product.image.save(filename, ContentFile(buffer.getvalue()), save=False)
            except Exception as exc:  # pragma: no cover - best-effort only
                self.stderr.write(f"Failed to generate image for {name}: {exc}")

            product.save()
            created += 1

        self.stdout.write(self.style.SUCCESS(f"Created {created} products."))
