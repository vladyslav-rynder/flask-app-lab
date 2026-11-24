import unittest
from app import create_app, db
from app.posts.models import Post

class PostTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['WTF_CSRF_ENABLED'] = False

        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_list_posts(self):
        response = self.client.get('/post')
        self.assertEqual(response.status_code, 200)

    def test_create_post_with_session_author(self):
        with self.client.session_transaction() as sess:
            sess['username'] = 'test_user'

        response = self.client.post('/post/create', data={
            'title': 'Test Post',
            'content': 'Test Content',
            'publish_date': '2026-11-12T12:00',
            'category': 'news',
            'is_active': True
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)

        post = Post.query.first()
        self.assertIsNotNone(post)
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.author, 'test_user')

    def test_detail_post(self):
        post = Post(title='Detail Title', content='Detail Content', author='Anonymous')
        db.session.add(post)
        db.session.commit()

        response = self.client.get(f'/post/{post.id}')
        self.assertEqual(response.status_code, 200)

    def test_update_post(self):
        post = Post(title='Old Title', content='Old Content', author='Anonymous')
        db.session.add(post)
        db.session.commit()

        response = self.client.post(f'/post/{post.id}/update', data={
            'title': 'Updated Title',
            'content': 'Updated Content',
            'publish_date': '2026-11-12T14:00',
            'category': 'tech',
            'is_active': True
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)

        updated_post = db.session.get(Post, post.id)
        self.assertEqual(updated_post.title, 'Updated Title')

    def test_delete_post(self):
        post = Post(title='To Delete', content='Content', author='Anonymous')
        db.session.add(post)
        db.session.commit()
        post_id = post.id

        response = self.client.post(f'/post/{post_id}/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        deleted_post = db.session.get(Post, post_id)
        self.assertIsNone(deleted_post)

if __name__ == '__main__':
    unittest.main()