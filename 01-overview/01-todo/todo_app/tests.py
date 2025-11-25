from django.test import TestCase
from django.urls import reverse
from .models import Todo

class TodoTests(TestCase):
  def setUp(self):
      self.todo1 = Todo.objects.create(title="Test TODO 1", description="Description 1", due_date="2025-12-01", is_resolved=False)
      self.todo2 = Todo.objects.create(title="Test TODO 2", description="Description 2", due_date="2025-12-02", is_resolved=True)

# TODO List View
  def test_todo_list_view(self):
      response = self.client.get(reverse('todo_list'))
      self.assertEqual(response.status_code, 200)
      self.assertContains(response, "Test TODO 1")
      self.assertContains(response, "Test TODO 2")

# TODO Creation
  def test_todo_creation(self):
      response = self.client.post(reverse('todo_create'), {
          'title': 'New TODO',
          'description': 'New Description',
          'due_date': '2025-12-03',
          'is_resolved': False
      })
      self.assertEqual(response.status_code, 302)  # Redirect after creation
      self.assertTrue(Todo.objects.filter(title="New TODO").exists())

# TODO Editing
  def test_todo_edit(self):
      response = self.client.post(reverse('todo_edit', args=[self.todo1.pk]), {
          'title': 'Updated TODO',
          'description': 'Updated Description',
          'due_date': '2025-12-04',
          'is_resolved': True
      })
      self.assertEqual(response.status_code, 302)  # Redirect after editing
      self.todo1.refresh_from_db()
      self.assertEqual(self.todo1.title, "Updated TODO")
      self.assertTrue(self.todo1.is_resolved)

# TODO Deletion
  def test_todo_delete(self):
      response = self.client.post(reverse('todo_delete', args=[self.todo1.pk]))
      self.assertEqual(response.status_code, 302)  # Redirect after deletion
      self.assertFalse(Todo.objects.filter(pk=self.todo1.pk).exists())

# TODO Resolution
  def test_todo_resolve(self):
      response = self.client.post(reverse('todo_resolve', args=[self.todo1.pk]))
      self.assertEqual(response.status_code, 302)  # Redirect after resolution
      self.todo1.refresh_from_db()
      self.assertTrue(self.todo1.is_resolved)

# Edge Cases
  def test_empty_todo_list(self):
      Todo.objects.all().delete()
      response = self.client.get(reverse('todo_list'))
      self.assertEqual(response.status_code, 200)
      self.assertContains(response, "No TODOs found")

  def test_invalid_todo_id(self):
      response = self.client.get(reverse('todo_edit', args=[999]))
      self.assertEqual(response.status_code, 404)  # Not Found