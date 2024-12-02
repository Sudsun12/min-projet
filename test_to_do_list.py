import unittest
from to_do_list import TodoList

class TestTodoList(unittest.TestCase):

    def setUp(self):
        """Initialisation avant chaque test"""
        self.todo_list = TodoList()
        self.todo_list.tasks = {}  # Réinitialiser les tâches pour chaque test

    def test_add_task(self):
        """Test de l'ajout d'une tâche"""
        task_id = self.todo_list.add_task("Test Task", "Description", "one", "2023-12-31")
        self.assertIn(str(task_id), self.todo_list.tasks)
        self.assertEqual(self.todo_list.tasks[str(task_id)]['title'], "Test Task")

    def test_complete_task(self):
        """Test de la complétion d'une tâche"""
        task_id = self.todo_list.add_task("Test Task", "Description", "one", "2023-12-31")
        self.todo_list.complete_task(task_id)
        self.assertTrue(self.todo_list.tasks[str(task_id)]['completed'])

    def test_delete_task(self):
        """Test de la suppression d'une tâche"""
        task_id = self.todo_list.add_task("Test Task", "Description", "one", "2023-12-31")
        self.todo_list.delete_task(task_id)
        self.assertNotIn(str(task_id), self.todo_list.tasks)

    def test_search_task_by_title(self):
        """Test de la recherche de tâche par titre"""
        self.todo_list.add_task("Test Task", "Description", "one", "2023-12-31")
        results = self.todo_list.search_task_by_title("Test")
        self.assertEqual(len(results), 1)
        self.assertIn("Test Task", [task['title'] for task in results.values()])

if __name__ == '__main__':
    unittest.main() 