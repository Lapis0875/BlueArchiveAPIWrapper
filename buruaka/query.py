from typing import Self

import attr

from buruaka.models.enums import Role, CharacterType, School, Position, Weapon, DamageType, ArmorType


@attr.s
class BuruakaQuery:
    """
    Query object to specify which student to get.
    """
    role: Role | None = attr.field(default=None)
    type: CharacterType | None = attr.field(default=None)
    school: School | None = attr.field(default=None)
    position: Position | None = attr.field(default=None)
    weapon: Weapon | None = attr.field(default=None)
    damage: DamageType | None = attr.field(default=None)
    armor: ArmorType | None = attr.field(default=None)

    def Role(self, role: Role) -> Self:
        self.role = role
        return self

    def Type(self, type: CharacterType) -> Self:
        self.type = type
        return self

    def School(self, school: School) -> Self:
        self.school = school
        return self

    def Position(self, position: Position) -> Self:
        self.position = position
        return self

    def Weapon(self, weapon: Weapon) -> Self:
        self.weapon = weapon
        return self

    def Damage(self, damage: DamageType) -> Self:
        self.damage = damage
        return self

    def Armor(self, armor: ArmorType) -> Self:
        self.armor = armor
        return self

    def build(self) -> str:
        queries: list[str] = []
        if self.role is not None:
            queries.append(f"role={self.role.value}")
        if self.type is not None:
            queries.append(f"type={self.type.value}")
        if self.school is not None:
            queries.append(f"school={self.school.value}")
        if self.position is not None:
            queries.append(f"position={self.position.value}")
        if self.weapon is not None:
            queries.append(f"weapon={self.weapon.value}")
        if self.damage is not None:
            queries.append(f"damage={self.damage.value}")
        if self.armor is not None:
            queries.append(f"armor={self.armor.value.replace(' ', '%20')}")
        return "/query?" + "&".join(queries)
