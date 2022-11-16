import attr

from buruaka.models.abc import JsonObject
from buruaka.models.base import BlueArchiveObject
from buruaka.models.enums import ArmorType, DamageType, Position, Role, CharacterType, Weapon, School, TerrainMood
from buruaka.types import JSON, Stars


@attr.s
class TerrainData(JsonObject):
    """
    Student Terrain
    """
    damageDealt: int = attr.field()
    shieldBlockRate: int = attr.field()

    @classmethod
    def from_json(cls, data: JSON) -> "TerrainData":
        return cls(
            damageDealt=int(data["DamageDealt"].split("%")[0]),
            shieldBlockRate=int(data["ShieldBlockRate"].split("%")[0])
        )

    def to_json(self) -> JSON:
        damageDealt: str = "(1.0x)" if self.damageDealt == 100 else f"({self.damageDealt/100:.1}x)"
        return {
            "DamageDealt": f"{self.damageDealt}%{damageDealt}",
            "ShieldBlockRate": f"{self.shieldBlockRate}%"
        }


@attr.s
class TerrainObject(JsonObject):
    """
    Wrapper object to hold 3 types of TerrainData.
    """
    indoor: TerrainData = attr.field()
    outdoor: TerrainData = attr.field()
    urban: TerrainData = attr.field()

    @classmethod
    def from_json(cls, data: JSON) -> "TerrainObject":
        return cls(
            indoor=TerrainData.from_json(data["indoor"]),
            outdoor=TerrainData.from_json(data["outdoor"]),
            urban=TerrainData.from_json(data["urban"])
        )

    def to_json(self) -> JSON:
        return {
            "indoor": self.indoor.to_json(),
            "outdoor": self.outdoor.to_json(),
            "urban": self.urban.to_json()
        }


@attr.s
class Student(BlueArchiveObject):
    """
    Blue Archive Student Object.
    """
    baseStar: Stars = attr.field(repr=lambda stars: "★"*stars)
    rarity: str = attr.field(repr=True)
    name: str = attr.field(repr=True)
    profile: str = attr.field(repr=False)
    armorType: ArmorType = attr.field(repr=True)
    bulletType: DamageType = attr.field(repr=True)
    position: Position = attr.field(repr=True)
    role: Role = attr.field(repr=True)
    squadType: CharacterType = attr.field(repr=True)
    weaponType: Weapon = attr.field(repr=True)
    terrain: TerrainObject = attr.field(repr=True)

    @classmethod
    def from_json(cls, data: JSON) -> "Student":
        return cls(
            id=data["id"],
            baseStar=int(data["baseStar"]),
            rarity=data["rarity"],
            name=data["name"],
            profile=data["profile"],
            armorType=ArmorType(data["armorType"]),
            bulletType=DamageType[data["bulletType"]],
            position=Position(data["position"]),
            role=Role(data["role"]),
            squadType=CharacterType(data["squadType"]),
            weaponType=Weapon(data["weaponType"]),
            terrain=TerrainObject.from_json(data["terrain"])
        )

    def to_json(self) -> JSON:
        return {
            "id": self.id,
            "baseStar": self.baseStar,
            "rarity": self.rarity,
            "name": self.name,
            "profile": self.profile,
            "armorType": self.armorType.value,
            "bulletType": self.bulletType.value,
            "position": self.position.value,
            "role": self.role.value,
            "squadType": self.squadType.value,
            "weaponType": self.weaponType.value,
            "terrain": self.terrain.to_json()
        }


GRADE_EXPR = ["1st", "2nd", "3rd"]  # just hard-code it. maybe there is a better way, but leave it for now.


@attr.s
class StudentInfo(JsonObject):
    age: str = attr.field()
    artist: str = attr.field()
    club: str = attr.field()
    school: School = attr.field()
    schoolYear: str = attr.field()
    voiceActor: str = attr.field()

    @classmethod
    def from_json(cls, data: JSON) -> "StudentInfo":
        return cls(
            age=data["age"].replace(" years old", ""),
            artist=data["artis"],    # why this field name is 'artis'?
            club=data["club"],
            school=School(data["school"]),
            schoolYear=data["schoolYear"],
            voiceActor=data["voiceActor"]
        )

    def to_json(self) -> JSON:
        return {
            "age": self.ageText,
            "artis": self.artist,
            "club": self.club,
            "school": self.school.name,
            "schoolYear": self.schoolYear,
            "voiceActor": self.voiceActor
        }

    @property
    def ageText(self) -> str:
        return f"{self.age} years old."


@attr.s
class Skill(JsonObject):
    bulletType: DamageType = attr.field()
    description: str = attr.field()
    level: int = attr.field()
    name: str = attr.field()
    skillCost: int = attr.field()

    @classmethod
    def from_json(cls, data: JSON) -> "Skill":
        return cls(
            bulletType=DamageType[data["bulletType"]],
            description=data["description"],
            level=data["level"],
            name=data["name"],
            skillCost=data["skillCost"]
        )

    def to_json(self) -> JSON:
        return {
            "bulletType": self.bulletType.name,
            "description": self.description,
            "level": self.level,
            "name": self.name,
            "skillCost": self.skillCost
        }


@attr.s
class StudentSkills(JsonObject):
    ex: list[Skill] = attr.field(factory=list)
    normal: list[Skill] = attr.field(factory=list)
    passive: list[Skill] = attr.field(factory=list)
    sub: list[Skill] = attr.field(factory=list)

    @classmethod
    def from_json(cls, data: JSON) -> "StudentSkills":
        return cls(
            ex=list(map(Skill.from_json, data["ex"])),
            normal=list(map(Skill.from_json, data["normal"])),
            passive=list(map(Skill.from_json, data["passive"])),
            sub=list(map(Skill.from_json, data["sub"]))
        )

    def to_json(self) -> JSON:
        return {
            "ex": list(map(lambda s: s.to_json(), self.ex)),
            "normal": list(map(lambda s: s.to_json(), self.normal)),
            "passive": list(map(lambda s: s.to_json(), self.passive)),
            "sub": list(map(lambda s: s.to_json(), self.sub))
        }


@attr.s
class StudentStat(BlueArchiveObject):
    ammoCost: int = attr.field()
    ammoCount: int = attr.field()

    attackLevel1: int = attr.field()
    attackLevel100: int = attr.field()

    defPenetrateLevel1: int = attr.field()
    defPenetrateLevel100: int = attr.field()

    defenseLevel1: int = attr.field()
    defenseLevel100: int = attr.field()

    healPowerLevel1: int = attr.field()
    healPowerLevel100: int = attr.field()

    maxHPLevel1: int = attr.field()
    maxHPLevel100: int = attr.field()

    moveSpeed: int = attr.field()
    range: int = attr.field()

    indoorMood: TerrainMood = attr.field()
    outdoorMood: TerrainMood = attr.field()
    streetMood: TerrainMood = attr.field()

    @classmethod
    def from_json(cls, data: JSON) -> "StudentStat":
        return cls(
            id=data["id"],
            ammoCost=data["ammoCost"],
            ammoCount=data["ammoCount"],
            attackLevel1=data["attackLevel1"],
            attackLevel100=data["attackLevel100"],
            defPenetrateLevel1=data["defPenetrateLevel1"],
            defPenetrateLevel100=data["defPenetrateLevel100"],
            defenseLevel1=data["defenseLevel1"],
            defenseLevel100=data["defenseLevel100"],
            healPowerLevel1=data["healPowerLevel1"],
            healPowerLevel100=data["healPowerLevel100"],
            maxHPLevel1=data["maxHPLevel1"],
            maxHPLevel100=data["maxHPLevel100"],
            moveSpeed=data["moveSpeed"],
            range=data["range"],
            indoorMood=TerrainMood[data["indoorMood"]],
            outdoorMood=TerrainMood[data["outdoorMood"]],
            streetMood=TerrainMood[data["streetMood"]]
        )

    def to_json(self) -> JSON:
        return {
            "id": self.id,
            "ammoCost": self.ammoCost,
            "ammoCount": self.ammoCount,
            "attackLevel1": self.attackLevel1,
            "attackLevel100": self.attackLevel100,
            "defPenetrateLevel1": self.defPenetrateLevel1,
            "defPenetrateLevel100": self.defPenetrateLevel100,
            "defenseLevel1": self.defenseLevel1,
            "defenseLevel100": self.defenseLevel100,
            "healPowerLevel1": self.healPowerLevel1,
            "healPowerLevel100": self.healPowerLevel100,
            "maxHpLevel1": self.maxHpLevel1,
            "maxHpLevel100": self.maxHpLevel100,
            "moveSpeed": self.moveSpeed,
            "range": self.range,
            "indoorMood": self.indoorMood.name,
            "outdoorMood": self.outdoorMood.name,
            "streetMood": self.streetMood.name
        }


@attr.s
class StudentDetails(BlueArchiveObject):
    """
    Blue Archive "Detailed" Student Object.
    """
    stu: Student = attr.field()
    info: StudentInfo = attr.field()
    skills: StudentSkills = attr.field()
    stat: StudentStat = attr.field()
    terrain: TerrainObject = attr.field()
    isPlayable: bool = attr.field(default=False)
    isReleased: bool = attr.field(default=False)

    @classmethod
    def from_json(cls, data: JSON) -> "StudentDetails":
        stu = data.pop("character")
        stu["id"] = data["id"]
        stu["terrain"] = data["terrain"]
        stuObj = Student.from_json(stu)

        stat = data["stat"]
        stat["id"] = data["id"]
        return cls(
            id=data["id"],
            stu=stuObj,
            info=StudentInfo.from_json(data["info"]),
            isPlayable=data["isPlayable"],
            isReleased=data["isReleased"],
            skills=StudentSkills.from_json(data["skills"]),
            stat=StudentStat.from_json(stat),
            terrain=stuObj.terrain                  # just reference it.
        )

    def to_json(self) -> JSON:
        stu_json: JSON = self.stu.to_json()
        terrain_json: JSON = stu_json.pop("terrain")
        stu_id: int = stu_json.pop("id")
        return {
            "id": stu_id,
            "character": stu_json,
            "info": self.info.to_json(),
            "isPlayable": self.isPlayable,
            "isReleased": self.isReleased,
            "terrain": terrain_json
        }