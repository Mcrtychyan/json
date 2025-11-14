import pytest
import json
import os
from task_manager import load_tasks, save_tasks, view_tasks, add_task, delete_task, FILENAME

class TestLoadTasks:

    def test_load_tasks_when_file_not_exists(self):
        if os.path.exists(FILENAME):
            os.remove(FILENAME)

        result = load_tasks()
        assert result == []

    def test_load_tasks_when_file_empty(self):
        with open(FILENAME, 'w', encoding='utf-8') as f:
            f.write('')

        result = load_tasks()
        assert result == []

    def test_load_tasks_with_valid_data(self):
        test_data = [
            {"title": "Купить молоко", "priority": "Высокий"},
            {"title": "Сделать уроки", "priority": "Средний"}
        ]
        with open(FILENAME, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, ensure_ascii=False)

        result = load_tasks()
        assert result == test_data
        assert len(result) == 2


class TestSaveTasks:

    def test_save_tasks_creates_file(self):
        tasks = [{"title": "Тест", "priority": "Низкий"}]
        save_tasks(tasks)
        assert os.path.exists(FILENAME)

    def test_save_tasks_stores_correct_data(self):
        tasks = [
            {"title": "Задача 1", "priority": "Высокий"},
            {"title": "Задача 2", "priority": "Низкий"}
        ]
        save_tasks(tasks)

        with open(FILENAME, 'r', encoding='utf-8') as f:
            saved_data = json.load(f)

        assert saved_data == tasks


class TestViewTasks:

    def test_view_tasks_empty_list(self, capsys):
        tasks = []
        view_tasks(tasks)
        captured = capsys.readouterr()
        assert "Список задач пуст." in captured.out

    def test_view_tasks_with_tasks(self, capsys):
        tasks = [
            {"title": "Учеба", "priority": "Высокий"},
            {"title": "Отдых", "priority": "Низкий"}
        ]
        view_tasks(tasks)
        captured = capsys.readouterr()
        assert "Учеба" in captured.out
        assert "Отдых" in captured.out


class TestAddTask:

    def test_add_task_success(self, monkeypatch):
        tasks = []
        inputs = ["Новая задача", "Средний"]
        monkeypatch.setattr('builtins.input', lambda _: inputs.pop(0))

        def mock_save(tasks_list):
            pass

        monkeypatch.setattr('task_manager.save_tasks', mock_save)
        add_task(tasks)

        assert len(tasks) == 1
        assert tasks[0]["title"] == "Новая задача"
        assert tasks[0]["priority"] == "Средний"


class TestDeleteTask:

    def test_delete_task_empty_list(self, capsys):
        tasks = []
        delete_task(tasks)
        captured = capsys.readouterr()
        assert "Нет задач для удаления." in captured.out

    def test_delete_task_success(self, monkeypatch, capsys):
        tasks = [
            {"title": "Первая", "priority": "Высокий"},
            {"title": "Вторая", "priority": "Низкий"}
        ]
        monkeypatch.setattr('builtins.input', lambda _: "1")

        def mock_save(tasks_list):
            pass

        def mock_view(tasks_list):
            print("Список задач показан")

        monkeypatch.setattr('task_manager.save_tasks', mock_save)
        monkeypatch.setattr('task_manager.view_tasks', mock_view)
        delete_task(tasks)
        captured = capsys.readouterr()

        assert len(tasks) == 1
        assert tasks[0]["title"] == "Вторая"
        assert "Задача удалена" in captured.out

    def test_delete_task_invalid_number(self, monkeypatch, capsys):
        tasks = [{"title": "Задача", "priority": "Средний"}]
        monkeypatch.setattr('builtins.input', lambda _: "5")

        def mock_view(tasks_list):
            print("Список показан")

        monkeypatch.setattr('task_manager.view_tasks', mock_view)
        delete_task(tasks)
        captured = capsys.readouterr()

        assert "Некорректный номер задачи." in captured.out
        assert len(tasks) == 1

    def test_delete_task_not_number(self, monkeypatch, capsys):
        tasks = [{"title": "Задача", "priority": "Средний"}]
        monkeypatch.setattr('builtins.input', lambda _: "abc")

        def mock_view(tasks_list):
            print("Список показан")

        monkeypatch.setattr('task_manager.view_tasks', mock_view)
        delete_task(tasks)
        captured = capsys.readouterr()

        assert "Ошибка: введите корректный номер." in captured.out
        assert len(tasks) == 1

@pytest.fixture
def sample_tasks():
    return [
        {"title": "Задача 1", "priority": "Высокий"},
        {"title": "Задача 2", "priority": "Низкий"}
    ]


@pytest.fixture
def clean_file():
    if os.path.exists(FILENAME):
        os.remove(FILENAME)
    yield
    if os.path.exists(FILENAME):
        os.remove(FILENAME)

def test_save_and_load_integration(clean_file, sample_tasks):
    save_tasks(sample_tasks)
    loaded_tasks = load_tasks()
    assert loaded_tasks == sample_tasks


def test_add_and_view_integration(monkeypatch, capsys, clean_file):
    tasks = []
    inputs = ["Тест задача", "Высокий"]
    monkeypatch.setattr('builtins.input', lambda _: inputs.pop(0))

    def mock_save(tasks_list):
        pass

    monkeypatch.setattr('task_manager.save_tasks', mock_save)

    add_task(tasks)
    view_tasks(tasks)
    captured = capsys.readouterr()

    assert "Тест задача" in captured.out
    assert "Высокий" in captured.out