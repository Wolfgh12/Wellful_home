from django.core.management.base import BaseCommand
from catalog.models import Category

class Command(BaseCommand):
    help = "Seeds the 7 core product pillars for Wellful Home"

    def handle(self, *args, **options):
        pillars = [
            {
                "pillar_type": "MEDICAL",
                "name": "Wellful Care",
                "icon": "wellful_care.jpg",
                "description": "Diagnostic tools, vital monitors, and everyday health check devices designed for home monitoring and preventive care.",
            },
            {
                "pillar_type": "DEPOSITORY",
                "name": "Wellful Data",
                "icon": "wellful_data.jpg",
                "description": "Security safes, digital storage hardware, and protective vaults designed to safeguard vital family records, legal files, and valuable assets.",
            },
            {
                "pillar_type": "VOLTAGE",
                "name": "Wellful Devices",
                "icon": "wellful_devices.jpg",
                "description": "Certified surge protectors, automatic voltage regulators, and power management equipment engineered to protect household and office electronics.",
            },
            {
                "pillar_type": "FITNESS",
                "name": "Wellful Fitness",
                "icon": "wellful_fitness.jpg",
                "description": "Home treadmills, dumbbells, resistance gear, and mobility aids designed to support everyday fitness, strength training, and active living.",
            },
            {
                "pillar_type": "SUPPLEMENTS",
                "name": "Wellful Food",
                "icon": "wellful_food.jpg",
                "description": "Quality dietary supplements, wellness formulas, and nutritional products crafted to support energy, bone health, and everyday vitality.",
            },
            {
                "pillar_type": "SANITARY",
                "name": "Wellful Sanitary",
                "icon": "wellful_sanitary.jpg",
                "description": "Safety grab rails, accessible bathroom hardware, and clean living essentials built for independence, hygiene, and slip prevention.",
            },
            {
                "pillar_type": "FOOTWEAR",
                "name": "Wellful Sole",
                "icon": "wellful_sole.jpg",
                "description": "Supportive orthopedic shoes, therapeutic insoles, and high-traction footwear engineered for arch support, joint relief, and confident walking.",
            },
        ]

        created_count = 0
        updated_count = 0

        for item in pillars:
            category, created = Category.objects.update_or_create(
                pillar_type=item["pillar_type"],
                defaults={
                    "name": item["name"],
                    "icon": item["icon"],
                    "description": item["description"],
                },
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"+ Created: {category.name}"))
            else:
                updated_count += 1
                self.stdout.write(self.style.WARNING(f"= Synced: {category.name}"))

        self.stdout.write(
            self.style.SUCCESS(
                f"\nSeeding complete. {created_count} added, {updated_count} synced."
            )
        )