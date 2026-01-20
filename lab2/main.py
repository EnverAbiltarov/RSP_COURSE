import random

from lab2.enums import FlowerColorEnum, TulipTypeEnum
from lab2.models import RoseFlower, TulipFlower, LilyFlower, Bouquet, Accessory


roses = []
tulips = []
lilyies = []

for i in range(5):
    roses.append(
        RoseFlower(
            name=f"Роза {i+1}",
            color=random.choice(list(FlowerColorEnum)),
            freshness_level=random.randint(1, 10),
            stem_length=random.randint(35, 60),
            price=random.randint(100, 250),
            thorns=random.choice([True, False])
        )
    )

    tulips.append(
        TulipFlower(
            name=f"Тюльпан {i+1}",
            color=random.choice(list(FlowerColorEnum)),
            freshness_level=random.randint(1, 10),
            stem_length=random.randint(35, 60),
            price=random.randint(50, 150),
            type_of_tulip=random.choice(list(TulipTypeEnum))
        )
    )

    lilyies.append(
        LilyFlower(
            name=f"Лилия {i+1}",
            color=random.choice(list(FlowerColorEnum)),
            freshness_level=random.randint(1, 10),
            stem_length=random.randint(15, 35),
            price=random.randint(50, 200),
            pollen_free=random.choice([True, False]),
        )
    )

bouquet = Bouquet(
    accessories=[
        Accessory(
            name="Упаковка",
            price=random.randint(500, 1500),
        ),
        Accessory(
            name="Упаковочная лента",
            price=random.randint(500, 1000),
        )
    ],
    flowers=[*roses, *tulips, *lilyies]
)

print("Букет до сортировки цветов")
print(bouquet)

print("")
print("Букет после сортировки цветов")
bouquet.sort_by_freshness()
print(bouquet)

print("")
print(f"Стоимость букета: {bouquet.price}")

selected_flowers = bouquet.find_flowers_by_stem(25, 45)

print("")
for flower in selected_flowers:
    print(flower)
