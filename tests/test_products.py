import io
import unittest
from app import app

class ProductTestCase(unittest.TestCase):

    def setUp(self):
        """Налаштування перед кожним тестом"""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = (
            False
        )
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        """Очищення після тестів"""
        self.app_context.pop()

    def test_01_product_list(self):
        """Тест перегляду списку товарів (GET /products/)"""
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)

    def test_02_add_product_get(self):
        """Тест перевірки доступності сторінки додавання товару (GET /products/add)"""
        response = self.client.get('/products/add')
        self.assertEqual(response.status_code, 200)

    def test_03_add_product_post(self):
        """Тест успішного додавання товару через POST із завантаженням файлу"""
        data = {
            'name': 'Тестовий товар',
            'content': 'Це опис тестового товару для перевірки створення.',
            'price': '150.50',
            'category': 'electronics',
            'quantity': '10',
            'image': (io.BytesIO(b'fake image bytes content'), 'test.jpg'),
        }

        response = self.client.post(
            '/products/add', data=data, content_type='multipart/form-data'
        )

        self.assertEqual(response.status_code, 302)

    def test_04_product_detail_not_found(self):
        """Тест перегляду неіснуючого товару (має кидати редирект з flash-повідомленням)"""
        response = self.client.get('/products/999999')
        self.assertEqual(response.status_code, 302)

    def test_05_delete_product(self):
        """Тест видалення товару (POST /products/<id>/delete)"""
        data = {
            'name': 'Товар на видалення',
            'content': 'Опис товару, який буде видалено.',
            'price': '99.99',
            'category': 'books',
            'quantity': '5',
            'image': (io.BytesIO(b'fake image bytes'), 'delete.jpg'),
        }
        self.client.post(
            '/products/add', data=data, content_type='multipart/form-data'
        )

        response = self.client.post('/products/1/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()