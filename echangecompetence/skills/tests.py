from django.test import TestCase
from django.urls import reverse

class Views(TestCase):
    def test_views_exists_index(self):
        """
        verifiate if the view index exists
        """
        response = self.client.get(reverse("skills:index"))
        self.assertEqual(response.status_code, 200)

    def test_views_exists_all_skills(self):
            """
            verifiate if the view index exists
            """
            response = self.client.get(reverse("skills:all_skills"))
            self.assertEqual(response.status_code, 200)

    def test_views_exists_connection(self):
                """
                verifiate if the view index exists
                """
                response = self.client.get(reverse("skills:connection"))
                self.assertEqual(response.status_code, 200)

    def test_views_exists_add_skills(self):
                    """
                    verifiate if the view index exists
                    """
                    response = self.client.get(reverse("skills:add_skills"))
                    self.assertEqual(response.status_code, 302)

    def test_views_exists_search_help_skills(self):
                        """
                        verifiate if the view index exists
                        """
                        response = self.client.get(reverse("skills:search_skills_help"))
                        self.assertEqual(response.status_code, 302)

    def test_views_exists_search_skills(self):
                            """
                            verifiate if the view index exists
                            """
                            response = self.client.get(reverse("skills:search_skills"))
                            self.assertEqual(response.status_code, 302)