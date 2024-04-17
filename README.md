# The_Invasion_of_Aliens_Game

The_Invasion_of_Aliens_Game - это компьютерная мини-игра в стиле космической 2D стрелялки.

Игра содержит 9 уровней. С увеличением уровня увеличивается количество инопланетных захатчиков, которых надо поразить ракетой из космического корабля.
![Без имени](https://github.com/borshcheed13/The_Invasion_of_Aliens_Game/assets/158568211/ee7efbd8-095c-4527-9cce-c986b7c87229)
![Без имени1](https://github.com/borshcheed13/The_Invasion_of_Aliens_Game/assets/158568211/62dc7063-8688-410d-89f2-98eff358cb09)



Особенности игры:

- ♦ существует рейтинг игрока, для чего необходимо перед стартом игры ввести имя, подсчет очков идет автоматически;
- ♦ рейтинг игрока будет внесен в таблицу "лучших 10 игроков". Данные таблицы перезаписываются после проигрыша или прохождения всех 9 уровней игры в JSON-файл;
- ♦ невозможно выпустить вторую ракету из космического корабля до детонации уже запущенной или "вылета" ее за пределы игрового поля;
- ♦ управление игрой с помощью клавиш (на окне игры управление дублируется):
  - • esc - выход из игры в любой момент игры
  - • ← - движение космического корабля влево
  - • → - движение космического корабля вправо
  - • space - выстрел космического корабля ракетой


## Установка

1. Код игры писался на Python 3.12
2. GUI - встроенный пакет tkinter
3. Обработка png-изображений с помощью пакета pillow 10.2.0
4. Для считывания размеров экрана применялся пакет screeninfo 0.8.1
5. Применялись встроенные пакеты random, time, json

## Поддержка

Если у вас есть замечания или рекомендации к моей работе, прошу вас написать сообщение в обсуждении:
https://github.com/borshcheed13/The_Invasion_of_Aliens_Game/discussions/1

## В части подготовки резюме:

- Код писался согласно парадигмы Объектно-Ориентированного Программирования.
- Описаны классы ряда объектов с их поведением и взаимосвязью между собой.
- Экземпляры классов (инопланетяне, ракета, имитация взрыва) имитируют движение в процессе игры, фон игры меняется в зависимости от уровня.
- Применена логика последовательности создания экземпляров классов в определенный момент игры.
- Предусмотрен рейтинг игрока, сравнение рейтинга игрока с выдуманными игроками, считывание и запись данных в файле в формате JSON


