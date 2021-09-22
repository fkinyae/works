from django.test import TestCase
from .models import Rate,Profile,Project,User

# Create your tests here.
class ProjectTestClass(TestCase):
    #setuo method
    def setUp(self):
        self.user = User(username='martin')
        self.francis = Project(title = 'love', url='http://love.com', description = 'love is beautiful', user = self.user, photo = 'default.png', date = '12-12-2020')
        
    #Testing Instance
    def test_instance(self):
        self.assertTrue(isinstance(self.francis,Project))
        
    def test_save_method(self):
        self.francis.save_project()
        projects = Project.objects.all()
        self.assertTrue(len(projects) > 0)    