#ссылочная модель данных:основной принцип-копируются ссылки, а не объекты
#a[0]*5 -->5 ссылок на один и тот ж еобъект
#[a[0]*5]*5- создали 5 ссылок на один список= создали матрицу
#listcomprehentions конструкция в списке, в которой можем писать списки и условия
#инкапсуляция=реализация,скрытие логики внутри класса,ограничение доступа к составляющим объекта
#полимоорфизм-возможность переопределить конструкцию языка для каждого класса


class MyClass:
    pass
object=MyClass()

print(type(object))

class Ork:
    #метод инициализации класса(конструктор)
    def __init__(self, level:int)->None: #дандр метод(__) магический метод определяет как будет
                             # вести себя объект класса с разными конструкциями языка
        self.level=level        #self-экземпляр класса который мы передаём в метод класса(ссылка)
        self.health_points = 100*level
        self.attack_power = 10 * level

    def attack(self):
        print(f"Ork attacks with {self.attack_power} power")

    def __str__(self):
        return f"Ork level: {self.level}, health: {self.health_points}"

ork=Ork(level=2)
ork.level+=1 #можно менять атрибуты класса
print(ork)

ork.attack()
#Ork.attack() <-- ERROR нет экземпляра класса

#Наследование(решает проблему копирования)

class Elf:
    def __init__(self, level:int)->None:
        self.level=level
        self.health_points = 50*level
        self.attack_power = 15*level

    def attack(self):
        print(f"Elf attacks with {self.attack_power} power")

    def __str__(self)->str:
        return f"Elf level: {self.level}, health: {self.health_points}"

class Character:
    def __init__(self, level:int)->None:
        self.level=level
        self.health_points = self.base_health_points *level
        self.attack_power = self.base_attack_power * level

    def attack(self, *,target:"Character")->None:#добавляем цель атакуемую
        #до инкапсуляции
        #print(f"{self.character_name} attacks {target.character_name} ({target.health_points} health_points)"
        #f" with {self.attack_power} power. "
              #)
        #target.health_points -= self.attack_power
        #print(f"After attack {target.character_name} hp has {target.health_points}")

        # после инкапсуляции
        target.got_damage(damage=self.attack_power)

    def got_damage(self, *,damage:int)->None:
        damage = damage * (100-self.defence) /100
        damage=round(damage)
        self.health_points -= damage


    def is_alive(self)->bool:
        return self.health_points > 0

    #определим защиту как свойство класса
    @property #декоратор
    def defence(self):
        defence = self.base_defence * self.level
        return defence

    @property
    def max_health_points(self)->int:
        return self.level * self.base_health_points


    def health_points_persent(self):
        return self.health_points // self.max_health_points

    def __str__(self)->str:
        return f"{self.character_name} (level: {self.level}, health: {self.health_points})"


class Ork(Character):
    base_health_points = 100
    base_attack_power = 10
    character_name = "Ork"
    base_character_name = "Ork"
    base_defence = 15

    @property
    def defence(self)-> int:
        defence = super().defence #обращение к классу наследника с помощью супер
        if self.health_points < 50:
            defence=
        return defence
class Elf(Character):
    base_health_points = 50
    base_attack_power=15
    character_name = "Elf"

    #можем переопределять методы
    #def attack(self):
        #print("This method is from class inheritor")

#elf1=Elf(level=3)
#elf1.attack()


def fight(*, character_1:Character, character_2:Character)->None:
    while character_1.is_alive() and character_2.is_alive():
        character_1.attack(target=character_2)
        if character_2.is_alive():
            character_2.attack(target=character_1)

    print(f"Character 1:{character_1}, is_alive {character_1.is_alive()}")
    print(f"Character 2:{character_2}, is_alive {character_2.is_alive()}")

ork = Ork(level=1)
elf = Elf(level=1)

fight(character_1=ork, character_2=elf)