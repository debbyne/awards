from django.test import TestCase
from .models import Project

# Create your tests here.
class ProjectTestClass(TestCase):
    def setUp(self):
       pass
    def test_instance(self):
        self.assertTrue(isinstance(self.test_image,Project))
     
    def test_save_image(self):
        self.image.save_image()
        self.assertTrue(len(Project.objects.all()) == 1)
    def test_delete_image(self):
        self.test_image.delete_image()
        image = Project.objects.all()
        self.assertTrue(len(Project.objects.all()) ==1)