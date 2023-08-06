# -*- encoding: utf-8 -*-
"""
A list real vehicle manufacturers.

**Usage:**

::

    from liar.iamaliar import IAmALiar
    number_records = 10
    maker = IAmALiar(number_records)

    # Use:
    from liar.model.raw import transport_raw

    # Or from scratch:
    transport_raw = {
        'name': 'academic_raw',
        'class': 'igetraw',
        'data': 'transport',
    }

    data_set = maker.get_data([transport_raw])

    for row in data_set:
        data = Model()
        data.make = row['transport_raw']['make']
        data.class = row['transport_raw']['class']
        data.img = row['transport_raw']['img']
        data.save()

"""

transport = [
    {"make": "Seat", "class": "Car", "img": "vehiclemanufacturers_car_seat"},
    {"make": "Kia", "class": "Car", "img": "vehiclemanufacturers_car_kia"},
    {"make": "Mazda", "class": "Car", "img": "vehiclemanufacturers_car_mazda"},
    {
        "make": "Aston Martin",
        "class": "Car",
        "img": "vehiclemanufacturers_car_aston_martin",
    },
    {"make": "Riley", "class": "Car", "img": "vehiclemanufacturers_car_riley"},
    {
        "make": "De Tomaso",
        "class": "Car",
        "img": "vehiclemanufacturers_car_de_tomaso",
    },
    {
        "make": "Proton",
        "class": "Car",
        "img": "vehiclemanufacturers_car_proton",
    },
    {
        "make": "Lamborghini",
        "class": "Car",
        "img": "vehiclemanufacturers_car_lamborghini",
    },
    {
        "make": "Cobra",
        "class": "Motorbike",
        "img": "vehiclemanufacturers_motorbike_cobra",
    },
    {"make": "Honda", "class": "Car", "img": "vehiclemanufacturers_car_honda"},
    {
        "make": "Lancia",
        "class": "Car",
        "img": "vehiclemanufacturers_car_lancia",
    },
    {
        "make": "Mitsubishi",
        "class": "Car",
        "img": "vehiclemanufacturers_car_mitsubishi",
    },
    {
        "make": "Renault",
        "class": "Truck",
        "img": "vehiclemanufacturers_truck_renault",
    },
    {
        "make": "Porsche",
        "class": "Car",
        "img": "vehiclemanufacturers_car_porsche",
    },
    {
        "make": "Gulfstream",
        "class": "Airplane",
        "img": "vehiclemanufacturers_airplane_gulfstream",
    },
    {
        "make": "Saab",
        "class": "BusCoach",
        "img": "vehiclemanufacturers_buscoach_saab",
    },
    {
        "make": "Triumph",
        "class": "Motorbike",
        "img": "vehiclemanufacturers_motorbike_triumph",
    },
    {
        "make": "Microcar",
        "class": "Car",
        "img": "vehiclemanufacturers_car_microcar",
    },
    {"make": "Aixam", "class": "Car", "img": "vehiclemanufacturers_car_aixam"},
    {
        "make": "Lincoln",
        "class": "Car",
        "img": "vehiclemanufacturers_car_lincoln",
    },
    {"make": "Isuzu", "class": "Car", "img": "vehiclemanufacturers_car_isuzu"},
    {
        "make": "Daihatsu",
        "class": "Car",
        "img": "vehiclemanufacturers_car_daihatsu",
    },
    {
        "make": "Boeing",
        "class": "Airplane",
        "img": "vehiclemanufacturers_airplane_boeing",
    },
    {
        "make": "Suzuki",
        "class": "Motorbike",
        "img": "vehiclemanufacturers_motorbike_suzuki",
    },
    {
        "make": "Delorean",
        "class": "Car",
        "img": "vehiclemanufacturers_car_delorean",
    },
    {"make": "Noble", "class": "Car", "img": "vehiclemanufacturers_car_noble"},
    {"make": "Skoda", "class": "Car", "img": "vehiclemanufacturers_car_skoda"},
    {
        "make": "Coleman Milne",
        "class": "Car",
        "img": "vehiclemanufacturers_car_coleman_milne",
    },
    {"make": "Audi", "class": "Car", "img": "vehiclemanufacturers_car_audi"},
    {"make": "Ford", "class": "Car", "img": "vehiclemanufacturers_car_ford"},
    {"make": "Smart", "class": "Car", "img": "vehiclemanufacturers_car_smart"},
    {
        "make": "Honda",
        "class": "Motorbike",
        "img": "vehiclemanufacturers_motorbike_honda",
    },
    {
        "make": "Holden",
        "class": "Car",
        "img": "vehiclemanufacturers_car_holden",
    },
    {
        "make": "Yamaha",
        "class": "Motorbike",
        "img": "vehiclemanufacturers_motorbike_yamaha",
    },
    {
        "make": "Land Rover",
        "class": "Car",
        "img": "vehiclemanufacturers_car_land_rover",
    },
    {
        "make": "Rolls-Royce",
        "class": "Car",
        "img": "vehiclemanufacturers_car_rolls_royce",
    },
    {
        "make": "Jensen",
        "class": "Car",
        "img": "vehiclemanufacturers_car_jensen",
    },
    {"make": "Yugo", "class": "Car", "img": "vehiclemanufacturers_car_yugo"},
    {
        "make": "Austin",
        "class": "Car",
        "img": "vehiclemanufacturers_car_austin",
    },
    {
        "make": "McLaren",
        "class": "Car",
        "img": "vehiclemanufacturers_car_mclaren",
    },
    {"make": "GMC", "class": "Car", "img": "vehiclemanufacturers_car_gmc"},
    {
        "make": "Cessna",
        "class": "Airplane",
        "img": "vehiclemanufacturers_airplane_cessna",
    },
    {
        "make": "Marcos",
        "class": "Car",
        "img": "vehiclemanufacturers_car_marcos",
    },
    {
        "make": "Mercedes-Benz",
        "class": "Car",
        "img": "vehiclemanufacturers_car_mercedes_benz",
    },
    {
        "make": "Kawasaki",
        "class": "Motorbike",
        "img": "vehiclemanufacturers_motorbike_kawasaki",
    },
    {
        "make": "Greyhound",
        "class": "BusCoach",
        "img": "vehiclemanufacturers_buscoach_greyhound",
    },
    {
        "make": "Cadillac",
        "class": "Car",
        "img": "vehiclemanufacturers_car_cadillac",
    },
    {"make": "AC", "class": "Car", "img": "vehiclemanufacturers_car_ac"},
    {
        "make": "Husaberg",
        "class": "Motorbike",
        "img": "vehiclemanufacturers_motorbike_husaberg",
    },
    {"make": "Dodge", "class": "Car", "img": "vehiclemanufacturers_car_dodge"},
    {
        "make": "Daihatsu",
        "class": "Truck",
        "img": "vehiclemanufacturers_truck_daihatsu",
    },
    {
        "make": "Noge",
        "class": "BusCoach",
        "img": "vehiclemanufacturers_buscoach_noge",
    },
    {
        "make": "Catepillar",
        "class": "BusCoach",
        "img": "vehiclemanufacturers_buscoach_catepillar",
    },
    {"make": "Rover", "class": "Car", "img": "vehiclemanufacturers_car_rover"},
    {
        "make": "Triumph",
        "class": "Car",
        "img": "vehiclemanufacturers_car_triumph",
    },
    {
        "make": "Alfa Romeo",
        "class": "Car",
        "img": "vehiclemanufacturers_car_alfa_romeo",
    },
    {
        "make": "Daimler",
        "class": "Car",
        "img": "vehiclemanufacturers_car_daimler",
    },
    {
        "make": "Infiniti",
        "class": "Car",
        "img": "vehiclemanufacturers_car_infiniti",
    },
    {
        "make": "Bentley",
        "class": "Car",
        "img": "vehiclemanufacturers_car_bentley",
    },
    {
        "make": "Panther",
        "class": "Car",
        "img": "vehiclemanufacturers_car_panther",
    },
    {"make": "Lexus", "class": "Car", "img": "vehiclemanufacturers_car_lexus"},
    {
        "make": "Airbus",
        "class": "Airplane",
        "img": "vehiclemanufacturers_airplane_airbus",
    },
    {
        "make": "Nissan",
        "class": "Car",
        "img": "vehiclemanufacturers_car_nissan",
    },
    {
        "make": "Singer",
        "class": "Car",
        "img": "vehiclemanufacturers_car_singer",
    },
    {"make": "Mini", "class": "Car", "img": "vehiclemanufacturers_car_mini"},
    {
        "make": "VOR",
        "class": "Motorbike",
        "img": "vehiclemanufacturers_motorbike_vor",
    },
    {"make": "Tata", "class": "Car", "img": "vehiclemanufacturers_car_tata"},
    {"make": "Opel", "class": "Car", "img": "vehiclemanufacturers_car_opel"},
    {
        "make": "Mitsuoka",
        "class": "Car",
        "img": "vehiclemanufacturers_car_mitsuoka",
    },
    {
        "make": "Corvette",
        "class": "Car",
        "img": "vehiclemanufacturers_car_corvette",
    },
    {
        "make": "Iveco",
        "class": "Truck",
        "img": "vehiclemanufacturers_truck_iveco",
    },
    {
        "make": "Caterham",
        "class": "Car",
        "img": "vehiclemanufacturers_car_caterham",
    },
    {
        "make": "Renault",
        "class": "Car",
        "img": "vehiclemanufacturers_car_renault",
    },
    {
        "make": "Chevrolet",
        "class": "Car",
        "img": "vehiclemanufacturers_car_chevrolet",
    },
    {
        "make": "Scania",
        "class": "Truck",
        "img": "vehiclemanufacturers_truck_scania",
    },
    {
        "make": "Isuzu",
        "class": "Truck",
        "img": "vehiclemanufacturers_truck_isuzu",
    },
    {
        "make": "Mercury",
        "class": "Car",
        "img": "vehiclemanufacturers_car_mercury",
    },
    {
        "make": "Citroen",
        "class": "Car",
        "img": "vehiclemanufacturers_car_citroen",
    },
    {
        "make": "Koenigsegg",
        "class": "Car",
        "img": "vehiclemanufacturers_car_koenigsegg",
    },
    {
        "make": "Pagani",
        "class": "Car",
        "img": "vehiclemanufacturers_car_pagani",
    },
    {"make": "Man", "class": "Truck", "img": "vehiclemanufacturers_truck_man"},
    {
        "make": "Daewoo",
        "class": "Car",
        "img": "vehiclemanufacturers_car_daewoo",
    },
    {
        "make": "Wolseley",
        "class": "Car",
        "img": "vehiclemanufacturers_car_wolseley",
    },
    {
        "make": "Antonov",
        "class": "Airplane",
        "img": "vehiclemanufacturers_airplane_antonov",
    },
    {
        "make": "Ferrari",
        "class": "Car",
        "img": "vehiclemanufacturers_car_ferrari",
    },
    {
        "make": "Irisbus",
        "class": "BusCoach",
        "img": "vehiclemanufacturers_buscoach_irisbus",
    },
    {
        "make": "Motor Coach Industries",
        "class": "BusCoach",
        "img": "vehiclemanufacturers_buscoach_motor_coach_industries",
    },
    {
        "make": "Reliant",
        "class": "Car",
        "img": "vehiclemanufacturers_car_reliant",
    },
    {
        "make": "Morris",
        "class": "Car",
        "img": "vehiclemanufacturers_car_morris",
    },
    {
        "make": "General Motors",
        "class": "Car",
        "img": "vehiclemanufacturers_car_general_motors",
    },
    {
        "make": "Pontiac",
        "class": "Car",
        "img": "vehiclemanufacturers_car_pontiac",
    },
    {
        "make": "Ssangyong",
        "class": "Car",
        "img": "vehiclemanufacturers_car_ssangyong",
    },
    {
        "make": "Scandus",
        "class": "BusCoach",
        "img": "vehiclemanufacturers_buscoach_scandus",
    },
    {
        "make": "Subaru",
        "class": "Car",
        "img": "vehiclemanufacturers_car_subaru",
    },
    {
        "make": "Maserati",
        "class": "Car",
        "img": "vehiclemanufacturers_car_maserati",
    },
    {"make": "Lada", "class": "Car", "img": "vehiclemanufacturers_car_lada"},
    {
        "make": "Lockheed Martin",
        "class": "Airplane",
        "img": "vehiclemanufacturers_airplane_lockheed_martin",
    },
    {
        "make": "Chrysler",
        "class": "Car",
        "img": "vehiclemanufacturers_car_chrysler",
    },
    {
        "make": "Mack",
        "class": "Truck",
        "img": "vehiclemanufacturers_truck_mack",
    },
    {"make": "TVR", "class": "Car", "img": "vehiclemanufacturers_car_tvr"},
    {
        "make": "Fantic",
        "class": "Motorbike",
        "img": "vehiclemanufacturers_motorbike_fantic",
    },
    {
        "make": "Mahindra",
        "class": "Car",
        "img": "vehiclemanufacturers_car_mahindra",
    },
    {"make": "MG", "class": "Car", "img": "vehiclemanufacturers_car_mg"},
    {
        "make": "Suzuki",
        "class": "Car",
        "img": "vehiclemanufacturers_car_suzuki",
    },
    {
        "make": "General Motors",
        "class": "BusCoach",
        "img": "vehiclemanufacturers_buscoach_general_motors",
    },
    {
        "make": "Toyota",
        "class": "Car",
        "img": "vehiclemanufacturers_car_toyota",
    },
    {
        "make": "Peugeot",
        "class": "Car",
        "img": "vehiclemanufacturers_car_peugeot",
    },
    {
        "make": "Jaguar",
        "class": "Car",
        "img": "vehiclemanufacturers_car_jaguar",
    },
    {
        "make": "Blaney",
        "class": "Motorbike",
        "img": "vehiclemanufacturers_motorbike_blaney",
    },
    {
        "make": "Mercedes-Benz",
        "class": "BusCoach",
        "img": "vehiclemanufacturers_buscoach_mercedes_benz",
    },
    {
        "make": "Aprilia",
        "class": "Motorbike",
        "img": "vehiclemanufacturers_motorbike_aprilla",
    },
    {
        "make": "Volkswagen",
        "class": "Truck",
        "img": "vehiclemanufacturers_truck_volkswagen",
    },
    {
        "make": "Volkswagen",
        "class": "Car",
        "img": "vehiclemanufacturers_car_volkswagen",
    },
    {"make": "Saab", "class": "Car", "img": "vehiclemanufacturers_car_saab"},
    {
        "make": "Vauxhall",
        "class": "Car",
        "img": "vehiclemanufacturers_car_vauxhall",
    },
    {
        "make": "Maybach",
        "class": "Car",
        "img": "vehiclemanufacturers_car_maybach",
    },
    {
        "make": "Ligier",
        "class": "Car",
        "img": "vehiclemanufacturers_car_ligier",
    },
    {
        "make": "Westfield",
        "class": "Car",
        "img": "vehiclemanufacturers_car_westfield",
    },
    {"make": "Gaz", "class": "Truck", "img": "vehiclemanufacturers_truck_gaz"},
    {"make": "BMW", "class": "Car", "img": "vehiclemanufacturers_car_bmw"},
    {
        "make": "Ultima",
        "class": "Car",
        "img": "vehiclemanufacturers_car_ultima",
    },
    {"make": "Jeep", "class": "Car", "img": "vehiclemanufacturers_car_jeep"},
    {
        "make": "Pilgrim",
        "class": "Car",
        "img": "vehiclemanufacturers_car_pilgrim",
    },
    {
        "make": "Bristol",
        "class": "Car",
        "img": "vehiclemanufacturers_car_bristol",
    },
    {
        "make": "Morgan",
        "class": "Car",
        "img": "vehiclemanufacturers_car_morgan",
    },
    {
        "make": "Nabi",
        "class": "BusCoach",
        "img": "vehiclemanufacturers_buscoach_nabi",
    },
    {"make": "Daf", "class": "Truck", "img": "vehiclemanufacturers_truck_daf"},
    {"make": "Volvo", "class": "Car", "img": "vehiclemanufacturers_car_volvo"},
    {
        "make": "BSA",
        "class": "Motorbike",
        "img": "vehiclemanufacturers_motorbike_bsa",
    },
    {
        "make": "Ford",
        "class": "Motorbike",
        "img": "vehiclemanufacturers_motorbike_ford",
    },
    {"make": "Lotus", "class": "Car", "img": "vehiclemanufacturers_car_lotus"},
    {
        "make": "Perodua",
        "class": "Car",
        "img": "vehiclemanufacturers_car_perodua",
    },
    {
        "make": "Hyundai",
        "class": "Car",
        "img": "vehiclemanufacturers_car_hyundai",
    },
    {
        "make": "Gas Gas",
        "class": "Motorbike",
        "img": "vehiclemanufacturers_motorbike_gas_gas",
    },
    {"make": "Fiat", "class": "Car", "img": "vehiclemanufacturers_car_fiat"},
]
