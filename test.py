import func
from flask import url_for
import requests


func.init_db()

# func.add_new_place_to_db(
#     "Приморский",
#     "Граффити",
#     "Граффити на Маршала Новикова",
#     "grafitti_marshal_novikov.jpg",
#     "улица Маршала Новикова, 1",
#     "классное граффити",
#     "60.009004, 30.267979"
# )
#
# func.add_new_place_to_db(
#     "Центральный",
#     "Покупки",
#     "Лофт проект Этажи",
#     "floors.jpg",
#     "Лиговский проспект, 74",
#     "Торгово-выставочный центр в Санкт-Петербурге, первый и самый известный такого рода комплекс в Санкт-Петербурге, функционирующий в лофте - бывшем фабричном помещении.",
#     "59.921880, 30.356367"
# )

# for place in func.get_places():
#     print(place[4])
#
#
# #
# # #
# # # # # func.update_user_fav_places_id("fedor", "")
# # func.update_user_fav_places_id("admin", "1")
# func.update_user_fav_places_id("admin", "2")
# # # #
# # # # print(func.get_all_users())
# print(func.get_user_info("admin"))

func.add_new_place_to_db(
    "Приморский",
    "Волейбол",
    "Волейбольная площадка парка Озеро Долгое",
    "volleyball_park_oz_dolgoe.jpg",
    "парк Озеро Долгое",
    "Играйте в волейбол!",
    "60.01667, 30.26368"
)

func.add_new_place_to_db(
    "Приморский",
    "Волейбол",
    "Волейбольная площадка школы номер 595",
    "volleyball.jpg",
    "проспект Королева, 47",
    "Играйте в волейбол!",
    "60.02268, 30.25538"
)

func.add_new_place_to_db(
    "Приморский",
    "Волейбол",
    "Волейбольная площадка школы номер 579",
    "volleyball.jpg",
    "проспект Авиаконструкторов, 21",
    "Играйте в волейбол!",
    "60.01826, 30.2421"
)

func.add_new_place_to_db(
    "Приморский",
    "Волейбол",
    "Волейбольная площадка на Стародеревенской",
    "volleyball_staroderevenskay.jpg",
    "улица Стародеревенская, 24",
    "Играйте в волейбол!",
    "60.00113, 30.24317"
)


# import func
#
#
# func.delete_place("Волейбольная площадка парка Озеро Долгое")
# func.delete_place("Волейбольная площадка школы номер 595")
# func.delete_place("Волейбольная площадка школы номер 579")
# func.delete_place("Волейбольная площадка на Стародеревенской")