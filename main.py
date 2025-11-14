import json
import os

FILENAME = "tasks.json"


def load_tasks():
    """
    Загружает список задач из JSON файла.

    Что должен сделать студент:
    1. Проверить, существует ли файл:
           os.path.exists(FILENAME)
    2. Если файла нет — вернуть пустой список: return []
    3. Если файл есть:
           - открыть его через: with open(FILENAME, "r", encoding="utf-8") as f
           - загрузить данные с помощью: json.load(f)
    4. Вернуть список задач.

    Возможные проблемы, которые студент должен учитывать:
    - файл может быть пустым → тогда json.load может вызвать ошибку
      это можно обработать через try/except или просто создавать файл заранее123123
    """
    if not os.path.exists(FILENAME):
        return []

    try:
        with open(FILENAME, "r", encoding="utf-8") as f:
            tasks = json.load(f)
        return tasks
    except (json.JSONDecodeError, Exception):
        return []



def save_tasks(tasks):
    """
    Сохраняет список задач tasks в JSON файл.

    Что должен сделать студент:
    1. Открыть файл на запись:
           with open(FILENAME, "w", encoding="utf-8") as f
    2. Использовать json.dump(tasks, f, ensure_ascii=False, indent=4)

    Подсказки:
    - ensure_ascii=False → чтобы русские буквы сохранились читаемыми
    - indent=4 → красивое форматирование JSON
    """
    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)



def view_tasks(tasks):
    """
    Выводит список задач на экран.

    Что должен сделать студент:
    1. Если задач нет: вывести строку:
           "Список задач пуст."
    2. Если задачи есть:
           - Использовать enumerate(tasks, start=1) чтобы получить номера
           - Напечатать в формате:
                 1. Купить продукты — [Высокий]

    Подсказки:
    - Каждая задача — это словарь вида:
          {"title": "...", "priority": "..."}
    - Вывести нужно так:
          print(f"{номер}. {task['title']} — [{task['priority']}]")
    """
    if not tasks:
        print("Список задач пуст.")
        return

    for i, task in enumerate(tasks, start=1):
        print(f"{i}. {task['title']} — [{task['priority']}]")




def add_task(tasks):
    """
    Добавляет новую задачу в список.

    Что должен сделать студент:
    1. Спросить название задачи:
           title = input("Введите название задачи: ")
    2. Спросить приоритет:
           priority = input("Введите приоритет (Низкий/Средний/Высокий): ")
    3. Создать объект задачи:
           task = {"title": title, "priority": priority}
    4. Добавить его в список:
           tasks.append(task)
    5. Сохранить обновлённый список:
           save_tasks(tasks)
    6. Вывести подтверждение:
           "Задача добавлена."

    Важно:
    - Приоритет можно не валидировать, это учебная версия.
    """
    title = input("Введите название задачи: ")
    priority = input("Введите приоритет (Низкий/Средний/Высокий): ")
    task = {"title": title, "priority": priority}
    tasks.append(task)
    save_tasks(tasks)
    print('Задача добавлена')



def delete_task(tasks):
    """
    Удаляет задачу по её номеру.

    Что должен сделать студент:

    1. Если список пуст → вывести:
           "Нет задач для удаления."
       и выйти из функции.
    2. Показать текущие задачи (можно вызвать view_tasks(tasks)).
    3. Спросить номер для удаления:
           number = input("Введите номер задачи: ")
    4. Преобразовать ввод в число:
           num = int(number)

       ⚠ ВАЖНО: это нужно обернуть в try/except, чтобы отловить ValueError,
       если пользователь введёт строки типа "abc".

    5. Проверить, что номер в правильном диапазоне:
           1 <= num <= len(tasks)

       Если номер неправильный:
           вывести: "Некорректный номер задачи."
           и выйти из функции.

    6. Удалить задачу:
           tasks.pop(num - 1)

    7. Сохранить обновлённый список:
           save_tasks(tasks)

    8. Вывести:
           "Задача удалена."
    """
    if not tasks:
        print("Нет задач для удаления.")
        return

    view_tasks(tasks)

    try:
        number = input("Введите номер задачи: ")
        num = int(number)

        if 1 <= num <= len(tasks):
            tasks.pop(num - 1)
            save_tasks(tasks)
            print('Задача удалена')
        else:
            print("Некорректный номер задачи.")

    except ValueError:
        print("Ошибка: введите корректный номер.")



def main():
    """
    Главная функция программы.123

    Что должен сделать студент:

    1. Загрузить задачи в начале:
           tasks = load_tasks()

    2. Запустить бесконечный цикл меню:
           while True:

    3. Напечатать меню:
           1 — Просмотреть задачи
           2 — Добавить задачу
           3 — Удалить задачу
           0 — Выход

    4. Считать выбор через input().

    5. В зависимости от выбора вызываются функции:
           if choice == "1": view_tasks(tasks)
           elif choice == "2": add_task(tasks)
           elif choice == "3": delete_task(tasks)
           elif choice == "0": break

    6. При неправильном вводе вывести:
           "Ошибка: такого пункта меню нет."

    """
    print("Добро пожаловать в менеджер задач!")

    tasks = load_tasks()

    while True:
        print("\nМеню:")
        print("1 — Просмотреть задачи")
        print("2 — Добавить задачу")
        print("3 — Удалить задачу")
        print("0 — Выход")

        choice = input("Выберите пункт меню: ")

        if choice == "1":
            view_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            delete_task(tasks)
        elif choice == "0":
            print("Выход из программы.")
            break
        else:
            print("Ошибка: такого пункта меню нет. Попробуйте снова.")


if __name__ == "__main__":
    main()
