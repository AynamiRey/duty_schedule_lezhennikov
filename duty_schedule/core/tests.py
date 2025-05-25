from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from .models import DutySchedule


class IntegrationTests(TestCase):
    def setUp(self):
        """Настройка для тестов."""
        # Создаем обычного пользователя для тестов
        self.test_user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='userpassword',
            first_name='Тест',
            last_name='Пользователь'
        )
        
        # Создаем административного пользователя
        self.admin_user = get_user_model().objects.create_superuser(
            username='admin_test',
            email='admin@example.com',
            password='adminpassword',
            first_name='Админ',
            last_name='Тестовый'
        )
        
        # Создаем дежурство для тестового пользователя
        self.current_date = timezone.now().date()
        self.duty = DutySchedule.objects.create(
            user=self.test_user,
            date=self.current_date
        )

    def test_login_view(self):
        """Тест отображения страницы входа."""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_user_login(self):
        """Тест входа пользователя в систему."""
        login_successful = self.client.login(username='testuser', password='userpassword')
        self.assertTrue(login_successful)
        
        # Проверяем доступ к странице пользователя после входа
        response = self.client.get(reverse('user_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_dashboard.html')

    def test_admin_login(self):
        """Тест входа администратора в систему."""
        login_successful = self.client.login(username='admin_test', password='adminpassword')
        self.assertTrue(login_successful)
        
        # Проверяем доступ к административной панели после входа
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_dashboard.html')

    def test_logout(self):
        """Тест выхода из системы."""
        # Сначала входим
        self.client.login(username='testuser', password='userpassword')
        
        # Проверяем доступ к защищенному ресурсу после входа
        response = self.client.get(reverse('user_dashboard'))
        self.assertEqual(response.status_code, 200)
        
        # Выходим
        self.client.logout()
        
        # Проверяем, что теперь доступ к защищенному ресурсу ограничен
        response = self.client.get(reverse('user_dashboard'), follow=True)
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('user_dashboard')}")

    def test_access_restriction(self):
        """Тест ограничения доступа к административной панели."""
        # Входим как обычный пользователь
        self.client.login(username='testuser', password='userpassword')
        
        # Пытаемся получить доступ к административной панели
        response = self.client.get(reverse('admin_dashboard'), follow=True)
        
        # Ожидаем, что нас перенаправят на страницу входа
        self.assertTrue(len(response.redirect_chain) > 0)
        self.assertIn('login', response.redirect_chain[0][0])
