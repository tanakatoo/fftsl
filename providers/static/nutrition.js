const EDAMAM_API = 'https://api.edamam.com'

const RESPONSE = {
    "uri": "http://www.edamam.com/ontologies/edamam.owl#recipe_0244bf1acc224cddb020840339807cdb",
    "calories": 361,
    "totalWeight": 552.6806498257349,
    "dietLabels": [],
    "healthLabels": [
        "EGG_FREE",
        "PEANUT_FREE",
        "TREE_NUT_FREE",
        "SOY_FREE",
        "FISH_FREE",
        "SHELLFISH_FREE",
        "PORK_FREE",
        "RED_MEAT_FREE",
        "CRUSTACEAN_FREE",
        "CELERY_FREE",
        "MUSTARD_FREE",
        "SESAME_FREE",
        "LUPINE_FREE",
        "MOLLUSK_FREE",
        "ALCOHOL_FREE"
    ],
    "cautions": [
        "GLUTEN",
        "WHEAT",
        "MILK",
        "SULFITES",
        "FODMAP"
    ],
    "totalNutrients": {
        "ENERC_KCAL": {
            "label": "Energy",
            "quantity": 361.5415023289238,
            "unit": "kcal"
        },
        "FAT": {
            "label": "Total lipid (fat)",
            "quantity": 7.213003686360159,
            "unit": "g"
        },
        "FASAT": {
            "label": "Fatty acids, total saturated",
            "quantity": 1.693550129711643,
            "unit": "g"
        },
        "FATRN": {
            "label": "Fatty acids, total trans",
            "quantity": 0.12167028742313382,
            "unit": "g"
        },
        "FAMS": {
            "label": "Fatty acids, total monounsaturated",
            "quantity": 6.115482435286585,
            "unit": "g"
        },
        "FAPU": {
            "label": "Fatty acids, total polyunsaturated",
            "quantity": 2.96078047288128,
            "unit": "g"
        },
        "CHOCDF": {
            "label": "Carbohydrate, by difference",
            "quantity": 36.57847863398293,
            "unit": "g"
        },
        "CHOCDF.net": {
            "label": "Carbohydrates (net)",
            "quantity": 29.88553561417876,
            "unit": "g"
        },
        "FIBTG": {
            "label": "Fiber, total dietary",
            "quantity": 6.692943019804171,
            "unit": "g"
        },
        "SUGAR": {
            "label": "Sugars, total",
            "quantity": 19.621684092194343,
            "unit": "g"
        },
        "SUGAR.added": {
            "label": "Sugars, added",
            "quantity": 5.094943936008,
            "unit": "g"
        },
        "PROCNT": {
            "label": "Protein",
            "quantity": 21.958918617899638,
            "unit": "g"
        },
        "CHOLE": {
            "label": "Cholesterol",
            "quantity": 69.40629683861943,
            "unit": "mg"
        },
        "NA": {
            "label": "Sodium, Na",
            "quantity": 200.479096,
            "unit": "mg"
        },
        "CA": {
            "label": "Calcium, Ca",
            "quantity": 110.74107346173787,
            "unit": "mg"
        },
        "MG": {
            "label": "Magnesium, Mg",
            "quantity": 73.5806256841026,
            "unit": "mg"
        },
        "K": {
            "label": "Potassium, K",
            "quantity": 1126.2420613256443,
            "unit": "mg"
        },
        "FE": {
            "label": "Iron, Fe",
            "quantity": 2.2815680541724856,
            "unit": "mg"
        },
        "ZN": {
            "label": "Zinc, Zn",
            "quantity": 1.8950281433824383,
            "unit": "mg"
        },
        "P": {
            "label": "Phosphorus, P",
            "quantity": 288.8940349959702,
            "unit": "mg"
        },
        "VITA_RAE": {
            "label": "Vitamin A, RAE",
            "quantity": 169.99473329369334,
            "unit": "µg"
        },
        "VITC": {
            "label": "Vitamin C, total ascorbic acid",
            "quantity": 55.14456091667835,
            "unit": "mg"
        },
        "THIA": {
            "label": "Thiamin",
            "quantity": 0.2850575835263177,
            "unit": "mg"
        },
        "RIBF": {
            "label": "Riboflavin",
            "quantity": 0.26010288193413916,
            "unit": "mg"
        },
        "NIA": {
            "label": "Niacin",
            "quantity": 8.472462937273407,
            "unit": "mg"
        },
        "VITB6A": {
            "label": "Vitamin B-6",
            "quantity": 0.854028853368137,
            "unit": "mg"
        },
        "FOLDFE": {
            "label": "Folate, DFE",
            "quantity": 89.23663472457378,
            "unit": "µg"
        },
        "FOLFD": {
            "label": "Folate, food",
            "quantity": 85.13827990013777,
            "unit": "µg"
        },
        "FOLAC": {
            "label": "Folic acid",
            "quantity": 2.444839343762691,
            "unit": "µg"
        },
        "VITB12": {
            "label": "Vitamin B-12",
            "quantity": 0.35969942630630614,
            "unit": "µg"
        },
        "VITD": {
            "label": "Vitamin D (D2 + D3)",
            "quantity": 0.22168260325118289,
            "unit": "µg"
        },
        "TOCPHA": {
            "label": "Vitamin E (alpha-tocopherol)",
            "quantity": 2.3298305618786865,
            "unit": "mg"
        },
        "VITK1": {
            "label": "Vitamin K (phylloquinone)",
            "quantity": 35.33963499549747,
            "unit": "µg"
        },
        "WATER": {
            "label": "Water",
            "quantity": 471.78422411753263,
            "unit": "g"
        }
    },
    "totalDaily": {
        "ENERC_KCAL": {
            "label": "Energy",
            "quantity": 18.077075116446192,
            "unit": "%"
        },
        "FAT": {
            "label": "Fat",
            "quantity": 23.40462105593871,
            "unit": "%"
        },
        "FASAT": {
            "label": "Saturated",
            "quantity": 23.467750648558216,
            "unit": "%"
        },
        "CHOCDF": {
            "label": "Carbs",
            "quantity": 12.192826211327644,
            "unit": "%"
        },
        "FIBTG": {
            "label": "Fiber",
            "quantity": 26.771772079216685,
            "unit": "%"
        },
        "PROCNT": {
            "label": "Protein",
            "quantity": 43.91783723579928,
            "unit": "%"
        },
        "CHOLE": {
            "label": "Cholesterol",
            "quantity": 23.13543227953981,
            "unit": "%"
        },
        "NA": {
            "label": "Sodium",
            "quantity": 53.311628999999996,
            "unit": "%"
        },
        "CA": {
            "label": "Calcium",
            "quantity": 11.074107346173786,
            "unit": "%"
        },
        "MG": {
            "label": "Magnesium",
            "quantity": 17.519196591453,
            "unit": "%"
        },
        "K": {
            "label": "Potassium",
            "quantity": 23.962597049481793,
            "unit": "%"
        },
        "FE": {
            "label": "Iron",
            "quantity": 12.675378078736031,
            "unit": "%"
        },
        "ZN": {
            "label": "Zinc",
            "quantity": 17.227528576203984,
            "unit": "%"
        },
        "P": {
            "label": "Phosphorus",
            "quantity": 41.27057642799574,
            "unit": "%"
        },
        "VITA_RAE": {
            "label": "Vitamin A",
            "quantity": 18.88830369929926,
            "unit": "%"
        },
        "VITC": {
            "label": "Vitamin C",
            "quantity": 61.27173435186483,
            "unit": "%"
        },
        "THIA": {
            "label": "Thiamin (B1)",
            "quantity": 23.754798627193146,
            "unit": "%"
        },
        "RIBF": {
            "label": "Riboflavin (B2)",
            "quantity": 20.00791399493378,
            "unit": "%"
        },
        "NIA": {
            "label": "Niacin (B3)",
            "quantity": 52.9528933579588,
            "unit": "%"
        },
        "VITB6A": {
            "label": "Vitamin B6",
            "quantity": 65.69452718216439,
            "unit": "%"
        },
        "FOLDFE": {
            "label": "Folate equivalent (total)",
            "quantity": 22.309158681143444,
            "unit": "%"
        },
        "VITB12": {
            "label": "Vitamin B12",
            "quantity": 14.987476096096088,
            "unit": "%"
        },
        "VITD": {
            "label": "Vitamin D",
            "quantity": 1.4778840216745526,
            "unit": "%"
        },
        "TOCPHA": {
            "label": "Vitamin E",
            "quantity": 15.53220374585791,
            "unit": "%"
        },
        "VITK1": {
            "label": "Vitamin K",
            "quantity": 29.449695829581223,
            "unit": "%"
        }
    },
    "ingredients": [
        {
            "text": "150g chicken and 2 medium tomatoes and 1 tsp salt and 1 tsp sugar and 1 large onion",
            "parsed": [
                {
                    "quantity": 150.0,
                    "measure": "gram",
                    "foodMatch": "chicken",
                    "food": "Chicken",
                    "foodId": "food_bkzqg38b4wc494bwfwrsda9r7pq7",
                    "weight": 150.0,
                    "retainedWeight": 150.0,
                    "nutrients": {
                        "VITD": {
                            "label": "Vitamin D",
                            "quantity": 9.378359474971194,
                            "unit": "IU"
                        },
                        "FATRN": {
                            "label": "Fatty acids, total trans",
                            "quantity": 0.12167028742313382,
                            "unit": "g"
                        },
                        "ENERC_KCAL": {
                            "label": "Energy",
                            "quantity": 241.00750232892378,
                            "unit": "kcal"
                        },
                        "FASAT": {
                            "label": "Fatty acids, total saturated",
                            "quantity": 4.5616701297116435,
                            "unit": "g"
                        },
                        "VITA_RAE": {
                            "label": "Vitamin A, RAE",
                            "quantity": 66.67473329369335,
                            "unit": "µg"
                        },
                        "PROCNT": {
                            "label": "Protein",
                            "quantity": 18.14411861789964,
                            "unit": "g"
                        },
                        "TOCPHA": {
                            "label": "Vitamin E (alpha-tocopherol)",
                            "quantity": 0.9714305618786867,
                            "unit": "mg"
                        },
                        "CHOLE": {
                            "label": "Cholesterol",
                            "quantity": 69.40629683861943,
                            "unit": "mg"
                        },
                        "CHOCDF": {
                            "label": "Carbohydrate, by difference",
                            "quantity": 8.799918633982935,
                            "unit": "g"
                        },
                        "FAT": {
                            "label": "Total lipid (fat)",
                            "quantity": 14.571003686360159,
                            "unit": "g"
                        },
                        "FIBTG": {
                            "label": "Fiber, total dietary",
                            "quantity": 1.190943019804172,
                            "unit": "g"
                        },
                        "RIBF": {
                            "label": "Riboflavin",
                            "quantity": 0.17206488193413919,
                            "unit": "mg"
                        },
                        "THIA": {
                            "label": "Thiamin",
                            "quantity": 0.12503758352631775,
                            "unit": "mg"
                        },
                        "FAPU": {
                            "label": "Fatty acids, total polyunsaturated",
                            "quantity": 2.73110047288128,
                            "unit": "g"
                        },
                        "NIA": {
                            "label": "Niacin",
                            "quantity": 6.837222937273408,
                            "unit": "mg"
                        },
                        "VITC": {
                            "label": "Vitamin C, total ascorbic acid",
                            "quantity": 10.342560916678348,
                            "unit": "mg"
                        },
                        "FAMS": {
                            "label": "Fatty acids, total monounsaturated",
                            "quantity": 6.019722435286586,
                            "unit": "g"
                        },
                        "VITB6A": {
                            "label": "Vitamin B-6",
                            "quantity": 0.4772288533681371,
                            "unit": "mg"
                        },
                        "VITB12": {
                            "label": "Vitamin B-12",
                            "quantity": 0.35969942630630614,
                            "unit": "µg"
                        },
                        "SUGAR.added": {
                            "label": "Sugars, added",
                            "quantity": 0.9033439360079994,
                            "unit": "g"
                        },
                        "WATER": {
                            "label": "Water",
                            "quantity": 105.5942228178812,
                            "unit": "g"
                        },
                        "K": {
                            "label": "Potassium, K",
                            "quantity": 323.93960933958556,
                            "unit": "mg"
                        },
                        "P": {
                            "label": "Phosphorus, P",
                            "quantity": 186.35403499597015,
                            "unit": "mg"
                        },
                        "NA": {
                            "label": "Sodium, Na",
                            "quantity": 299.6868365416454,
                            "unit": "mg"
                        },
                        "ZN": {
                            "label": "Zinc, Zn",
                            "quantity": 1.218927493556703,
                            "unit": "mg"
                        },
                        "SUGAR": {
                            "label": "Sugars, total",
                            "quantity": 2.6002840921943426,
                            "unit": "g"
                        },
                        "CA": {
                            "label": "Calcium, Ca",
                            "quantity": 51.003717503561475,
                            "unit": "mg"
                        },
                        "MG": {
                            "label": "Magnesium, Mg",
                            "quantity": 31.495819185845253,
                            "unit": "mg"
                        },
                        "FE": {
                            "label": "Iron, Fe",
                            "quantity": 1.2920819097475598,
                            "unit": "mg"
                        },
                        "VITK1": {
                            "label": "Vitamin K (phylloquinone)",
                            "quantity": 15.30563499549747,
                            "unit": "µg"
                        },
                        "FOLFD": {
                            "label": "Folate, food",
                            "quantity": 19.738279900137776,
                            "unit": "µg"
                        },
                        "FOLAC": {
                            "label": "Folic acid",
                            "quantity": 2.444839343762691,
                            "unit": "µg"
                        },
                        "FOLDFE": {
                            "label": "Folate, DFE",
                            "quantity": 23.836634724573788,
                            "unit": "µg"
                        }
                    },
                    "measureURI": "http://www.edamam.com/ontologies/edamam.owl#Measure_gram",
                    "status": "OK"
                },
                {
                    "quantity": 2.0,
                    "measure": "whole",
                    "foodMatch": "tomatoes",
                    "food": "tomato",
                    "foodId": "food_a6k79rrahp8fe2b26zussa3wtkqh",
                    "weight": 246.0,
                    "retainedWeight": 246.0,
                    "nutrients": {
                        "VITD": {
                            "label": "Vitamin D",
                            "quantity": 0.0,
                            "unit": "IU"
                        },
                        "ENERC_KCAL": {
                            "label": "Energy",
                            "quantity": 44.28,
                            "unit": "kcal"
                        },
                        "FASAT": {
                            "label": "Fatty acids, total saturated",
                            "quantity": 0.06888,
                            "unit": "g"
                        },
                        "VITA_RAE": {
                            "label": "Vitamin A, RAE",
                            "quantity": 103.32,
                            "unit": "µg"
                        },
                        "PROCNT": {
                            "label": "Protein",
                            "quantity": 2.1648,
                            "unit": "g"
                        },
                        "TOCPHA": {
                            "label": "Vitamin E (alpha-tocopherol)",
                            "quantity": 1.3284,
                            "unit": "mg"
                        },
                        "CHOLE": {
                            "label": "Cholesterol",
                            "quantity": 0.0,
                            "unit": "mg"
                        },
                        "CHOCDF": {
                            "label": "Carbohydrate, by difference",
                            "quantity": 9.5694,
                            "unit": "g"
                        },
                        "FAT": {
                            "label": "Total lipid (fat)",
                            "quantity": 0.49200000000000005,
                            "unit": "g"
                        },
                        "FIBTG": {
                            "label": "Fiber, total dietary",
                            "quantity": 2.952,
                            "unit": "g"
                        },
                        "RIBF": {
                            "label": "Riboflavin",
                            "quantity": 0.04674,
                            "unit": "mg"
                        },
                        "THIA": {
                            "label": "Thiamin",
                            "quantity": 0.09102,
                            "unit": "mg"
                        },
                        "FAPU": {
                            "label": "Fatty acids, total polyunsaturated",
                            "quantity": 0.20418000000000003,
                            "unit": "g"
                        },
                        "NIA": {
                            "label": "Niacin",
                            "quantity": 1.4612399999999999,
                            "unit": "mg"
                        },
                        "VITC": {
                            "label": "Vitamin C, total ascorbic acid",
                            "quantity": 33.702,
                            "unit": "mg"
                        },
                        "FAMS": {
                            "label": "Fatty acids, total monounsaturated",
                            "quantity": 0.07626000000000001,
                            "unit": "g"
                        },
                        "VITB6A": {
                            "label": "Vitamin B-6",
                            "quantity": 0.1968,
                            "unit": "mg"
                        },
                        "VITB12": {
                            "label": "Vitamin B-12",
                            "quantity": 0.0,
                            "unit": "µg"
                        },
                        "WATER": {
                            "label": "Water",
                            "quantity": 232.51919999999998,
                            "unit": "g"
                        },
                        "K": {
                            "label": "Potassium, K",
                            "quantity": 583.02,
                            "unit": "mg"
                        },
                        "P": {
                            "label": "Phosphorus, P",
                            "quantity": 59.04,
                            "unit": "mg"
                        },
                        "NA": {
                            "label": "Sodium, Na",
                            "quantity": 12.3,
                            "unit": "mg"
                        },
                        "ZN": {
                            "label": "Zinc, Zn",
                            "quantity": 0.4182,
                            "unit": "mg"
                        },
                        "SUGAR": {
                            "label": "Sugars, total",
                            "quantity": 6.4698,
                            "unit": "g"
                        },
                        "CA": {
                            "label": "Calcium, Ca",
                            "quantity": 24.6,
                            "unit": "mg"
                        },
                        "MG": {
                            "label": "Magnesium, Mg",
                            "quantity": 27.06,
                            "unit": "mg"
                        },
                        "FE": {
                            "label": "Iron, Fe",
                            "quantity": 0.6642,
                            "unit": "mg"
                        },
                        "VITK1": {
                            "label": "Vitamin K (phylloquinone)",
                            "quantity": 19.434,
                            "unit": "µg"
                        },
                        "FOLFD": {
                            "label": "Folate, food",
                            "quantity": 36.9,
                            "unit": "µg"
                        },
                        "FOLAC": {
                            "label": "Folic acid",
                            "quantity": 0.0,
                            "unit": "µg"
                        },
                        "FOLDFE": {
                            "label": "Folate, DFE",
                            "quantity": 36.9,
                            "unit": "µg"
                        }
                    },
                    "measureURI": "http://www.edamam.com/ontologies/edamam.owl#Measure_unit",
                    "status": "OK"
                },
                {
                    "quantity": 1.0,
                    "measure": "teaspoon",
                    "foodMatch": "salt",
                    "food": "salt",
                    "foodId": "food_btxz81db72hwbra2pncvebzzzum9",
                    "weight": 6.0,
                    "retainedWeight": 2.4806498257349574,
                    "nutrients": {
                        "RIBF": {
                            "label": "Riboflavin",
                            "quantity": 0.0,
                            "unit": "mg"
                        },
                        "VITD": {
                            "label": "Vitamin D",
                            "quantity": 0.0,
                            "unit": "IU"
                        },
                        "THIA": {
                            "label": "Thiamin",
                            "quantity": 0.0,
                            "unit": "mg"
                        },
                        "FAPU": {
                            "label": "Fatty acids, total polyunsaturated",
                            "quantity": 0.0,
                            "unit": "g"
                        },
                        "NIA": {
                            "label": "Niacin",
                            "quantity": 0.0,
                            "unit": "mg"
                        },
                        "ENERC_KCAL": {
                            "label": "Energy",
                            "quantity": 0.0,
                            "unit": "kcal"
                        },
                        "FASAT": {
                            "label": "Fatty acids, total saturated",
                            "quantity": 0.0,
                            "unit": "g"
                        },
                        "VITA_RAE": {
                            "label": "Vitamin A, RAE",
                            "quantity": 0.0,
                            "unit": "µg"
                        },
                        "VITC": {
                            "label": "Vitamin C, total ascorbic acid",
                            "quantity": 0.0,
                            "unit": "mg"
                        },
                        "PROCNT": {
                            "label": "Protein",
                            "quantity": 0.0,
                            "unit": "g"
                        },
                        "TOCPHA": {
                            "label": "Vitamin E (alpha-tocopherol)",
                            "quantity": 0.0,
                            "unit": "mg"
                        },
                        "CHOLE": {
                            "label": "Cholesterol",
                            "quantity": 0.0,
                            "unit": "mg"
                        },
                        "FAMS": {
                            "label": "Fatty acids, total monounsaturated",
                            "quantity": 0.0,
                            "unit": "g"
                        },
                        "CHOCDF": {
                            "label": "Carbohydrate, by difference",
                            "quantity": 0.0,
                            "unit": "g"
                        },
                        "FAT": {
                            "label": "Total lipid (fat)",
                            "quantity": 0.0,
                            "unit": "g"
                        },
                        "VITB6A": {
                            "label": "Vitamin B-6",
                            "quantity": 0.0,
                            "unit": "mg"
                        },
                        "VITB12": {
                            "label": "Vitamin B-12",
                            "quantity": 0.0,
                            "unit": "µg"
                        },
                        "FIBTG": {
                            "label": "Fiber, total dietary",
                            "quantity": 0.0,
                            "unit": "g"
                        },
                        "WATER": {
                            "label": "Water",
                            "quantity": 0.004961299651469915,
                            "unit": "g"
                        },
                        "K": {
                            "label": "Potassium, K",
                            "quantity": 0.1984519860587966,
                            "unit": "mg"
                        },
                        "P": {
                            "label": "Phosphorus, P",
                            "quantity": 0.0,
                            "unit": "mg"
                        },
                        "NA": {
                            "label": "Sodium, Na",
                            "quantity": 961.4502594583548,
                            "unit": "mg"
                        },
                        "ZN": {
                            "label": "Zinc, Zn",
                            "quantity": 0.0024806498257349575,
                            "unit": "mg"
                        },
                        "SUGAR": {
                            "label": "Sugars, total",
                            "quantity": 0.0,
                            "unit": "g"
                        },
                        "CA": {
                            "label": "Calcium, Ca",
                            "quantity": 0.5953559581763898,
                            "unit": "mg"
                        },
                        "MG": {
                            "label": "Magnesium, Mg",
                            "quantity": 0.024806498257349575,
                            "unit": "mg"
                        },
                        "FE": {
                            "label": "Iron, Fe",
                            "quantity": 0.00818614442492536,
                            "unit": "mg"
                        },
                        "VITK1": {
                            "label": "Vitamin K (phylloquinone)",
                            "quantity": 0.0,
                            "unit": "µg"
                        },
                        "FOLFD": {
                            "label": "Folate, food",
                            "quantity": 0.0,
                            "unit": "µg"
                        },
                        "FOLAC": {
                            "label": "Folic acid",
                            "quantity": 0.0,
                            "unit": "µg"
                        },
                        "FOLDFE": {
                            "label": "Folate, DFE",
                            "quantity": 0.0,
                            "unit": "µg"
                        }
                    },
                    "measureURI": "http://www.edamam.com/ontologies/edamam.owl#Measure_teaspoon",
                    "status": "OK"
                },
                {
                    "quantity": 1.0,
                    "measure": "teaspoon",
                    "foodMatch": "sugar",
                    "food": "sugar",
                    "foodId": "food_axi2ijobrk819yb0adceobnhm1c2",
                    "weight": 4.2,
                    "retainedWeight": 4.2,
                    "nutrients": {
                        "RIBF": {
                            "label": "Riboflavin",
                            "quantity": 7.98E-4,
                            "unit": "mg"
                        },
                        "VITD": {
                            "label": "Vitamin D",
                            "quantity": 0.0,
                            "unit": "IU"
                        },
                        "THIA": {
                            "label": "Thiamin",
                            "quantity": 0.0,
                            "unit": "mg"
                        },
                        "FAPU": {
                            "label": "Fatty acids, total polyunsaturated",
                            "quantity": 0.0,
                            "unit": "g"
                        },
                        "NIA": {
                            "label": "Niacin",
                            "quantity": 0.0,
                            "unit": "mg"
                        },
                        "ENERC_KCAL": {
                            "label": "Energy",
                            "quantity": 16.254,
                            "unit": "kcal"
                        },
                        "FASAT": {
                            "label": "Fatty acids, total saturated",
                            "quantity": 0.0,
                            "unit": "g"
                        },
                        "VITA_RAE": {
                            "label": "Vitamin A, RAE",
                            "quantity": 0.0,
                            "unit": "µg"
                        },
                        "VITC": {
                            "label": "Vitamin C, total ascorbic acid",
                            "quantity": 0.0,
                            "unit": "mg"
                        },
                        "PROCNT": {
                            "label": "Protein",
                            "quantity": 0.0,
                            "unit": "g"
                        },
                        "TOCPHA": {
                            "label": "Vitamin E (alpha-tocopherol)",
                            "quantity": 0.0,
                            "unit": "mg"
                        },
                        "CHOLE": {
                            "label": "Cholesterol",
                            "quantity": 0.0,
                            "unit": "mg"
                        },
                        "FAMS": {
                            "label": "Fatty acids, total monounsaturated",
                            "quantity": 0.0,
                            "unit": "g"
                        },
                        "CHOCDF": {
                            "label": "Carbohydrate, by difference",
                            "quantity": 4.199160000000001,
                            "unit": "g"
                        },
                        "FAT": {
                            "label": "Total lipid (fat)",
                            "quantity": 0.0,
                            "unit": "g"
                        },
                        "VITB6A": {
                            "label": "Vitamin B-6",
                            "quantity": 0.0,
                            "unit": "mg"
                        },
                        "VITB12": {
                            "label": "Vitamin B-12",
                            "quantity": 0.0,
                            "unit": "µg"
                        },
                        "SUGAR.added": {
                            "label": "Sugars, added",
                            "quantity": 4.1916,
                            "unit": "g"
                        },
                        "FIBTG": {
                            "label": "Fiber, total dietary",
                            "quantity": 0.0,
                            "unit": "g"
                        },
                        "WATER": {
                            "label": "Water",
                            "quantity": 8.4E-4,
                            "unit": "g"
                        },
                        "K": {
                            "label": "Potassium, K",
                            "quantity": 0.084,
                            "unit": "mg"
                        },
                        "P": {
                            "label": "Phosphorus, P",
                            "quantity": 0.0,
                            "unit": "mg"
                        },
                        "NA": {
                            "label": "Sodium, Na",
                            "quantity": 0.042,
                            "unit": "mg"
                        },
                        "ZN": {
                            "label": "Zinc, Zn",
                            "quantity": 4.2E-4,
                            "unit": "mg"
                        },
                        "SUGAR": {
                            "label": "Sugars, total",
                            "quantity": 4.1916,
                            "unit": "g"
                        },
                        "CA": {
                            "label": "Calcium, Ca",
                            "quantity": 0.042,
                            "unit": "mg"
                        },
                        "MG": {
                            "label": "Magnesium, Mg",
                            "quantity": 0.0,
                            "unit": "mg"
                        },
                        "FE": {
                            "label": "Iron, Fe",
                            "quantity": 0.0021000000000000003,
                            "unit": "mg"
                        },
                        "VITK1": {
                            "label": "Vitamin K (phylloquinone)",
                            "quantity": 0.0,
                            "unit": "µg"
                        },
                        "FOLFD": {
                            "label": "Folate, food",
                            "quantity": 0.0,
                            "unit": "µg"
                        },
                        "FOLAC": {
                            "label": "Folic acid",
                            "quantity": 0.0,
                            "unit": "µg"
                        },
                        "FOLDFE": {
                            "label": "Folate, DFE",
                            "quantity": 0.0,
                            "unit": "µg"
                        }
                    },
                    "measureURI": "http://www.edamam.com/ontologies/edamam.owl#Measure_teaspoon",
                    "status": "OK"
                },
                {
                    "quantity": 1.0,
                    "measure": "whole",
                    "foodMatch": "onion",
                    "food": "onions",
                    "foodId": "food_bmrvi4ob4binw9a5m7l07amlfcoy",
                    "weight": 150.0,
                    "retainedWeight": 150.0,
                    "nutrients": {
                        "VITD": {
                            "label": "Vitamin D",
                            "quantity": 0.0,
                            "unit": "IU"
                        },
                        "ENERC_KCAL": {
                            "label": "Energy",
                            "quantity": 60.0,
                            "unit": "kcal"
                        },
                        "FASAT": {
                            "label": "Fatty acids, total saturated",
                            "quantity": 0.063,
                            "unit": "g"
                        },
                        "VITA_RAE": {
                            "label": "Vitamin A, RAE",
                            "quantity": 0.0,
                            "unit": "µg"
                        },
                        "PROCNT": {
                            "label": "Protein",
                            "quantity": 1.65,
                            "unit": "g"
                        },
                        "TOCPHA": {
                            "label": "Vitamin E (alpha-tocopherol)",
                            "quantity": 0.03,
                            "unit": "mg"
                        },
                        "CHOLE": {
                            "label": "Cholesterol",
                            "quantity": 0.0,
                            "unit": "mg"
                        },
                        "CHOCDF": {
                            "label": "Carbohydrate, by difference",
                            "quantity": 14.01,
                            "unit": "g"
                        },
                        "FAT": {
                            "label": "Total lipid (fat)",
                            "quantity": 0.15,
                            "unit": "g"
                        },
                        "FIBTG": {
                            "label": "Fiber, total dietary",
                            "quantity": 2.55,
                            "unit": "g"
                        },
                        "RIBF": {
                            "label": "Riboflavin",
                            "quantity": 0.0405,
                            "unit": "mg"
                        },
                        "THIA": {
                            "label": "Thiamin",
                            "quantity": 0.06899999999999999,
                            "unit": "mg"
                        },
                        "FAPU": {
                            "label": "Fatty acids, total polyunsaturated",
                            "quantity": 0.025500000000000002,
                            "unit": "g"
                        },
                        "NIA": {
                            "label": "Niacin",
                            "quantity": 0.17400000000000002,
                            "unit": "mg"
                        },
                        "VITC": {
                            "label": "Vitamin C, total ascorbic acid",
                            "quantity": 11.1,
                            "unit": "mg"
                        },
                        "FAMS": {
                            "label": "Fatty acids, total monounsaturated",
                            "quantity": 0.0195,
                            "unit": "g"
                        },
                        "VITB6A": {
                            "label": "Vitamin B-6",
                            "quantity": 0.18,
                            "unit": "mg"
                        },
                        "VITB12": {
                            "label": "Vitamin B-12",
                            "quantity": 0.0,
                            "unit": "µg"
                        },
                        "WATER": {
                            "label": "Water",
                            "quantity": 133.665,
                            "unit": "g"
                        },
                        "K": {
                            "label": "Potassium, K",
                            "quantity": 219.0,
                            "unit": "mg"
                        },
                        "P": {
                            "label": "Phosphorus, P",
                            "quantity": 43.5,
                            "unit": "mg"
                        },
                        "NA": {
                            "label": "Sodium, Na",
                            "quantity": 6.0,
                            "unit": "mg"
                        },
                        "ZN": {
                            "label": "Zinc, Zn",
                            "quantity": 0.25500000000000006,
                            "unit": "mg"
                        },
                        "SUGAR": {
                            "label": "Sugars, total",
                            "quantity": 6.36,
                            "unit": "g"
                        },
                        "CA": {
                            "label": "Calcium, Ca",
                            "quantity": 34.5,
                            "unit": "mg"
                        },
                        "MG": {
                            "label": "Magnesium, Mg",
                            "quantity": 15.0,
                            "unit": "mg"
                        },
                        "FE": {
                            "label": "Iron, Fe",
                            "quantity": 0.315,
                            "unit": "mg"
                        },
                        "VITK1": {
                            "label": "Vitamin K (phylloquinone)",
                            "quantity": 0.6,
                            "unit": "µg"
                        },
                        "FOLFD": {
                            "label": "Folate, food",
                            "quantity": 28.5,
                            "unit": "µg"
                        },
                        "FOLAC": {
                            "label": "Folic acid",
                            "quantity": 0.0,
                            "unit": "µg"
                        },
                        "FOLDFE": {
                            "label": "Folate, DFE",
                            "quantity": 28.5,
                            "unit": "µg"
                        }
                    },
                    "measureURI": "http://www.edamam.com/ontologies/edamam.owl#Measure_unit",
                    "status": "OK"
                }
            ]
        }
    ],
    "totalNutrientsKCal": {
        "ENERC_KCAL": {
            "label": "Energy",
            "quantity": 362,
            "unit": "kcal"
        },
        "PROCNT_KCAL": {
            "label": "Calories from protein",
            "quantity": 86,
            "unit": "kcal"
        },
        "FAT_KCAL": {
            "label": "Calories from fat",
            "quantity": 133,
            "unit": "kcal"
        },
        "CHOCDF_KCAL": {
            "label": "Calories from carbohydrates",
            "quantity": 143,
            "unit": "kcal"
        }
    }
}

// console.log('fat ' + RESPONSE.totalNutrients.FAT.quantity)
// console.log('saturated fat ' + RESPONSE.totalNutrients.FASAT.quantity)
// console.log('trans fat ' + RESPONSE.totalNutrients.FATRN.quantity)
// console.log('energy ' + RESPONSE.totalNutrients.ENERC_KCAL.quantity)
// console.log('fiber ' + RESPONSE.totalNutrients.FIBTG.quantity)
// console.log('protein ' + RESPONSE.totalNutrients.PROCNT.quantity)
// console.log('sodium ' + RESPONSE.totalNutrients.NA.quantity)
// console.log('ingred ' + RESPONSE.ingredients[0].parsed[0].food)
// console.log('ingred ' + RESPONSE.ingredients[0].parsed[0].quantity)
// console.log('ingred ' + RESPONSE.ingredients[0].parsed[0].measure)
// console.log('ingred ' + RESPONSE.ingredients[0].parsed[0].weight + 'g')
// console.log('ingred ' + RESPONSE.ingredients[0].parsed[1].food)
// console.log('ingred ' + RESPONSE.ingredients[0].parsed[1].quantity)
// console.log('ingred ' + RESPONSE.ingredients[0].parsed[1].measure)
// console.log('ingred ' + RESPONSE.ingredients[0].parsed[1].weight + 'g')
// console.log('food ' + ingredients[0].food)
// console.log('quantity ' + ingredients[0].quantity)
// console.log('measure ' + ingredients[0].measure)
// console.log('weight ' + ingredients[0].weight)
document.querySelector("#analyze").addEventListener("click", getNutrition)

async function getNutrition(e) {
    e.preventDefault()
    try {
        if (document.querySelector("#recipe").value.trim() != "") {
            const ingr = encodeURIComponent(document.querySelector("#recipe").value.replaceAll("\n", " and "))
            // call axios to get info from db
            // const RESPONSE = await axios.get(`${EDAMAM_API}/api/nutrition-data?app_id=0b4f0367&app_key=ad95ab4c4d78064dfa5d69506156ef1d&ingr=${ingr}`)

            console.log(RESPONSE)
            // console.log('fat ' + RESPONSE.data.totalNutrients.FAT.quantity)
            // console.log('saturated fat ' + RESPONSE.data.totalNutrients.FASAT.quantity)
            // console.log('trans fat ' + RESPONSE.data.totalNutrients.FATRN.quantity)
            // console.log('energy ' + RESPONSE.data.totalNutrients.ENERC_KCAL.quantity)
            // console.log('fiber ' + RESPONSE.data.totalNutrients.FIBTG.quantity)
            // console.log('protein ' + RESPONSE.data.totalNutrients.PROCNT.quantity)
            // console.log('sodium ' + RESPONSE.data.totalNutrients.NA.quantity)
            // console.log('# of ingred ' + RESPONSE.data.ingredients[0].parsed.length)
            // console.log('food ' + RESPONSE.data.ingredients[0].parsed[0].food)

            // console.log('quantity ' + RESPONSE.data.ingredients[0].parsed[0].quantity)
            // console.log('measure ' + RESPONSE.data.ingredients[0].parsed[0].measure)
            // console.log('weight ' + RESPONSE.data.ingredients[0].parsed[0].weight + 'g')
            // console.log('food ' + RESPONSE.data.ingredients[0].parsed[1].food)
            // console.log('quantity ' + RESPONSE.data.ingredients[0].parsed[1].quantity)
            // console.log('measure ' + RESPONSE.data.ingredients[0].parsed[1].measure)
            // console.log('weight ' + RESPONSE.data.ingredients[0].parsed[1].weight + 'g')

            // display section
            // document.querySelector("#analyzeResults").classList.toggle("hide")
            // displayAPIResults(RESPONSE.data)
            let guideline = checkGuidelines(RESPONSE)

            if (guideline) {
                document.querySelector("#guidelines").checked = true
            } else {
                document.querySelector("#guidelines").checked = false
            }
        }
    } catch (e) {
        console.log('error in getting string', e)
    }

}

function displayAPIResults(res) {
    let tableDiv = document.querySelector("#analyzeResults")
    let table = document.createElement('table')
    // table.id = "addressTable"
    let tblBody = document.createElement('tbody')

    // create one cell for each ingredient line
    for (let i = 0; i < showAddresses.length; i++) {
        // creates a table row
        const row = document.createElement("tr");
        const cell = document.createElement("td");
        const cellText = document.createTextNode(showAddresses[i].fullAddress);
        cell.dataset.id = i
        cell.appendChild(cellText);
        row.appendChild(cell);

        tblBody.appendChild(row);
    }
    // put no address found if results returned empty
    if (showAddresses.length == 0) {
        const row = document.createElement("tr");
        const cell = document.createElement("td");
        const cellText = document.createTextNode("No address found");
        table.className = "noPointer"
        cell.dataset.id = "none"
        cell.appendChild(cellText);
        row.appendChild(cell);

        tblBody.appendChild(row);
    }
    table.appendChild(tblBody)
    tableDiv.appendChild(table)
    return table
}

function checkGuidelines(res) {
    // all guidelines are less than or equal to except for fiber and protein which is greater than or equal to
    const ENTREE_FAT = 10 // in g
    const ENTREE_SAT_FAT = 5 // in g
    const ENTREE_FIBER = 2 // in g
    const ENTREE_PROTEIN = 10 // in g
    const ENTREE_SODIUM = 960 // in mg

    const SIDE_FAT = 5 // in g
    const SIDE_SAT_FAT = 2 // in g
    const SIDE_FIBER = 2 // greater than or equal to in g
    const SIDE_SODIUM = 360 // in mg

    const SOUP_FAT = 3 // in g
    const SOUP_FIBER = 2 // in g
    const SOUP_SODIUM = 720 // in mg



    // console.log('fat ' + res.totalNutrients.FAT.quantity)
    // console.log('saturated fat ' + res.totalNutrients.FASAT.quantity)
    // console.log('fiber ' + res.totalNutrients.FIBTG.quantity)
    // console.log('protein ' + res.totalNutrients.PROCNT.quantity)
    // console.log('sodium ' + res.totalNutrients.NA.quantity)

    // what kind of dish is this, 1 is entree, 2 is side 3 is soup
    const DISH = document.querySelector('input[name="categories"]:checked').value
    let selectedDish = ''
    if (DISH == 1) {
        selectedDish = 'ENTREE'
    } else if (DISH == 2) {
        selectedDish = 'SIDE'
    } else {
        selectedDish = 'SOUP'
    }

    // check if recipe follows guidelines
    // divide the result by the number of servings
    num_servings = document.querySelector("#num_servings").value
    if (res.totalNutrients.FAT.quantity / num_servings <= eval(`${selectedDish}_FAT`) &&
        res.totalNutrients.FIBTG.quantity / num_servings >= eval(`${selectedDish}_FIBER`) &&
        res.totalNutrients.NA.quantity / num_servings <= eval(`${selectedDish}_SODIUM`)) {

        if (DISH == 3) {
            return true
        } else if (DISH == 2 && res.totalNutrients.FASAT.quantity / num_servings <= eval(`${selectedDish}_SAT_FAT`)) {
            return true
        } else if (DISH == 1 && res.totalNutrients.FASAT.quantity / num_servings <= eval(`${selectedDish}_SAT_FAT`) &&
            res.totalNutrients.PROCNT.quantity / num_servings >= eval(`${selectedDish}_PROTEIN`)) {
            return true
        } else {
            return false
        }
    } else {
        return false
    }
}