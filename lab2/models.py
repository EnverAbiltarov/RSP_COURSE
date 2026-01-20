from pydantic import BaseModel


class Accessory(BaseModel):
    name: str
    price: float


class Flower(BaseModel):
    name: str
    color: str
    freshness_level: int # from 1 to 10
    stem_length: float
    price: float


class RoseFlower(Flower):
    thorns: bool


class TulipFlower(Flower):
    type_of_tulip: str


class LilyFlower(Flower):
    pollen_free: bool


class Bouquet(BaseModel):
    accessories: list[Accessory]
    flowers: list[Flower]

    @property
    def name(self) -> str:
        return f"Букет из {len(self.flowers)} цветов"

    @property
    def flowers_colors_count(self) -> dict[str, int]:
        flowers_colors = [flower.color for flower in self.flowers]
        flowers_colors_set = set()

        for color in flowers_colors:
            flowers_colors_set.add(color)

        dict_colors = {}

        for color in flowers_colors_set:
            dict_colors[color] = flowers_colors.count(color)

        return dict_colors


    @property
    def price(self) -> int:
        price = 0

        for flower in self.flowers:
            price += flower.price

        for accessory in self.accessories:
            price += accessory.price

        return price

    def sort_by_freshness(self, descending: bool = True) -> None:
        """Сортирует цветы в букете по уровню свежести."""
        self.flowers.sort(key=lambda flower: flower.freshness_level, reverse=descending)


    def find_flowers_by_stem(self, minimal, maximum) -> list[Flower]:
        return [
            flower
            for flower in self.flowers
            if minimal <= flower.stem_length <= maximum
        ]


    def __repr__(self) -> str:
        return f"""
Букет: {self.name}
Цвет: {self.color}
Аксессуары: {self.accessories}
Цветы: {self.flowers}
"""
