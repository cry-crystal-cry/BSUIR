# Лабораторная работа №2

В рамках лабораторной работы №2 было разработано приложение, которое предназначено для управления общественной работой студентов с помощью графического интерфейса и XML файлов.

## Описание функционала

### Главное окно

На главном окне приложения представлена таблица со всеми студентами, оконное меню с возможными действиями над студентами и панель с перелистыванием страниц и выбором, сколько студентов будет на странице:
> ![image](https://github.com/cry-crystal-cry/BSUIR/blob/master/4_sem/PPOIS/lab2/imgs/main.PNG)

Пример изменения количества отобразаемых записей на странице:

> ![image](https://github.com/cry-crystal-cry/BSUIR/blob/master/4_sem/PPOIS/lab2/imgs/page_change.PNG)


### Взаимодействие с файлами

Можно загрузить данные из уже существующего XML файла:

> ![image](https://github.com/cry-crystal-cry/BSUIR/blob/master/4_sem/PPOIS/lab2/imgs/load_from_xml.PNG)


Также можно сохранить текущие данные из приложения в XML файл:

> ![image](https://github.com/cry-crystal-cry/BSUIR/blob/master/4_sem/PPOIS/lab2/imgs/save_to_xml.PNG)


### Добавление студента

Можно добавить студента с помощью отдельного окна, после нажатия на кнопку "Добавить студента":

> ![image](https://github.com/cry-crystal-cry/BSUIR/blob/master/4_sem/PPOIS/lab2/imgs/add.PNG)

При неправильном вводе данных открывается соответсвующее сообщение об ошибке:

> ![image](https://github.com/cry-crystal-cry/BSUIR/blob/master/4_sem/PPOIS/lab2/imgs/add_error.PNG)

### Поиск студентов

Представлено 3 способа поиска студентов: 
- по фамилии
- по группе
- по фамилии и общественной работе
- по группе и общественной работе

> ![image](https://github.com/cry-crystal-cry/BSUIR/blob/master/4_sem/PPOIS/lab2/imgs/serch_choose.PNG)

После нажатия на кнопку "Поиск" в данном окне выводятся все студенты, которые удовлетворяют критериям поиска:

> ![image](https://github.com/cry-crystal-cry/BSUIR/blob/master/4_sem/PPOIS/lab2/imgs/search_examlpe.PNG)

### Удаление студентов

Удаление студентов возможно по тем же критериям, что и поиск:

> ![image](https://github.com/cry-crystal-cry/BSUIR/blob/master/4_sem/PPOIS/lab2/imgs/delete.PNG)

После нажатия на кнопку "Удалить" в данном окне появится сообщение о том, сколько студентов было удалено, сразу же после этого данные студенты исчезнут из главного окна

> ![image](https://github.com/cry-crystal-cry/BSUIR/blob/master/4_sem/PPOIS/lab2/imgs/delete_example.PNG)
