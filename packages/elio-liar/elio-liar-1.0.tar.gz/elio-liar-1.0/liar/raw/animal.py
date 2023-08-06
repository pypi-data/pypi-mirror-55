# -*- encoding: utf-8 -*-
"""
The data is a compiled list of well known animal, insect and plant names,
each classified (Mammal, Reptile, Plant, Bug, etc) and a 200x240px or
240x200px image from the public domain.

**Usage:**

::

    from liar.iamaliar import IAmALiar
    number_records = 10
    maker = IAmALiar(number_records)

    # Use:
    from liar.model.raw import animal_raw

    # Or from scratch:
    animal_raw = {
        'name': 'animal_raw',
        'class': 'igetraw',
        'data': 'animal',
    }

    data_set = maker.get_data([animal_suffix_raw])

    for row in data_set:
        data = Model()
        data.animal = row['animal_raw']['animal']
        data.classification = row['animal_raw']['classification']
        data.drawing = row['animal_raw']['images']['drawing']
        data.save()

Animal images are stored in "liar/liar/rawimages/animals/<img>.gif"

If you only need the animal name, use the property option:

::

    # Use:
    from liar.model.raw import animal_name_raw

    # Or from scratch:
    animal_name_raw = {
        'name': 'animal_name_raw',
        'class': 'igetraw',
        'data': 'animal',
        'property': 'animal'
    }

    data_set = maker.get_data([animal_name_raw])

    for row in data_set:
        data = Model()
        data.animal_name = row['animal_name_raw']
        data.save()

"""

animal = [
    {
        "animal": "oar fish",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_oar_fish.gif"},
    },
    {
        "animal": "pohutukawa",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_pohutukawa.gif"},
    },
    {
        "animal": "mulberry",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_mulberry.gif"},
    },
    {
        "animal": "lovebird",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_lovebird.gif"},
    },
    {
        "animal": "puku",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_puku.gif"},
    },
    {
        "animal": "beech",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_beech.gif"},
    },
    {
        "animal": "falcon",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_falcon.gif"},
    },
    {
        "animal": "toucan",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_toucan.gif"},
    },
    {
        "animal": "tapir",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_tapir.gif"},
    },
    {
        "animal": "chestnut",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_chestnut.gif"},
    },
    {
        "animal": "friar bird",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_friar_bird.gif"},
    },
    {
        "animal": "rose",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_rose.gif"},
    },
    {
        "animal": "spiraea",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_spiraea.gif"},
    },
    {
        "animal": "muskallunge",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_muskallunge.gif"},
    },
    {
        "animal": "porgy",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_porgy.gif"},
    },
    {
        "animal": "mangrove",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_mangrove.gif"},
    },
    {
        "animal": "roller",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_roller.gif"},
    },
    {
        "animal": "mole",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_mole.gif"},
    },
    {
        "animal": "yarrow",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_yarrow.gif"},
    },
    {
        "animal": "porcupine fish",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_porcupine_fish.gif"},
    },
    {
        "animal": "flying dragon",
        "classification": "reptile",
        "images": {
            "drawing": "images/animal/animals_reptile_flying_dragon.gif"
        },
    },
    {
        "animal": "hazel",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_hazel.gif"},
    },
    {
        "animal": "borer",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_borer.gif"},
    },
    {
        "animal": "poditti",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_poditti.gif"},
    },
    {
        "animal": "moccasin flower",
        "classification": "plant",
        "images": {
            "drawing": "images/animal/animals_plant_moccasin_flower.gif"
        },
    },
    {
        "animal": "agouti",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_agouti.gif"},
    },
    {
        "animal": "lizard's tail",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_lizard_s_tail.gif"},
    },
    {
        "animal": "olive",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_olive.gif"},
    },
    {
        "animal": "wattle bird",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_wattle_bird.gif"},
    },
    {
        "animal": "gnu",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_gnu.gif"},
    },
    {
        "animal": "dziggetai",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_dziggetai.gif"},
    },
    {
        "animal": "catnip",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_catnip.gif"},
    },
    {
        "animal": "mignonette",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_mignonette.gif"},
    },
    {
        "animal": "lorikeet",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_lorikeet.gif"},
    },
    {
        "animal": "nelumbo",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_nelumbo.gif"},
    },
    {
        "animal": "scallop",
        "classification": "invertebrate",
        "images": {"drawing": "images/animal/animals_invertebrate_scallop.gif"},
    },
    {
        "animal": "grasshopper",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_grasshopper.gif"},
    },
    {
        "animal": "arenia",
        "classification": "invertebrate",
        "images": {"drawing": "images/animal/animals_invertebrate_arenia.gif"},
    },
    {
        "animal": "gerbil",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_gerbil.gif"},
    },
    {
        "animal": "terrapin",
        "classification": "reptile",
        "images": {"drawing": "images/animal/animals_reptile_terrapin.gif"},
    },
    {
        "animal": "rattlesnake",
        "classification": "reptile",
        "images": {"drawing": "images/animal/animals_reptile_rattlesnake.gif"},
    },
    {
        "animal": "hog",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_hog.gif"},
    },
    {
        "animal": "cockscomb",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_cockscomb.gif"},
    },
    {
        "animal": "trout",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_trout.gif"},
    },
    {
        "animal": "atlas",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_atlas.gif"},
    },
    {
        "animal": "armadillo",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_armadillo.gif"},
    },
    {
        "animal": "klipspringer",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_klipspringer.gif"},
    },
    {
        "animal": "ptarmigan",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_ptarmigan.gif"},
    },
    {
        "animal": "elephant",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_elephant.gif"},
    },
    {
        "animal": "nidularia",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_nidularia.gif"},
    },
    {
        "animal": "cavy",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_cavy.gif"},
    },
    {
        "animal": "globefish",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_globefish.gif"},
    },
    {
        "animal": "jiboa",
        "classification": "reptile",
        "images": {"drawing": "images/animal/animals_reptile_jiboa.gif"},
    },
    {
        "animal": "foxglove",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_foxglove.gif"},
    },
    {
        "animal": "tea tree",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_tea_tree.gif"},
    },
    {
        "animal": "weaver bird",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_weaver_bird.gif"},
    },
    {
        "animal": "cephalotus",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_cephalotus.gif"},
    },
    {
        "animal": "coco palm",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_coco_palm.gif"},
    },
    {
        "animal": "festuca",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_festuca.gif"},
    },
    {
        "animal": "okapi",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_okapi.gif"},
    },
    {
        "animal": "elm",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_elm.gif"},
    },
    {
        "animal": "ass",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_ass.gif"},
    },
    {
        "animal": "polecat",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_polecat.gif"},
    },
    {
        "animal": "shooting fish",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_shooting_fish.gif"},
    },
    {
        "animal": "mariposa",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_mariposa.gif"},
    },
    {
        "animal": "termite",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_termite.gif"},
    },
    {
        "animal": "sassafras",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_sassafras.gif"},
    },
    {
        "animal": "merlin",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_merlin.gif"},
    },
    {
        "animal": "racoon",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_racoon.gif"},
    },
    {
        "animal": "manakin",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_manakin.gif"},
    },
    {
        "animal": "lemming",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_lemming.gif"},
    },
    {
        "animal": "fly",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_fly.gif"},
    },
    {
        "animal": "dandelion",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_dandelion.gif"},
    },
    {
        "animal": "callitrix",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_callitrix.gif"},
    },
    {
        "animal": "baobab",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_baobab.gif"},
    },
    {
        "animal": "hare",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_hare.gif"},
    },
    {
        "animal": "catfish",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_catfish.gif"},
    },
    {
        "animal": "tobacco plant",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_tobacco_plant.gif"},
    },
    {
        "animal": "nightjar",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_nightjar.gif"},
    },
    {
        "animal": "earthworm",
        "classification": "invertebrate",
        "images": {
            "drawing": "images/animal/animals_invertebrate_earthworm.gif"
        },
    },
    {
        "animal": "sea elephant",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_sea_elephant.gif"},
    },
    {
        "animal": "papyrus",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_papyrus.gif"},
    },
    {
        "animal": "sugar beet",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_sugar_beet.gif"},
    },
    {
        "animal": "grackle",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_grackle.gif"},
    },
    {
        "animal": "parnassia",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_parnassia.gif"},
    },
    {
        "animal": "cowpea",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_cowpea.gif"},
    },
    {
        "animal": "camomile",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_camomile.gif"},
    },
    {
        "animal": "kite",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_kite.gif"},
    },
    {
        "animal": "sloth",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_sloth.gif"},
    },
    {
        "animal": "plantain",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_plantain.gif"},
    },
    {
        "animal": "pentstemon",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_pentstemon.gif"},
    },
    {
        "animal": "wombat",
        "classification": "marsupial",
        "images": {"drawing": "images/animal/animals_marsupial_wombat.gif"},
    },
    {
        "animal": "capibara",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_capibara.gif"},
    },
    {
        "animal": "aconite",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_aconite.gif"},
    },
    {
        "animal": "cashew branch",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_cashew_branch.gif"},
    },
    {
        "animal": "saxifrage",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_saxifrage.gif"},
    },
    {
        "animal": "lion",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_lion.gif"},
    },
    {
        "animal": "honey ant",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_honey_ant.gif"},
    },
    {
        "animal": "brass bass",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_brass_bass.gif"},
    },
    {
        "animal": "kiwi",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_kiwi.gif"},
    },
    {
        "animal": "aardwolf",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_aardwolf.gif"},
    },
    {
        "animal": "spoonbill",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_spoonbill.gif"},
    },
    {
        "animal": "banana",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_banana.gif"},
    },
    {
        "animal": "sheep laurel",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_sheep_laurel.gif"},
    },
    {
        "animal": "lark plover",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_lark_plover.gif"},
    },
    {
        "animal": "yew",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_yew.gif"},
    },
    {
        "animal": "sunfish",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_sunfish.gif"},
    },
    {
        "animal": "dove",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_dove.gif"},
    },
    {
        "animal": "ermine",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_ermine.gif"},
    },
    {
        "animal": "pickerel weed",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_pickerel_weed.gif"},
    },
    {
        "animal": "rice",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_rice.gif"},
    },
    {
        "animal": "paca",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_paca.gif"},
    },
    {
        "animal": "bandicoot",
        "classification": "marsupial",
        "images": {"drawing": "images/animal/animals_marsupial_bandicoot.gif"},
    },
    {
        "animal": "mountain laurel",
        "classification": "plant",
        "images": {
            "drawing": "images/animal/animals_plant_mountain_laurel.gif"
        },
    },
    {
        "animal": "cony",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_cony.gif"},
    },
    {
        "animal": "usnea",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_usnea.gif"},
    },
    {
        "animal": "drone beetle",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_drone_beetle.gif"},
    },
    {
        "animal": "kudu",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_kudu.gif"},
    },
    {
        "animal": "ferret",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_ferret.gif"},
    },
    {
        "animal": "adiantum",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_adiantum.gif"},
    },
    {
        "animal": "hummingbird",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_hummingbird.gif"},
    },
    {
        "animal": "gander",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_gander.gif"},
    },
    {
        "animal": "mud dauber",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_mud_dauber.gif"},
    },
    {
        "animal": "barbet",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_barbet.gif"},
    },
    {
        "animal": "addax",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_addax.gif"},
    },
    {
        "animal": "squacco",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_squacco.gif"},
    },
    {
        "animal": "cicada",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_cicada.gif"},
    },
    {
        "animal": "hawthorn",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_hawthorn.gif"},
    },
    {
        "animal": "diver",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_diver.gif"},
    },
    {
        "animal": "cacao",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_cacao.gif"},
    },
    {
        "animal": "caracara",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_caracara.gif"},
    },
    {
        "animal": "piculet",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_piculet.gif"},
    },
    {
        "animal": "cyclamen",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_cyclamen.gif"},
    },
    {
        "animal": "ptolemy",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_ptolemy.gif"},
    },
    {
        "animal": "manatee",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_manatee.gif"},
    },
    {
        "animal": "tananger",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_tananger.gif"},
    },
    {
        "animal": "datura",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_datura.gif"},
    },
    {
        "animal": "leopard",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_cloud_leopard.gif"},
    },
    {
        "animal": "coypu",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_coypu.gif"},
    },
    {
        "animal": "herring",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_herring.gif"},
    },
    {
        "animal": "salamander",
        "classification": "amphibian",
        "images": {
            "drawing": "images/animal/animals_amphibian_spotted_salamander.gif"
        },
    },
    {
        "animal": "python",
        "classification": "reptile",
        "images": {"drawing": "images/animal/animals_reptile_python.gif"},
    },
    {
        "animal": "coot",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_coot.gif"},
    },
    {
        "animal": "painted snipe",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_painted_snipe.gif"},
    },
    {
        "animal": "bedbug",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_bedbug.gif"},
    },
    {
        "animal": "goatsucker",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_goatsucker.gif"},
    },
    {
        "animal": "dolphin",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_dolphin.gif"},
    },
    {
        "animal": "chinchilla",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_chinchilla.gif"},
    },
    {
        "animal": "shrimp",
        "classification": "invertebrate",
        "images": {"drawing": "images/animal/animals_invertebrate_shrimp.gif"},
    },
    {
        "animal": "house fly",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_house_fly.gif"},
    },
    {
        "animal": "cow",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_cow.gif"},
    },
    {
        "animal": "warbler",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_warbler.gif"},
    },
    {
        "animal": "earwig",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_earwig.gif"},
    },
    {
        "animal": "vanilla",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_vanilla.gif"},
    },
    {
        "animal": "deer",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_deer.gif"},
    },
    {
        "animal": "pin borer",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_pin_borer.gif"},
    },
    {
        "animal": "shad",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_shad.gif"},
    },
    {
        "animal": "steppe fowl",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_steppe_fowl.gif"},
    },
    {
        "animal": "snake",
        "classification": "reptile",
        "images": {"drawing": "images/animal/animals_reptile_snake.gif"},
    },
    {
        "animal": "gelsemium",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_gelsemium.gif"},
    },
    {
        "animal": "muntjak",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_muntjak.gif"},
    },
    {
        "animal": "starling",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_glossy_starling.gif"},
    },
    {
        "animal": "garlic",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_garlic.gif"},
    },
    {
        "animal": "floulder",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_floulder.gif"},
    },
    {
        "animal": "tumboa",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_tumboa.gif"},
    },
    {
        "animal": "trapa",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_trapa.gif"},
    },
    {
        "animal": "boat bill",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_boat_bill.gif"},
    },
    {
        "animal": "ginseng",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_ginseng.gif"},
    },
    {
        "animal": "strawberry pear",
        "classification": "plant",
        "images": {
            "drawing": "images/animal/animals_plant_strawberry_pear.gif"
        },
    },
    {
        "animal": "jacamar",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_jacamar.gif"},
    },
    {
        "animal": "pike",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_pike.gif"},
    },
    {
        "animal": "nutcracker",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_nutcracker.gif"},
    },
    {
        "animal": "dionaea",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_dionaea.gif"},
    },
    {
        "animal": "tutu",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_tutu.gif"},
    },
    {
        "animal": "arbutus",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_arbutus.gif"},
    },
    {
        "animal": "fruit bat",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_fruit_bat.gif"},
    },
    {
        "animal": "mangabey",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_mangabey.gif"},
    },
    {
        "animal": "purple loosestrife",
        "classification": "plant",
        "images": {
            "drawing": "images/animal/animals_plant_purple_loosestrife.gif"
        },
    },
    {
        "animal": "elecampane",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_elecampane.gif"},
    },
    {
        "animal": "escuerzos",
        "classification": "amphibian",
        "images": {"drawing": "images/animal/animals_amphibian_escuerzos.gif"},
    },
    {
        "animal": "eucharis",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_eucharis.gif"},
    },
    {
        "animal": "blenny",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_blenny.gif"},
    },
    {
        "animal": "frog hopper",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_frog_hopper.gif"},
    },
    {
        "animal": "bullfinch",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_bullfinch.gif"},
    },
    {
        "animal": "swallow",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_swallow.gif"},
    },
    {
        "animal": "box elder",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_box_elder.gif"},
    },
    {
        "animal": "ginger",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_ginger.gif"},
    },
    {
        "animal": "teal",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_teal.gif"},
    },
    {
        "animal": "guillemot",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_guillemot.gif"},
    },
    {
        "animal": "bittern",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_bittern.gif"},
    },
    {
        "animal": "heron",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_heron.gif"},
    },
    {
        "animal": "urchin",
        "classification": "invertebrate",
        "images": {"drawing": "images/animal/animals_invertebrate_urchin.gif"},
    },
    {
        "animal": "puffin",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_puffin.gif"},
    },
    {
        "animal": "sparrow",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_sparrow.gif"},
    },
    {
        "animal": "gecko",
        "classification": "reptile",
        "images": {"drawing": "images/animal/animals_reptile_gecko.gif"},
    },
    {
        "animal": "grossbeak",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_grossbeak.gif"},
    },
    {
        "animal": "fringe tree",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_fringe_tree.gif"},
    },
    {
        "animal": "sargassum fish",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_sargassum_fish.gif"},
    },
    {
        "animal": "cosmia",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_cosmia.gif"},
    },
    {
        "animal": "baboon",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_baboon.gif"},
    },
    {
        "animal": "walrus",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_walrus.gif"},
    },
    {
        "animal": "newt",
        "classification": "amphibian",
        "images": {"drawing": "images/animal/animals_amphibian_newt.gif"},
    },
    {
        "animal": "hammerhead",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_hammerhead.gif"},
    },
    {
        "animal": "tarsier",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_tarsier.gif"},
    },
    {
        "animal": "turtledove",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_turtledove.gif"},
    },
    {
        "animal": "octopus",
        "classification": "invertebrate",
        "images": {"drawing": "images/animal/animals_invertebrate_octopus.gif"},
    },
    {
        "animal": "crab",
        "classification": "invertebrate",
        "images": {"drawing": "images/animal/animals_invertebrate_crab.gif"},
    },
    {
        "animal": "trogapan",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_trogapan.gif"},
    },
    {
        "animal": "goshawk",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_goshawk.gif"},
    },
    {
        "animal": "fir",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_fir.gif"},
    },
    {
        "animal": "perch",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_perch.gif"},
    },
    {
        "animal": "lynx",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_lynx.gif"},
    },
    {
        "animal": "poison ivy",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_poison_ivy.gif"},
    },
    {
        "animal": "zebra",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_zebra.gif"},
    },
    {
        "animal": "roach",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_roach2.gif"},
    },
    {
        "animal": "chameleon",
        "classification": "reptile",
        "images": {"drawing": "images/animal/animals_reptile_chameleon.gif"},
    },
    {
        "animal": "grizzley",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_grizzley.gif"},
    },
    {
        "animal": "snipe",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_snipe.gif"},
    },
    {
        "animal": "cinchona",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_cinchona.gif"},
    },
    {
        "animal": "parrot",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_parrot.gif"},
    },
    {
        "animal": "dragon fly",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_dragon_fly.gif"},
    },
    {
        "animal": "shrew mouse",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_shrew_mouse.gif"},
    },
    {
        "animal": "albatross",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_albatross.gif"},
    },
    {
        "animal": "cabbage palmetto",
        "classification": "plant",
        "images": {
            "drawing": "images/animal/animals_plant_cabbage_palmetto.gif"
        },
    },
    {
        "animal": "mandrill",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_mandrill.gif"},
    },
    {
        "animal": "ash",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_ash.gif"},
    },
    {
        "animal": "tulip",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_tulip.gif"},
    },
    {
        "animal": "bat",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_bat.gif"},
    },
    {
        "animal": "ruff",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_ruff.gif"},
    },
    {
        "animal": "climbing fish",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_climbing_fish.gif"},
    },
    {
        "animal": "butternut",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_butternut.gif"},
    },
    {
        "animal": "ouzel",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_ouzel.gif"},
    },
    {
        "animal": "sago palm",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_sago_palm.gif"},
    },
    {
        "animal": "tamarin",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_tamarin.gif"},
    },
    {
        "animal": "teak",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_teak.gif"},
    },
    {
        "animal": "jack in the pulpit",
        "classification": "plant",
        "images": {
            "drawing": "images/animal/animals_plant_jack_in_the_pulpit.gif"
        },
    },
    {
        "animal": "hippopotamus",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_hippopotamus.gif"},
    },
    {
        "animal": "bear",
        "classification": "mammal",
        "images": {
            "drawing": "images/animal/animals_mammal_spectacled_bear.gif"
        },
    },
    {
        "animal": "bottle gourds",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_bottle_gourds.gif"},
    },
    {
        "animal": "medlar",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_medlar.gif"},
    },
    {
        "animal": "adder",
        "classification": "reptile",
        "images": {"drawing": "images/animal/animals_reptile_adder.gif"},
    },
    {
        "animal": "porpoise",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_porpoise.gif"},
    },
    {
        "animal": "brazil nut",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_brazil_nut.gif"},
    },
    {
        "animal": "sculpin",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_sculpin.gif"},
    },
    {
        "animal": "pelican",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_pelican.gif"},
    },
    {
        "animal": "wheat",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_wheat.gif"},
    },
    {
        "animal": "staghorn fern",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_staghorn_fern.gif"},
    },
    {
        "animal": "sabella",
        "classification": "invertebrate",
        "images": {"drawing": "images/animal/animals_invertebrate_sabella.gif"},
    },
    {
        "animal": "swan",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_swan.gif"},
    },
    {
        "animal": "golden wattle",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_golden_wattle.gif"},
    },
    {
        "animal": "teasel",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_teasel.gif"},
    },
    {
        "animal": "rhea",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_rhea.gif"},
    },
    {
        "animal": "bream",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_bream.gif"},
    },
    {
        "animal": "larkspur",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_larkspur.gif"},
    },
    {
        "animal": "partridge berry",
        "classification": "plant",
        "images": {
            "drawing": "images/animal/animals_plant_partridge_berry.gif"
        },
    },
    {
        "animal": "bamboo",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_bamboo.gif"},
    },
    {
        "animal": "coati",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_coati.gif"},
    },
    {
        "animal": "frog",
        "classification": "amphibian",
        "images": {
            "drawing": "images/animal/animals_amphibian_flying_frog.gif"
        },
    },
    {
        "animal": "gotwit",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_gotwit.gif"},
    },
    {
        "animal": "marmoset",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_marmoset.gif"},
    },
    {
        "animal": "honeysuckle",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_honeysuckle.gif"},
    },
    {
        "animal": "madder",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_madder.gif"},
    },
    {
        "animal": "geebung",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_geebung.gif"},
    },
    {
        "animal": "halibut",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_halibut.gif"},
    },
    {
        "animal": "sea cucumber",
        "classification": "invertebrate",
        "images": {
            "drawing": "images/animal/animals_invertebrate_sea_cucumber.gif"
        },
    },
    {
        "animal": "bumble bee",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_bumble_bee.gif"},
    },
    {
        "animal": "mullet",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_mullet.gif"},
    },
    {
        "animal": "bird of paradise",
        "classification": "bird",
        "images": {
            "drawing": "images/animal/animals_bird_bird_of_paradise.gif"
        },
    },
    {
        "animal": "ophioglossum",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_ophioglossum.gif"},
    },
    {
        "animal": "pangolin",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_pangolin.gif"},
    },
    {
        "animal": "basilisk",
        "classification": "reptile",
        "images": {"drawing": "images/animal/animals_reptile_basilisk.gif"},
    },
    {
        "animal": "tesera",
        "classification": "invertebrate",
        "images": {"drawing": "images/animal/animals_invertebrate_tesera.gif"},
    },
    {
        "animal": "squirrel",
        "classification": "mammal",
        "images": {
            "drawing": "images/animal/animals_mammal_flying_squirrel.gif"
        },
    },
    {
        "animal": "locust",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_locust2.gif"},
    },
    {
        "animal": "tench",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_tench.gif"},
    },
    {
        "animal": "angler fish",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_angler_fish.gif"},
    },
    {
        "animal": "sheep",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_sheep.gif"},
    },
    {
        "animal": "yellowhammer",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_yellowhammer.gif"},
    },
    {
        "animal": "argonaut",
        "classification": "invertebrate",
        "images": {
            "drawing": "images/animal/animals_invertebrate_argonaut.gif"
        },
    },
    {
        "animal": "swordfish",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_swordfish.gif"},
    },
    {
        "animal": "frog",
        "classification": "amphibian",
        "images": {"drawing": "images/animal/animals_amphibian_frog.gif"},
    },
    {
        "animal": "ostrich",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_ostrich.gif"},
    },
    {
        "animal": "sugar maple",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_sugar_maple.gif"},
    },
    {
        "animal": "saint john's wort",
        "classification": "plant",
        "images": {
            "drawing": "images/animal/animals_plant_saint_john_s_wort.gif"
        },
    },
    {
        "animal": "breadfruit",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_breadfruit.gif"},
    },
    {
        "animal": "chamois",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_chamois.gif"},
    },
    {
        "animal": "mare's tail",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_mare_s_tail.gif"},
    },
    {
        "animal": "moss rose",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_moss_rose.gif"},
    },
    {
        "animal": "bee eater",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_bee_eater.gif"},
    },
    {
        "animal": "echinocactus",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_echinocactus.gif"},
    },
    {
        "animal": "shellfish",
        "classification": "invertebrate",
        "images": {
            "drawing": "images/animal/animals_invertebrate_shellfish.gif"
        },
    },
    {
        "animal": "hemp",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_hemp.gif"},
    },
    {
        "animal": "ram",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_ram.gif"},
    },
    {
        "animal": "wallaby",
        "classification": "marsupial",
        "images": {"drawing": "images/animal/animals_marsupial_wallaby.gif"},
    },
    {
        "animal": "camel wasp",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_camel_wasp.gif"},
    },
    {
        "animal": "katydid",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_katydid.gif"},
    },
    {
        "animal": "echineta",
        "classification": "invertebrate",
        "images": {
            "drawing": "images/animal/animals_invertebrate_echineta.gif"
        },
    },
    {
        "animal": "pasque flower",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_pasque_flower.gif"},
    },
    {
        "animal": "lemur",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_lemur.gif"},
    },
    {
        "animal": "scorpian",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_scorpian.gif"},
    },
    {
        "animal": "curlew",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_curlew.gif"},
    },
    {
        "animal": "columbine",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_columbine.gif"},
    },
    {
        "animal": "chub",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_chub.gif"},
    },
    {
        "animal": "needle bug",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_needle_bug.gif"},
    },
    {
        "animal": "shark",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_shark2.gif"},
    },
    {
        "animal": "paradise fish",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_paradise_fish.gif"},
    },
    {
        "animal": "broadtail",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_broadtail.gif"},
    },
    {
        "animal": "pica",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_pica.gif"},
    },
    {
        "animal": "changa",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_changa.gif"},
    },
    {
        "animal": "touche",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_touche.gif"},
    },
    {
        "animal": "maigre",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_maigre.gif"},
    },
    {
        "animal": "panther",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_panther.gif"},
    },
    {
        "animal": "chough",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_chough.gif"},
    },
    {
        "animal": "seal",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_seal.gif"},
    },
    {
        "animal": "sealion",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_sealion.gif"},
    },
    {
        "animal": "spiderwort",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_spiderwort.gif"},
    },
    {
        "animal": "odontoglossum",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_odontoglossum.gif"},
    },
    {
        "animal": "guineahen",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_guinea_hen.gif"},
    },
    {
        "animal": "wild goat",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_wild_goat.gif"},
    },
    {
        "animal": "goral",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_goral.gif"},
    },
    {
        "animal": "swallowtail",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_swallowtail.gif"},
    },
    {
        "animal": "eggplant",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_eggplant.gif"},
    },
    {
        "animal": "ape",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_barbary_ape.gif"},
    },
    {
        "animal": "monkey",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_monkey.gif"},
    },
    {
        "animal": "beisa",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_beisa.gif"},
    },
    {
        "animal": "spruce",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_spruce.gif"},
    },
    {
        "animal": "wasp",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_wasp.gif"},
    },
    {
        "animal": "myrtle",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_myrtle.gif"},
    },
    {
        "animal": "spider",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_trapdoor_spider.gif"},
    },
    {
        "animal": "ibis",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_ibis.gif"},
    },
    {
        "animal": "sedum",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_sedum.gif"},
    },
    {
        "animal": "canary",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_canary.gif"},
    },
    {
        "animal": "mussell",
        "classification": "invertebrate",
        "images": {"drawing": "images/animal/animals_invertebrate_mussell.gif"},
    },
    {
        "animal": "coffer",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_coffer.gif"},
    },
    {
        "animal": "scup",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_scup.gif"},
    },
    {
        "animal": "chipmunk",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_chipmunk.gif"},
    },
    {
        "animal": "musquash",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_musquash.gif"},
    },
    {
        "animal": "liriodendron",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_liriodendron.gif"},
    },
    {
        "animal": "victoria",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_victoria.gif"},
    },
    {
        "animal": "jackal",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_jackal.gif"},
    },
    {
        "animal": "gannet",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_gannet.gif"},
    },
    {
        "animal": "artichoke",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_artichoke.gif"},
    },
    {
        "animal": "fennec",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_fennec.gif"},
    },
    {
        "animal": "paulownia",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_paulownia.gif"},
    },
    {
        "animal": "goldfinch",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_goldfinch.gif"},
    },
    {
        "animal": "flax",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_flax.gif"},
    },
    {
        "animal": "holly",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_holly.gif"},
    },
    {
        "animal": "centipede",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_centipede.gif"},
    },
    {
        "animal": "stapelia",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_stapelia.gif"},
    },
    {
        "animal": "charr",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_charr.gif"},
    },
    {
        "animal": "waxbill",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_waxbill.gif"},
    },
    {
        "animal": "stilt",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_stilt.gif"},
    },
    {
        "animal": "unicorn fish",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_unicorn_fish.gif"},
    },
    {
        "animal": "marsh marigold",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_marsh_marigold.gif"},
    },
    {
        "animal": "water lily",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_water_lily.gif"},
    },
    {
        "animal": "roach",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_roach.gif"},
    },
    {
        "animal": "fish of paradise",
        "classification": "fish",
        "images": {
            "drawing": "images/animal/animals_fish_fish_of_paradise.gif"
        },
    },
    {
        "animal": "chiff chaff",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_chiff_chaff.gif"},
    },
    {
        "animal": "mistletoe",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_mistletoe.gif"},
    },
    {
        "animal": "tetragona",
        "classification": "invertebrate",
        "images": {
            "drawing": "images/animal/animals_invertebrate_tetragona.gif"
        },
    },
    {
        "animal": "tse tse fly",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_tse_tse_fly.gif"},
    },
    {
        "animal": "shikepoke",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_shikepoke.gif"},
    },
    {
        "animal": "sarracenia",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_sarracenia.gif"},
    },
    {
        "animal": "mandrake",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_mandrake.gif"},
    },
    {
        "animal": "bruang",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_bruang.gif"},
    },
    {
        "animal": "weevil",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_weevil.gif"},
    },
    {
        "animal": "lobelia",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_lobelia.gif"},
    },
    {
        "animal": "cockatiel",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_cockatiel.gif"},
    },
    {
        "animal": "archer fish",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_archer_fish.gif"},
    },
    {
        "animal": "thorncrab",
        "classification": "invertebrate",
        "images": {
            "drawing": "images/animal/animals_invertebrate_thorncrab.gif"
        },
    },
    {
        "animal": "harebell",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_harebell.gif"},
    },
    {
        "animal": "redpoll",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_redpoll.gif"},
    },
    {
        "animal": "fox",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_fox.gif"},
    },
    {
        "animal": "badger",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_badger.gif"},
    },
    {
        "animal": "anoa",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_anoa.gif"},
    },
    {
        "animal": "mangosteen",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_mangosteen.gif"},
    },
    {
        "animal": "yellowwood",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_yellowwood.gif"},
    },
    {
        "animal": "eel",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_eel.gif"},
    },
    {
        "animal": "screamer",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_screamer.gif"},
    },
    {
        "animal": "mallow",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_mallow.gif"},
    },
    {
        "animal": "passion flower",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_passion_flower.gif"},
    },
    {
        "animal": "parson bird",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_parson_bird.gif"},
    },
    {
        "animal": "furze",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_furze.gif"},
    },
    {
        "animal": "heather",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_heather.gif"},
    },
    {
        "animal": "flycatcher",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_flycatcher.gif"},
    },
    {
        "animal": "tumble bug",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_tumble_bug.gif"},
    },
    {
        "animal": "wallcreeper",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_wallcreeper.gif"},
    },
    {
        "animal": "finch",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_finch.gif"},
    },
    {
        "animal": "grouper",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_grouper.gif"},
    },
    {
        "animal": "oxen",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_oxen.gif"},
    },
    {
        "animal": "scooter",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_scooter.gif"},
    },
    {
        "animal": "giraffe",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_giraffe.gif"},
    },
    {
        "animal": "okra",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_okra.gif"},
    },
    {
        "animal": "kangaroo",
        "classification": "marsupial",
        "images": {"drawing": "images/animal/animals_marsupial_kangaroo.gif"},
    },
    {
        "animal": "capparis",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_capparis.gif"},
    },
    {
        "animal": "raspberries",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_raspberries.gif"},
    },
    {
        "animal": "zoril",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_zoril.gif"},
    },
    {
        "animal": "orangutang",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_orangutang.gif"},
    },
    {
        "animal": "blackberry",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_blackberry.gif"},
    },
    {
        "animal": "mackeral",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_mackeral.gif"},
    },
    {
        "animal": "shrew mole",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_shrew_mole.gif"},
    },
    {
        "animal": "lily of the valley",
        "classification": "plant",
        "images": {
            "drawing": "images/animal/animals_plant_lily_of_the_valley.gif"
        },
    },
    {
        "animal": "minnow",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_minnow.gif"},
    },
    {
        "animal": "amphisbaena",
        "classification": "reptile",
        "images": {"drawing": "images/animal/animals_reptile_amphisbaena.gif"},
    },
    {
        "animal": "starnosed mole",
        "classification": "mammal",
        "images": {
            "drawing": "images/animal/animals_mammal_starnosed_mole.gif"
        },
    },
    {
        "animal": "wax palm",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_wax_palm.gif"},
    },
    {
        "animal": "anchovy",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_anchovy.gif"},
    },
    {
        "animal": "opuntia",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_opuntia.gif"},
    },
    {
        "animal": "fly agaric",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_fly_agaric.gif"},
    },
    {
        "animal": "peacock fish",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_peacock_fish.gif"},
    },
    {
        "animal": "blue gum",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_blue_gum.gif"},
    },
    {
        "animal": "gerboa",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_gerboa.gif"},
    },
    {
        "animal": "crossbill",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_crossbill.gif"},
    },
    {
        "animal": "mouse lemur",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_mouse_lemur.gif"},
    },
    {
        "animal": "pinkroot",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_pinkroot.gif"},
    },
    {
        "animal": "kingfisher",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_kingfisher.gif"},
    },
    {
        "animal": "flea",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_flea.gif"},
    },
    {
        "animal": "aloe",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_aloe.gif"},
    },
    {
        "animal": "serval",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_serval.gif"},
    },
    {
        "animal": "silvereye",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_silvereye.gif"},
    },
    {
        "animal": "alligator",
        "classification": "reptile",
        "images": {"drawing": "images/animal/animals_reptile_alligator.gif"},
    },
    {
        "animal": "moth",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_moth.gif"},
    },
    {
        "animal": "euphorbia",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_euphorbia.gif"},
    },
    {
        "animal": "sweet gum",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_sweet_gum.gif"},
    },
    {
        "animal": "tree fern",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_tree_fern.gif"},
    },
    {
        "animal": "kukkaburra",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_kukkaburra.gif"},
    },
    {
        "animal": "scad",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_scad.gif"},
    },
    {
        "animal": "reindeer",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_reindeer.gif"},
    },
    {
        "animal": "mink",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_mink.gif"},
    },
    {
        "animal": "fruit fly",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_fruit_fly.gif"},
    },
    {
        "animal": "leopard",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_snow_leopard.gif"},
    },
    {
        "animal": "malbrouk",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_malbrouk.gif"},
    },
    {
        "animal": "sand hopper",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_sand_hopper.gif"},
    },
    {
        "animal": "pigdeon",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_pigdeon.gif"},
    },
    {
        "animal": "annelid",
        "classification": "invertebrate",
        "images": {"drawing": "images/animal/animals_invertebrate_annelid.gif"},
    },
    {
        "animal": "midge",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_midge.gif"},
    },
    {
        "animal": "blackbird",
        "classification": "bird",
        "images": {
            "drawing": "images/animal/animals_bird_savannah_blackbird.gif"
        },
    },
    {
        "animal": "banksia",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_banksia.gif"},
    },
    {
        "animal": "henbane",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_henbane.gif"},
    },
    {
        "animal": "grouse",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_grouse.gif"},
    },
    {
        "animal": "bittersweet",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_bittersweet.gif"},
    },
    {
        "animal": "blue fin",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_blue_fin.gif"},
    },
    {
        "animal": "caiman",
        "classification": "reptile",
        "images": {"drawing": "images/animal/animals_reptile_caiman.gif"},
    },
    {
        "animal": "horse",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_horse.gif"},
    },
    {
        "animal": "cougar",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_cougar.gif"},
    },
    {
        "animal": "tube worm",
        "classification": "invertebrate",
        "images": {
            "drawing": "images/animal/animals_invertebrate_tube_worm.gif"
        },
    },
    {
        "animal": "chatterer",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_chatterer.gif"},
    },
    {
        "animal": "jay",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_jay.gif"},
    },
    {
        "animal": "bushbuck",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_bushbuck.gif"},
    },
    {
        "animal": "water hemlock",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_water_hemlock.gif"},
    },
    {
        "animal": "eagle",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_eagle.gif"},
    },
    {
        "animal": "pittosporum",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_pittosporum.gif"},
    },
    {
        "animal": "gutta percha",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_gutta_percha.gif"},
    },
    {
        "animal": "tamarind",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_tamarind.gif"},
    },
    {
        "animal": "aadvark",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_aadvark.gif"},
    },
    {
        "animal": "cat",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_cat.gif"},
    },
    {
        "animal": "starfish",
        "classification": "invertebrate",
        "images": {
            "drawing": "images/animal/animals_invertebrate_starfish.gif"
        },
    },
    {
        "animal": "rook",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_rook.gif"},
    },
    {
        "animal": "potto",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_potto.gif"},
    },
    {
        "animal": "quail",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_quail.gif"},
    },
    {
        "animal": "fuchsia",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_fuchsia.gif"},
    },
    {
        "animal": "ivy",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_ivy.gif"},
    },
    {
        "animal": "dormouse",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_dormouse.gif"},
    },
    {
        "animal": "gorrilla",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_gorrilla.gif"},
    },
    {
        "animal": "warmouth",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_warmouth.gif"},
    },
    {
        "animal": "meadowlark",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_meadowlark.gif"},
    },
    {
        "animal": "butterfly plant",
        "classification": "plant",
        "images": {
            "drawing": "images/animal/animals_plant_butterfly_plant.gif"
        },
    },
    {
        "animal": "bush dog",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_bush_dog.gif"},
    },
    {
        "animal": "australian nut",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_australian_nut.gif"},
    },
    {
        "animal": "physalis",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_physalis.gif"},
    },
    {
        "animal": "oncidium",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_oncidium.gif"},
    },
    {
        "animal": "smew",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_smew.gif"},
    },
    {
        "animal": "tortoise",
        "classification": "reptile",
        "images": {"drawing": "images/animal/animals_reptile_box_tortoise.gif"},
    },
    {
        "animal": "hornbill",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_hornbill.gif"},
    },
    {
        "animal": "indian pipe",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_indian_pipe.gif"},
    },
    {
        "animal": "tinamu",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_tinamu.gif"},
    },
    {
        "animal": "phalaenopsis",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_phalaenopsis.gif"},
    },
    {
        "animal": "gouty stem",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_gouty_stem.gif"},
    },
    {
        "animal": "bullhead",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_armed_bullhead.gif"},
    },
    {
        "animal": "horseshoe",
        "classification": "invertebrate",
        "images": {
            "drawing": "images/animal/animals_invertebrate_horseshoe.gif"
        },
    },
    {
        "animal": "wildebeest",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_wildebeest.gif"},
    },
    {
        "animal": "widow bird",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_widow_bird.gif"},
    },
    {
        "animal": "salamander",
        "classification": "amphibian",
        "images": {
            "drawing": "images/animal/animals_amphibian_three_toad_salamander.gif"
        },
    },
    {
        "animal": "sting ray",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_sting_ray.gif"},
    },
    {
        "animal": "tit",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_tit.gif"},
    },
    {
        "animal": "quince",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_quince.gif"},
    },
    {
        "animal": "salmon",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_salmon.gif"},
    },
    {
        "animal": "swift",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_swift.gif"},
    },
    {
        "animal": "gulfweed",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_gulfweed.gif"},
    },
    {
        "animal": "gnat",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_gnat2.gif"},
    },
    {
        "animal": "rat kangaroo",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_rat_kangaroo.gif"},
    },
    {
        "animal": "pheasant",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_pheasant.gif"},
    },
    {
        "animal": "anteater",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_anteater.gif"},
    },
    {
        "animal": "tick",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_tick.gif"},
    },
    {
        "animal": "brisbane box",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_brisbane_box.gif"},
    },
    {
        "animal": "harrier",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_harrier.gif"},
    },
    {
        "animal": "wryneck",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_wryneck.gif"},
    },
    {
        "animal": "pomegranate",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_pomegranate.gif"},
    },
    {
        "animal": "hakea",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_hakea.gif"},
    },
    {
        "animal": "zamia",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_zamia.gif"},
    },
    {
        "animal": "hoopoe",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_hoopoe.gif"},
    },
    {
        "animal": "bluets",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_bluets.gif"},
    },
    {
        "animal": "fluke",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_fluke.gif"},
    },
    {
        "animal": "phreoryctes",
        "classification": "invertebrate",
        "images": {
            "drawing": "images/animal/animals_invertebrate_phreoryctes.gif"
        },
    },
    {
        "animal": "loris",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_loris.gif"},
    },
    {
        "animal": "koala",
        "classification": "marsupial",
        "images": {"drawing": "images/animal/animals_marsupial_koala.gif"},
    },
    {
        "animal": "file fish",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_file_fish.gif"},
    },
    {
        "animal": "turkey",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_turkey.gif"},
    },
    {
        "animal": "saki",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_saki.gif"},
    },
    {
        "animal": "lizard",
        "classification": "reptile",
        "images": {"drawing": "images/animal/animals_reptile_lizard.gif"},
    },
    {
        "animal": "owl",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_owl.gif"},
    },
    {
        "animal": "mango",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_mango.gif"},
    },
    {
        "animal": "rabbit",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_rabbit.gif"},
    },
    {
        "animal": "hercules beetle",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_hercules_beetle.gif"},
    },
    {
        "animal": "oak",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_oak.gif"},
    },
    {
        "animal": "crane",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_crane.gif"},
    },
    {
        "animal": "vulture",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_vulture.gif"},
    },
    {
        "animal": "nuthatch",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_nuthatch.gif"},
    },
    {
        "animal": "wall rue",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_wall_rue.gif"},
    },
    {
        "animal": "jonquil",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_jonquil.gif"},
    },
    {
        "animal": "llama",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_llama.gif"},
    },
    {
        "animal": "shrew",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_shrew.gif"},
    },
    {
        "animal": "pinworm",
        "classification": "invertebrate",
        "images": {"drawing": "images/animal/animals_invertebrate_pinworm.gif"},
    },
    {
        "animal": "tarantula",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_tarantula.gif"},
    },
    {
        "animal": "crow",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_crow.gif"},
    },
    {
        "animal": "sugar cane",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_sugar_cane.gif"},
    },
    {
        "animal": "orange",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_orange.gif"},
    },
    {
        "animal": "waratah",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_waratah.gif"},
    },
    {
        "animal": "bower bird",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_bower_bird.gif"},
    },
    {
        "animal": "dog",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_dog.gif"},
    },
    {
        "animal": "guinea pig",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_guinea_pig.gif"},
    },
    {
        "animal": "skipper",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_skipper.gif"},
    },
    {
        "animal": "fathead",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_fathead.gif"},
    },
    {
        "animal": "saberbill",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_saberbill.gif"},
    },
    {
        "animal": "bluebird",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_bluebird.gif"},
    },
    {
        "animal": "cinnamon",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_cinnamon.gif"},
    },
    {
        "animal": "spider",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_garden_spider.gif"},
    },
    {
        "animal": "turtle",
        "classification": "reptile",
        "images": {"drawing": "images/animal/animals_reptile_turtle.gif"},
    },
    {
        "animal": "budgie",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_budgie.gif"},
    },
    {
        "animal": "sable",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_sable.gif"},
    },
    {
        "animal": "mouse",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_mouse.gif"},
    },
    {
        "animal": "sweet bay",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_sweet_bay.gif"},
    },
    {
        "animal": "oriole",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_oriole.gif"},
    },
    {
        "animal": "oat",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_oat.gif"},
    },
    {
        "animal": "utricularia",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_utricularia.gif"},
    },
    {
        "animal": "plover",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_plover.gif"},
    },
    {
        "animal": "laurel",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_laurel.gif"},
    },
    {
        "animal": "cornus",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_cornus.gif"},
    },
    {
        "animal": "hepatica",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_hepatica.gif"},
    },
    {
        "animal": "otter",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_sea_otter.gif"},
    },
    {
        "animal": "flour mite",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_flour_mite.gif"},
    },
    {
        "animal": "wild oat",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_wild_oat.gif"},
    },
    {
        "animal": "buzzard",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_buzzard.gif"},
    },
    {
        "animal": "hawk",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_hawk.gif"},
    },
    {
        "animal": "uji fly",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_uji_fly.gif"},
    },
    {
        "animal": "pickeral",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_pickeral.gif"},
    },
    {
        "animal": "inca weevil",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_inca_weevil.gif"},
    },
    {
        "animal": "lucern",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_lucern.gif"},
    },
    {
        "animal": "yucca",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_yucca.gif"},
    },
    {
        "animal": "gibbon",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_gibbon.gif"},
    },
    {
        "animal": "owl",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_long_eared_owl.gif"},
    },
    {
        "animal": "carp",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_telescope_carp.gif"},
    },
    {
        "animal": "dog rose",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_dog_rose.gif"},
    },
    {
        "animal": "ground beetle",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_ground_beetle.gif"},
    },
    {
        "animal": "mockingbird",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_mockingbird.gif"},
    },
    {
        "animal": "talapoin",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_talapoin.gif"},
    },
    {
        "animal": "live oak",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_live_oak.gif"},
    },
    {
        "animal": "goat",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_domestic_goat.gif"},
    },
    {
        "animal": "maize",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_maize.gif"},
    },
    {
        "animal": "dulus",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_dulus.gif"},
    },
    {
        "animal": "vole",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_vole.gif"},
    },
    {
        "animal": "hedgehog",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_hedgehog.gif"},
    },
    {
        "animal": "yaupon",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_yaupon.gif"},
    },
    {
        "animal": "cowslip",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_cowslip.gif"},
    },
    {
        "animal": "barberry",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_barberry.gif"},
    },
    {
        "animal": "piraya",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_piraya.gif"},
    },
    {
        "animal": "pike",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_pike2.gif"},
    },
    {
        "animal": "weasel",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_weasel.gif"},
    },
    {
        "animal": "buffalo",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_buffalo.gif"},
    },
    {
        "animal": "cassowary",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_cassowary.gif"},
    },
    {
        "animal": "thrift",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_thrift.gif"},
    },
    {
        "animal": "cow fish",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_cow_fish.gif"},
    },
    {
        "animal": "snail",
        "classification": "invertebrate",
        "images": {"drawing": "images/animal/animals_invertebrate_snail.gif"},
    },
    {
        "animal": "salvinia",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_salvinia.gif"},
    },
    {
        "animal": "grayling",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_grayling.gif"},
    },
    {
        "animal": "japu",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_japu.gif"},
    },
    {
        "animal": "sturgeon",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_sturgeon.gif"},
    },
    {
        "animal": "shamrock",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_shamrock.gif"},
    },
    {
        "animal": "gull",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_gull.gif"},
    },
    {
        "animal": "silver maple",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_silver_maple.gif"},
    },
    {
        "animal": "civet",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_civet.gif"},
    },
    {
        "animal": "tropaeolum",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_tropaeolum.gif"},
    },
    {
        "animal": "fly",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_gouty_legged_fly.gif"},
    },
    {
        "animal": "death cup",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_death_cup.gif"},
    },
    {
        "animal": "hop",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_hop.gif"},
    },
    {
        "animal": "redstart",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_redstart.gif"},
    },
    {
        "animal": "brittle star",
        "classification": "invertebrate",
        "images": {
            "drawing": "images/animal/animals_invertebrate_brittle_star.gif"
        },
    },
    {
        "animal": "bull",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_bull.gif"},
    },
    {
        "animal": "sweetsop",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_sweetsop.gif"},
    },
    {
        "animal": "bear",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_bear.gif"},
    },
    {
        "animal": "scopian",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_scopian.gif"},
    },
    {
        "animal": "lily",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_lily.gif"},
    },
    {
        "animal": "belladonna",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_belladonna.gif"},
    },
    {
        "animal": "jeffersonia",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_jeffersonia.gif"},
    },
    {
        "animal": "sheepshead",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_sheepshead.gif"},
    },
    {
        "animal": "saguin",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_saguin.gif"},
    },
    {
        "animal": "elk",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_elk.gif"},
    },
    {
        "animal": "greenbrier",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_greenbrier.gif"},
    },
    {
        "animal": "opossum",
        "classification": "marsupial",
        "images": {"drawing": "images/animal/animals_marsupial_opossum.gif"},
    },
    {
        "animal": "climbing fern",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_climbing_fern.gif"},
    },
    {
        "animal": "minivet",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_minivet.gif"},
    },
    {
        "animal": "whip scorpion",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_whip_scorpion.gif"},
    },
    {
        "animal": "panda",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_panda.gif"},
    },
    {
        "animal": "tumatukuru",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_tumatukuru.gif"},
    },
    {
        "animal": "linnaea",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_linnaea.gif"},
    },
    {
        "animal": "hawkbill",
        "classification": "reptile",
        "images": {"drawing": "images/animal/animals_reptile_hawkbill.gif"},
    },
    {
        "animal": "kentia",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_kentia.gif"},
    },
    {
        "animal": "tomfool",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_tomfool.gif"},
    },
    {
        "animal": "cimbex",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_cimbex.gif"},
    },
    {
        "animal": "tucotuco",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_tucotuco.gif"},
    },
    {
        "animal": "dryopteris",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_dryopteris.gif"},
    },
    {
        "animal": "meganser",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_meganser.gif"},
    },
    {
        "animal": "porcupine",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_porcupine.gif"},
    },
    {
        "animal": "cod",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_cod.gif"},
    },
    {
        "animal": "cotton",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_cotton.gif"},
    },
    {
        "animal": "rhino",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_rhino.gif"},
    },
    {
        "animal": "peacock",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_peacock.gif"},
    },
    {
        "animal": "chacma",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_chacma.gif"},
    },
    {
        "animal": "stint",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_stint.gif"},
    },
    {
        "animal": "garial",
        "classification": "reptile",
        "images": {"drawing": "images/animal/animals_reptile_garial.gif"},
    },
    {
        "animal": "tasmanian",
        "classification": "marsupial",
        "images": {"drawing": "images/animal/animals_marsupial_tasmanian.gif"},
    },
    {
        "animal": "thrips",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_thrips.gif"},
    },
    {
        "animal": "lyre bird",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_lyre_bird.gif"},
    },
    {
        "animal": "parakeet",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_parakeet.gif"},
    },
    {
        "animal": "whitefish",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_whitefish.gif"},
    },
    {
        "animal": "sandfish",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_sand_fish.gif"},
    },
    {
        "animal": "tunny",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_tunny.gif"},
    },
    {
        "animal": "goosander",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_goosander.gif"},
    },
    {
        "animal": "skunk",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_skunk.gif"},
    },
    {
        "animal": "sprawler",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_sprawler.gif"},
    },
    {
        "animal": "leaf insect",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_leaf_insect.gif"},
    },
    {
        "animal": "jaguar",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_jaguar.gif"},
    },
    {
        "animal": "crinkleroot",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_crinkleroot.gif"},
    },
    {
        "animal": "chevrotain",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_chevrotain.gif"},
    },
    {
        "animal": "woodchuck",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_woodchuck.gif"},
    },
    {
        "animal": "secretary bird",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_secretary_bird.gif"},
    },
    {
        "animal": "hornet",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_hornet.gif"},
    },
    {
        "animal": "isoetes",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_isoetes.gif"},
    },
    {
        "animal": "boa",
        "classification": "reptile",
        "images": {"drawing": "images/animal/animals_reptile_boa.gif"},
    },
    {
        "animal": "trepany",
        "classification": "invertebrate",
        "images": {"drawing": "images/animal/animals_invertebrate_trepany.gif"},
    },
    {
        "animal": "bison",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_bison.gif"},
    },
    {
        "animal": "pisdras",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_pisdras.gif"},
    },
    {
        "animal": "pelican",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_pelican.gif"},
    },
    {
        "animal": "viper",
        "classification": "reptile",
        "images": {"drawing": "images/animal/animals_reptile_viper.gif"},
    },
    {
        "animal": "stork",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_stork.gif"},
    },
    {
        "animal": "carex",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_carex.gif"},
    },
    {
        "animal": "awantibo",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_awantibo.gif"},
    },
    {
        "animal": "camel",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_camel.gif"},
    },
    {
        "animal": "poppy",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_poppy.gif"},
    },
    {
        "animal": "leopard",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_leopard.gif"},
    },
    {
        "animal": "oyster",
        "classification": "invertebrate",
        "images": {"drawing": "images/animal/animals_invertebrate_oyster.gif"},
    },
    {
        "animal": "dunlin",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_dunlin.gif"},
    },
    {
        "animal": "chicken",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_chicken.gif"},
    },
    {
        "animal": "millepede",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_millepede.gif"},
    },
    {
        "animal": "lanner",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_lanner.gif"},
    },
    {
        "animal": "flamingo",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_flamingo.gif"},
    },
    {
        "animal": "soldier beetle",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_soldier_beetle.gif"},
    },
    {
        "animal": "cooba",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_cooba.gif"},
    },
    {
        "animal": "cypripedium",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_cypripedium.gif"},
    },
    {
        "animal": "cockroach",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_cockroach.gif"},
    },
    {
        "animal": "holothurian",
        "classification": "invertebrate",
        "images": {
            "drawing": "images/animal/animals_invertebrate_holothurian.gif"
        },
    },
    {
        "animal": "penguin",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_penguin.gif"},
    },
    {
        "animal": "souslik",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_souslik.gif"},
    },
    {
        "animal": "john dory",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_john_dory.gif"},
    },
    {
        "animal": "alpaca",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_alpaca.gif"},
    },
    {
        "animal": "quandong nut",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_quandong_nut.gif"},
    },
    {
        "animal": "tea plant",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_tea_plant.gif"},
    },
    {
        "animal": "correa",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_correa.gif"},
    },
    {
        "animal": "flower de luce",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_flower_de_luce.gif"},
    },
    {
        "animal": "goose",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_goose.gif"},
    },
    {
        "animal": "marmose",
        "classification": "marsupial",
        "images": {"drawing": "images/animal/animals_marsupial_marmose.gif"},
    },
    {
        "animal": "tahr",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_tahr.gif"},
    },
    {
        "animal": "boar",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_boar.gif"},
    },
    {
        "animal": "fire fly",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_fire_fly.gif"},
    },
    {
        "animal": "ramarama",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_ramarama.gif"},
    },
    {
        "animal": "tortoise",
        "classification": "reptile",
        "images": {"drawing": "images/animal/animals_reptile_tortoise.gif"},
    },
    {
        "animal": "bluegill",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_bluegill.gif"},
    },
    {
        "animal": "kestrel",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_kestrel.gif"},
    },
    {
        "animal": "cardinal",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_cardinal.gif"},
    },
    {
        "animal": "sapodilla",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_sapodilla.gif"},
    },
    {
        "animal": "squirrel",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_squirrel.gif"},
    },
    {
        "animal": "snowdrop",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_snowdrop.gif"},
    },
    {
        "animal": "anaconda",
        "classification": "reptile",
        "images": {"drawing": "images/animal/animals_reptile_anaconda.gif"},
    },
    {
        "animal": "barricuda",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_barricuda.gif"},
    },
    {
        "animal": "gadfly",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_gadfly.gif"},
    },
    {
        "animal": "sabre bird",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_sabre_bird.gif"},
    },
    {
        "animal": "squid",
        "classification": "invertebrate",
        "images": {"drawing": "images/animal/animals_invertebrate_squid.gif"},
    },
    {
        "animal": "coyote",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_coyote.gif"},
    },
    {
        "animal": "carp",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_carp.gif"},
    },
    {
        "animal": "lark",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_lark.gif"},
    },
    {
        "animal": "broadbill",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_broadbill.gif"},
    },
    {
        "animal": "tiger flower",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_tiger_flower.gif"},
    },
    {
        "animal": "cuckoo",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_cuckoo.gif"},
    },
    {
        "animal": "fall fish",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_fall_fish.gif"},
    },
    {
        "animal": "gopher",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_gopher.gif"},
    },
    {
        "animal": "kangaroo apple",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_kangaroo_apple.gif"},
    },
    {
        "animal": "lantern fly",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_lantern_fly.gif"},
    },
    {
        "animal": "remora",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_remora.gif"},
    },
    {
        "animal": "narcissus",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_narcissus.gif"},
    },
    {
        "animal": "bunting",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_bunting.gif"},
    },
    {
        "animal": "papaw",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_papaw.gif"},
    },
    {
        "animal": "sondeli",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_sondeli.gif"},
    },
    {
        "animal": "agama",
        "classification": "reptile",
        "images": {"drawing": "images/animal/animals_reptile_agama.gif"},
    },
    {
        "animal": "pepper",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_pepper.gif"},
    },
    {
        "animal": "buttercup",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_buttercup.gif"},
    },
    {
        "animal": "chickadee",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_chickadee.gif"},
    },
    {
        "animal": "seatrout",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_sea_trout.gif"},
    },
    {
        "animal": "ant",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_ant.gif"},
    },
    {
        "animal": "teju",
        "classification": "reptile",
        "images": {"drawing": "images/animal/animals_reptile_teju.gif"},
    },
    {
        "animal": "douc",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_douc.gif"},
    },
    {
        "animal": "dace",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_dace.gif"},
    },
    {
        "animal": "papaya",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_papaya.gif"},
    },
    {
        "animal": "talipot",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_talipot.gif"},
    },
    {
        "animal": "shark",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_shark.gif"},
    },
    {
        "animal": "fairy wren",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_fairy_wren.gif"},
    },
    {
        "animal": "lobster",
        "classification": "invertebrate",
        "images": {"drawing": "images/animal/animals_invertebrate_lobster.gif"},
    },
    {
        "animal": "crappie",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_crappie.gif"},
    },
    {
        "animal": "thyme",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_thyme.gif"},
    },
    {
        "animal": "palm",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_palm.gif"},
    },
    {
        "animal": "stanhopea",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_stanhopea.gif"},
    },
    {
        "animal": "wolf",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_wolf.gif"},
    },
    {
        "animal": "wattle",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_wattle.gif"},
    },
    {
        "animal": "banyan tree",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_banyan_tree.gif"},
    },
    {
        "animal": "coffee",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_coffee.gif"},
    },
    {
        "animal": "tern",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_tern.gif"},
    },
    {
        "animal": "smelt",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_smelt.gif"},
    },
    {
        "animal": "salvia",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_salvia.gif"},
    },
    {
        "animal": "goldfish",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_goldfish.gif"},
    },
    {
        "animal": "silverfish",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_silverfish.gif"},
    },
    {
        "animal": "monitor",
        "classification": "reptile",
        "images": {"drawing": "images/animal/animals_reptile_monitor.gif"},
    },
    {
        "animal": "begonia",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_begonia.gif"},
    },
    {
        "animal": "jay",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_tree_jay.gif"},
    },
    {
        "animal": "narwhal",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_narwhal.gif"},
    },
    {
        "animal": "pipe fish",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_pipe_fish.gif"},
    },
    {
        "animal": "opah",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_opah.gif"},
    },
    {
        "animal": "sepiola",
        "classification": "invertebrate",
        "images": {"drawing": "images/animal/animals_invertebrate_sepiola.gif"},
    },
    {
        "animal": "kohl rabi",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_kohl_rabi.gif"},
    },
    {
        "animal": "butterfly",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_butterfly.gif"},
    },
    {
        "animal": "ruffe",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_ruffe.gif"},
    },
    {
        "animal": "water bug",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_water_bug.gif"},
    },
    {
        "animal": "rockfish",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_rockfish.gif"},
    },
    {
        "animal": "willow",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_willow.gif"},
    },
    {
        "animal": "otter",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_otter.gif"},
    },
    {
        "animal": "fieldfare",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_fieldfare.gif"},
    },
    {
        "animal": "hen",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_water_hen.gif"},
    },
    {
        "animal": "grebe",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_grebe.gif"},
    },
    {
        "animal": "cockatoo",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_cockatoo.gif"},
    },
    {
        "animal": "dogtooth violet",
        "classification": "plant",
        "images": {
            "drawing": "images/animal/animals_plant_dogtooth_violet.gif"
        },
    },
    {
        "animal": "shrike",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_shrike.gif"},
    },
    {
        "animal": "rose beetle",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_rose_beetle.gif"},
    },
    {
        "animal": "walleye",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_walleye.gif"},
    },
    {
        "animal": "poison sumac",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_poison_sumac.gif"},
    },
    {
        "animal": "bass",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_bass.gif"},
    },
    {
        "animal": "pig",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_pig.gif"},
    },
    {
        "animal": "gatrolobium",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_gatrolobium.gif"},
    },
    {
        "animal": "tuatera",
        "classification": "reptile",
        "images": {"drawing": "images/animal/animals_reptile_tuatera.gif"},
    },
    {
        "animal": "thrush",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_thrush.gif"},
    },
    {
        "animal": "mosquito",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_mosquito.gif"},
    },
    {
        "animal": "emuwren",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_emu_wren.gif"},
    },
    {
        "animal": "bidens",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_bidens.gif"},
    },
    {
        "animal": "trillium",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_trillium.gif"},
    },
    {
        "animal": "tiger",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_tiger.gif"},
    },
    {
        "animal": "iguana",
        "classification": "reptile",
        "images": {"drawing": "images/animal/animals_reptile_iguana.gif"},
    },
    {
        "animal": "sagittaria",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_sagittaria.gif"},
    },
    {
        "animal": "tambourine",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_tambourine.gif"},
    },
    {
        "animal": "pipsissewa",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_pipsissewa.gif"},
    },
    {
        "animal": "bloodroot",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_bloodroot.gif"},
    },
    {
        "animal": "emu",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_emu.gif"},
    },
    {
        "animal": "celery topped pine",
        "classification": "plant",
        "images": {
            "drawing": "images/animal/animals_plant_celery_topped_pine.gif"
        },
    },
    {
        "animal": "stipa",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_stipa.gif"},
    },
    {
        "animal": "pink",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_pink.gif"},
    },
    {
        "animal": "anemone",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_anemone.gif"},
    },
    {
        "animal": "pine sawyer",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_pine_sawyer.gif"},
    },
    {
        "animal": "koel",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_koel.gif"},
    },
    {
        "animal": "whale",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_whale.gif"},
    },
    {
        "animal": "paradise bird",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_paradise_bird.gif"},
    },
    {
        "animal": "stinkpot",
        "classification": "reptile",
        "images": {"drawing": "images/animal/animals_reptile_stinkpot.gif"},
    },
    {
        "animal": "gnat",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_gnat.gif"},
    },
    {
        "animal": "antelope",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_antelope.gif"},
    },
    {
        "animal": "plaice",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_plaice.gif"},
    },
    {
        "animal": "locust",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_locust.gif"},
    },
    {
        "animal": "geranium",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_geranium.gif"},
    },
    {
        "animal": "chimpazee",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_chimpazee.gif"},
    },
    {
        "animal": "hellebore",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_hellebore.gif"},
    },
    {
        "animal": "epidendrum",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_epidendrum.gif"},
    },
    {
        "animal": "bear",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_glacier_bear.gif"},
    },
    {
        "animal": "hyena",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_hyena.gif"},
    },
    {
        "animal": "crocodile",
        "classification": "reptile",
        "images": {"drawing": "images/animal/animals_reptile_crocodile.gif"},
    },
    {
        "animal": "sand cricket",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_sand_cricket.gif"},
    },
    {
        "animal": "beaver",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_beaver.gif"},
    },
    {
        "animal": "flying fish",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_flying_fish.gif"},
    },
    {
        "animal": "harrier eagle",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_harrier_eagle.gif"},
    },
    {
        "animal": "spider",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_spider.gif"},
    },
    {
        "animal": "ballan",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_ballan.gif"},
    },
    {
        "animal": "sardine",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_sardine.gif"},
    },
    {
        "animal": "grasshopper",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_grasshopper2.gif"},
    },
    {
        "animal": "jacana",
        "classification": "reptile",
        "images": {"drawing": "images/animal/animals_reptile_jacana.gif"},
    },
    {
        "animal": "drum fish",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_drum_fish.gif"},
    },
    {
        "animal": "sailfish",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_sailfish.gif"},
    },
    {
        "animal": "nagor",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_nagor.gif"},
    },
    {
        "animal": "chrysanthemums",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_chrysanthemums.gif"},
    },
    {
        "animal": "scarab beetle",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_scarab_beetle.gif"},
    },
    {
        "animal": "partridge",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_partridge.gif"},
    },
    {
        "animal": "crested quail",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_crested_quail.gif"},
    },
    {
        "animal": "lupine",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_lupine.gif"},
    },
    {
        "animal": "nepenthes",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_nepenthes.gif"},
    },
    {
        "animal": "pilchard",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_pilchard.gif"},
    },
    {
        "animal": "larch",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_larch.gif"},
    },
    {
        "animal": "fringed gentian",
        "classification": "plant",
        "images": {
            "drawing": "images/animal/animals_plant_fringed_gentian.gif"
        },
    },
    {
        "animal": "sand bur",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_sand_bur.gif"},
    },
    {
        "animal": "soy bean",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_soy_bean.gif"},
    },
    {
        "animal": "trout",
        "classification": "fish",
        "images": {"drawing": "images/animal/animals_fish_trout2.gif"},
    },
    {
        "animal": "crocus",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_crocus.gif"},
    },
    {
        "animal": "silkworm",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_silkworm.gif"},
    },
    {
        "animal": "planerian worm",
        "classification": "invertebrate",
        "images": {
            "drawing": "images/animal/animals_invertebrate_planerian_worm.gif"
        },
    },
    {
        "animal": "darter",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_darter.gif"},
    },
    {
        "animal": "oak pest",
        "classification": "bug",
        "images": {"drawing": "images/animal/animals_bug_oak_pest.gif"},
    },
    {
        "animal": "paca rana",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_paca_rana.gif"},
    },
    {
        "animal": "currasow",
        "classification": "bird",
        "images": {"drawing": "images/animal/animals_bird_currasow.gif"},
    },
    {
        "animal": "sequoia",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_sequoia.gif"},
    },
    {
        "animal": "buckeye",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_buckeye.gif"},
    },
    {
        "animal": "steenbok",
        "classification": "mammal",
        "images": {"drawing": "images/animal/animals_mammal_steenbok.gif"},
    },
    {
        "animal": "jasmine",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_jasmine.gif"},
    },
    {
        "animal": "totara",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_totara.gif"},
    },
    {
        "animal": "alder",
        "classification": "plant",
        "images": {"drawing": "images/animal/animals_plant_alder.gif"},
    },
]
