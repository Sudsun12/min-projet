import unittest
from unittest.mock import patch
import sys
import io
from to_do_list import TodoList

# Rediriger stdin pour simuler les entrées utilisateur
@patch('sys.stdin', io.StringIO('7\n'))
class TestTodoList(unittest.TestCase):
    def setUp(self):
        """Initialisation avant chaque test"""
        self.todo = TodoList()
        self.sample_task = {
            'title': 'Test Task',
            'description': 'Test Description',
            'priority': 'one',
            'due_date': '2024-12-31',
            'completed': False
        }

    def test_add_task(self):
        """Test l'ajout d'une tâche"""
        task_id = self.todo.add_task(
            self.sample_task['title'],
            self.sample_task['description'],
            self.sample_task['priority'],
            self.sample_task['due_date']
        )
        self.assertIn(task_id, self.todo.tasks)
        self.assertEqual(self.todo.tasks[task_id]['title'], 'Test Task')

    def test_delete_task(self):
        """Test la suppression d'une tâche"""
        task_id = self.todo.add_task(
            self.sample_task['title'],
            self.sample_task['description'],
            self.sample_task['priority'],
            self.sample_task['due_date']
        )
        self.todo.delete_task(task_id)
        self.assertNotIn(task_id, self.todo.tasks)

    def test_complete_task(self):
        """Test le marquage d'une tâche comme complétée"""
        task_id = self.todo.add_task(
            self.sample_task['title'],
            self.sample_task['description'],
            self.sample_task['priority'],
            self.sample_task['due_date']
        )
        self.todo.complete_task(task_id)
        self.assertTrue(self.todo.tasks[task_id]['completed'])

    def test_search_task_by_title(self):
        """Test la recherche de tâches par titre"""
        task_id = self.todo.add_task(
            self.sample_task['title'],
            self.sample_task['description'],
            self.sample_task['priority'],
            self.sample_task['due_date']
        )
        found_tasks = self.todo.search_task_by_title('Test')
        self.assertIn(task_id, found_tasks)
        found_tasks = self.todo.search_task_by_title('Nonexistent')
        self.assertEqual(len(found_tasks), 0)

    def test_update_task(self):
        """Test la mise à jour d'une tâche"""
        task_id = self.todo.add_task(
            self.sample_task['title'],
            self.sample_task['description'],
            self.sample_task['priority'],
            self.sample_task['due_date']
        )
        updated_task = {
            'title': 'Updated Task',
            'description': 'Updated Description',
            'priority': 'two',
            'due_date': '2024-12-31'
        }
        self.todo.update_task(task_id, updated_task)
        self.assertEqual(self.todo.tasks[task_id]['title'], 'Updated Task')

    def test_invalid_priority(self):
        """Test l'ajout d'une tâche avec une priorité invalide"""
        with self.assertRaises(ValueError):
            self.todo.add_task(
                'Test Task',
                'Test Description',
                'invalid_priority',
                '2024-12-31'
            )

    def test_invalid_date_format(self):
        """Test l'ajout d'une tâche avec un format de date invalide"""
        with self.assertRaises(ValueError):
            self.todo.add_task(
                'Test Task',
                'Test Description',
                'one',
                'invalid_date'
            )

    def test_view_tasks(self):
        """Test l'affichage des tâches"""
        # Ajouter une tâche de test
        task_id = self.todo.add_task(
            self.sample_task['title'],
            self.sample_task['description'],
            self.sample_task['priority'],
            self.sample_task['due_date']
        )
        
        # Rediriger stdout pour capturer l'output
        stdout = io.StringIO()
        with patch('sys.stdout', stdout):
            tasks = self.todo.view_tasks()
            output = stdout.getvalue()
        
        # Vérifier que quelque chose a été affiché
        self.assertNotEqual(output.strip(), "")
        
        # Vérifier que les informations de la tâche sont présentes
        self.assertIn(str(task_id), output)
        self.assertIn(self.sample_task['title'], output)
        self.assertIn(self.sample_task['description'], output)
        
        # Vérifier le retour de la fonction
        self.assertIn(task_id, tasks)
        task = tasks[task_id]
        self.assertEqual(task['title'], self.sample_task['title'])
        self.assertEqual(task['description'], self.sample_task['description'])

if __name__ == '__main__':
    unittest.main()