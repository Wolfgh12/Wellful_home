from decimal import Decimal
from django.core.management.base import BaseCommand
from catalog.models import Category, Product

class Command(BaseCommand):
    help = "Seeds realistic starter inventory with specifications and GHS pricing across the 7 pillars"

    def handle(self, *args, **options):
        products_data = [
            # Pillar 1: SANITARY
            {
                "pillar_type": "SANITARY",
                "name": "Heavy-Duty Anti-Slip Grab Rail Set (304 Stainless Steel)",
                "sku": "WFH-SAN-001",
                "price_ghs": Decimal("650.00"),
                "stock_quantity": 25,
                "is_featured": True,
                "description": "Textured diamond-knurled grip bars designed for wet environments. Mounts securely into bathroom tile or masonry to support transfers in showers and near water closets.",
                "specifications": {
                    "Material": "SUS 304 Stainless Steel",
                    "Finish": "Brushed Chrome with Anti-Slip Grip",
                    "Weight Capacity": "200 kg",
                    "Lengths Included": "30 cm and 60 cm",
                    "Hardware": "Corrosion-resistant wall anchors included"
                }
            },
            {
                "pillar_type": "SANITARY",
                "name": "Adjustable Shower Stool with Anti-Microbial Drainage",
                "sku": "WFH-SAN-002",
                "price_ghs": Decimal("850.00"),
                "stock_quantity": 18,
                "is_featured": False,
                "description": "Corrosion-proof aluminum bathing chair with wide non-skid rubber feet that suction firmly onto wet tile floors to prevent slips.",
                "specifications": {
                    "Frame": "Anodized Heavy-Gauge Aluminum",
                    "Height Adjustment": "38 cm - 53 cm (6 levels)",
                    "Seat Dimensions": "51 cm x 31 cm",
                    "Safety Load": "160 kg"
                }
            },

            # Pillar 2: FITNESS
            {
                "pillar_type": "FITNESS",
                "name": "Dual-Direction Low-Impact Pedal Exerciser with Digital Display",
                "sku": "WFH-FIT-001",
                "price_ghs": Decimal("1150.00"),
                "stock_quantity": 15,
                "is_featured": True,
                "description": "Seated circulation and joint mobility trainer. Can be used on the floor for leg pedaling or placed on a tabletop for shoulder and arm rehabilitation.",
                "specifications": {
                    "Resistance": "Adjustable magnetic dial",
                    "Display Metrics": "RPM, Time, Distance, Estimated Calories",
                    "Pedals": "Ergonomic foot straps with heel cups",
                    "Weight": "5.2 kg"
                }
            },
            {
                "pillar_type": "FITNESS",
                "name": "Self-Standing Pivot Quad Cane with Cushion Grip",
                "sku": "WFH-FIT-002",
                "price_ghs": Decimal("480.00"),
                "stock_quantity": 30,
                "is_featured": False,
                "description": "360-degree pivoting base replicates ankle articulation on uneven pavements, compound gravel, and polished tile.",
                "specifications": {
                    "Base": "4-point pivot rubber foot",
                    "Height Range": "74 cm - 97 cm",
                    "Handle": "Ergonomic shock-absorbing contour foam",
                    "Weight": "490 g"
                }
            },

            # Pillar 3: FOOTWEAR
            {
                "pillar_type": "FOOTWEAR",
                "name": "Diabetic Extra-Depth Orthopedic Slip-Ons",
                "sku": "WFH-SHOE-001",
                "price_ghs": Decimal("920.00"),
                "stock_quantity": 20,
                "is_featured": True,
                "description": "Seamless non-binding interior lining built to prevent friction blisters and ulcers, paired with high-traction soles for indoor and veranda tile safety.",
                "specifications": {
                    "Upper": "Breathable stretch mesh with adjustable velcro closure",
                    "Insole": "Dual-density memory foam with arch cradle",
                    "Sole": "High-traction non-marking rubber",
                    "Available Sizes": "EU 39 - 46"
                }
            },

            # Pillar 4: VOLTAGE
            {
                "pillar_type": "VOLTAGE",
                "name": "Sollatek AVS30 Heavy-Duty Voltage Switcher (230V / 30A)",
                "sku": "WFH-VOLT-001",
                "price_ghs": Decimal("1450.00"),
                "stock_quantity": 22,
                "is_featured": True,
                "description": "Protects continuous oxygen concentrators, hospital beds, and refrigeration units against Ghana grid brownouts, voltage spikes, and sudden power returns.",
                "specifications": {
                    "Operating Voltage": "230V AC nominal (50Hz)",
                    "Max Current": "30 Amps",
                    "Protection Range": "Cuts off below 185V and above 260V",
                    "Wait Delay": "Configurable 10s to 3-minute startup delay",
                    "Certification": "CE Certified / GSA Compliant"
                }
            },
            {
                "pillar_type": "VOLTAGE",
                "name": "1200VA Pure Sine Wave Line-Interactive UPS & AVR",
                "sku": "WFH-VOLT-002",
                "price_ghs": Decimal("2650.00"),
                "stock_quantity": 12,
                "is_featured": False,
                "description": "Clean battery backup engineered to keep digital vitals, communication routers, and CPAP machines operating uninterrupted through local outages.",
                "specifications": {
                    "Output Capacity": "1200VA / 720W",
                    "Waveform": "Pure Sine Wave",
                    "Transfer Time": "< 6 ms",
                    "Outlets": "4 Universal protected sockets"
                }
            },

            # Pillar 5: MEDICAL
            {
                "pillar_type": "MEDICAL",
                "name": "Clinical Upper Arm Digital Blood Pressure Monitor with Arrhythmia Detection",
                "sku": "WFH-MED-001",
                "price_ghs": Decimal("890.00"),
                "stock_quantity": 35,
                "is_featured": True,
                "description": "Large-backlit LCD screen with one-touch measurement, irregular heartbeat alerts, and a wide-range cuff fitting upper arms up to 42 cm.",
                "specifications": {
                    "Measurement Range": "Pressure: 0-299 mmHg | Pulse: 40-180 bpm",
                    "Cuff Size": "22 cm - 42 cm (Comfort-fit)",
                    "Memory": "Dual user x 90 memory slots with date & time",
                    "Power": "4x AA batteries or Type-C DC input"
                }
            },
            {
                "pillar_type": "MEDICAL",
                "name": "Finger-Clip OLED Pulse Oximeter & Perfusion Index Meter",
                "sku": "WFH-MED-002",
                "price_ghs": Decimal("350.00"),
                "stock_quantity": 40,
                "is_featured": False,
                "description": "Instant blood oxygen saturation (SpO2) and pulse rate monitor with multi-directional high-contrast OLED display.",
                "specifications": {
                    "SpO2 Range": "70% - 100% (+/- 2% accuracy)",
                    "Features": "Perfusion Index (PI) indicator + Plethysmograph wave",
                    "Auto-off": "Powers down after 8 seconds of finger removal"
                }
            },

            # Pillar 6: DEPOSITORY
            {
                "pillar_type": "DEPOSITORY",
                "name": "Biometric Fire & Water-Resistant Family Document Vault",
                "sku": "WFH-DEP-001",
                "price_ghs": Decimal("3400.00"),
                "stock_quantity": 10,
                "is_featured": True,
                "description": "High-security home archival safe engineered for legal title deeds, family wills, indenture papers, birth records, and backup hard drives.",
                "specifications": {
                    "Locking Mechanism": "Optical biometric sensor (up to 30 prints) + emergency keypad",
                    "Fire Rating": "UL Classified for 60 minutes at 927°C",
                    "Water Resistance": "ETL verified up to 20 cm for 24 hours",
                    "Capacity": "22.8 Liters with adjustable interior organizing shelf"
                }
            },
            {
                "pillar_type": "DEPOSITORY",
                "name": "Emergency Medical Alert RFID Bracelet & Encrypted USB Dossier",
                "sku": "WFH-DEP-002",
                "price_ghs": Decimal("420.00"),
                "stock_quantity": 50,
                "is_featured": False,
                "description": "Wearable emergency responder ID pairing an engraved stainless RFID tag with an encrypted waterproof micro-drive containing blood type, allergies, and family contact details.",
                "specifications": {
                    "Band Material": "Hypoallergenic medical-grade silicone",
                    "Plate": "Laser-etched emergency caduceus emblem",
                    "Storage": "32GB hardware-encrypted emergency partition",
                    "Compatibility": "Universal plug-and-play across Windows/Mac/Android"
                }
            },

            # Pillar 7: SUPPLEMENTS
            {
                "pillar_type": "SUPPLEMENTS",
                "name": "Senior Vitality Joint & Cartilage Support (Glucosamine + MSM + Boswellia)",
                "sku": "WFH-SUPP-001",
                "price_ghs": Decimal("520.00"),
                "stock_quantity": 45,
                "is_featured": True,
                "description": "Targeted anti-inflammatory formulation to relieve joint stiffness, support cartilage regeneration, and improve morning mobility in aging knees and hips.",
                "specifications": {
                    "Active Potency": "Glucosamine HCl 1500mg, Chondroitin 1200mg, MSM 1000mg",
                    "Count": "120 easy-to-swallow coated caplets (60-day supply)",
                    "Safety": "Third-party tested, free of heavy metals and artificial binders"
                }
            },
            {
                "pillar_type": "SUPPLEMENTS",
                "name": "Therapeutic High-Protein Recovery Powder (Micronutrient Enriched)",
                "sku": "WFH-SUPP-002",
                "price_ghs": Decimal("680.00"),
                "stock_quantity": 30,
                "is_featured": False,
                "description": "Easily digestible protein supplement formulated to fight age-related muscle loss (sarcopenia) and support post-surgery convalescence.",
                "specifications": {
                    "Protein Source": "Hydrolyzed Whey + Micellar Casein (24g per serving)",
                    "Fortification": "Vitamin D3, Calcium Citrate, B-Complex, Zinc",
                    "Flavor": "Mild Natural Vanilla (No refined sugars added)",
                    "Weight": "900 g tub"
                }
            },
        ]

        created_count = 0
        updated_count = 0

        for item in products_data:
            try:
                category = Category.objects.get(pillar_type=item["pillar_type"])
            except Category.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f"Category with pillar_type '{item['pillar_type']}' not found. Run seed_pillars first.")
                )
                continue

            product, created = Product.objects.update_or_create(
                sku=item["sku"],
                defaults={
                    "category": category,
                    "name": item["name"],
                    "price_ghs": item["price_ghs"],
                    "stock_quantity": item["stock_quantity"],
                    "is_featured": item["is_featured"],
                    "description": item["description"],
                    "specifications": item["specifications"],
                    "is_active": True,
                }
            )

            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"+ Created Product: {product.name} (GHS {product.price_ghs})"))
            else:
                updated_count += 1
                self.stdout.write(self.style.WARNING(f"= Synced Product: {product.name}"))

        self.stdout.write(
            self.style.SUCCESS(
                f"\nProduct seeding complete. {created_count} created, {updated_count} synced."
            )
        )