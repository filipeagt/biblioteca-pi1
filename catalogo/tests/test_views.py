from django.test import TestCase

# Create your tests here.

from catalogo.models import Autor
from django.urls import reverse


class AutorListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create authors for pagination tests
        number_of_autores = 13
        for autor_id in range(number_of_autores):
            Autor.objects.create(nome='Christian {0}'.format(autor_id),
                                  sobrenome='Surname {0}'.format(autor_id))

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/catalogo/autores/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('autores'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('autores'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalogo/autor_list.html')

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('autores'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertEqual(len(response.context['autor_list']), 10)

    def test_lists_all_autores(self):
        # Get second page and confirm it has (exactly) the remaining 3 items
        response = self.client.get(reverse('autores')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertEqual(len(response.context['autor_list']), 3)


import datetime
from django.utils import timezone

from catalogo.models import BookInstance, Book, Gênero, Language

# Get user model from settings
from django.contrib.auth import get_user_model
User = get_user_model()


class LoanedBookInstancesByUserListViewTest(TestCase):

    def setUp(self):
        # Create two users
        test_user1 = User.objects.create_user(
            username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(
            username='testuser2', password='2HJ1vRV0Z&3iD')

        test_user1.save()
        test_user2.save()

        # Create a book
        test_autor = Autor.objects.create(
            nome='John', sobrenome='Smith')
        test_genre = Gênero.objects.create(name='Fantasy')
        test_language = Language.objects.create(name='English')
        test_book = Book.objects.create(
            título='Book Title',
            resumo='My book summary',
            autor=test_autor,
        )
        # Create genre as a post-step
        genre_objects_for_book = Gênero.objects.all()
        test_book.gênero.set(genre_objects_for_book)
        test_book.save()

        # Create 30 BookInstance objects
        number_of_book_copies = 30
        for book_copy in range(number_of_book_copies):
            return_date = timezone.now() + datetime.timedelta(days=book_copy % 5)
            if book_copy % 2:
                the_borrower = test_user1
            else:
                the_borrower = test_user2
            status = 'a'
            BookInstance.objects.create(book=test_book, due_back=return_date,
                                        borrower=the_borrower, status=status)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('my-borrowed'))
        self.assertRedirects(
            response, '/accounts/login/?next=/catalogo/mybooks/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(
            username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('my-borrowed'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(
            response, 'catalogo/bookinstance_list_borrowed_user.html')

    def test_only_borrowed_books_in_list(self):
        login = self.client.login(
            username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('my-borrowed'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check that initially we don't have any books in list (none on loan)
        self.assertTrue('bookinstance_list' in response.context)
        self.assertEqual(len(response.context['bookinstance_list']), 0)

        # Now change all books to be on loan
        get_ten_books = BookInstance.objects.all()[:10]

        for copy in get_ten_books:
            copy.status = 'o'
            copy.save()

        # Check that now we have borrowed books in the list
        response = self.client.get(reverse('my-borrowed'))
        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        self.assertTrue('bookinstance_list' in response.context)

        # Confirm all books belong to testuser1 and are on loan
        for book_item in response.context['bookinstance_list']:
            self.assertEqual(response.context['user'], book_item.borrower)
            self.assertEqual(book_item.status, 'o')

    def test_pages_paginated_to_ten(self):

        # Change all books to be on loan.
        # This should make 15 test user ones.
        for copy in BookInstance.objects.all():
            copy.status = 'o'
            copy.save()

        login = self.client.login(
            username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('my-borrowed'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Confirm that only 10 items are displayed due to pagination
        # (if pagination not enabled, there would be 15 returned)
        self.assertEqual(len(response.context['bookinstance_list']), 10)

    def test_pages_ordered_by_due_date(self):

        # Change all books to be on loan
        for copy in BookInstance.objects.all():
            copy.status = 'o'
            copy.save()

        login = self.client.login(
            username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('my-borrowed'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Confirm that of the items, only 10 are displayed due to pagination.
        self.assertEqual(len(response.context['bookinstance_list']), 10)

        last_date = 0
        for copy in response.context['bookinstance_list']:
            if last_date == 0:
                last_date = copy.due_back
            else:
                self.assertTrue(last_date <= copy.due_back)


from django.contrib.auth.models import Permission  # Required to grant the permission needed to set a book as returned.


class RenewBookInstancesViewTest(TestCase):

    def setUp(self):
        # Create a user
        test_user1 = User.objects.create_user(
            username='testuser1', password='1X<ISRUkw+tuK')
        test_user1.save()

        test_user2 = User.objects.create_user(
            username='testuser2', password='2HJ1vRV0Z&3iD')
        test_user2.save()
        permission = Permission.objects.get(name='Set book as returned')
        test_user2.user_permissions.add(permission)
        test_user2.save()

        # Create a book
        test_autor = Autor.objects.create(
            nome='John', sobrenome='Smith')
        test_genre = Gênero.objects.create(name='Fantasy')
        #test_language = Language.objects.create(name='English')
        test_book = Book.objects.create(título='Book Title', resumo='My book summary',
                                        autor=test_autor,)
        # Create genre as a post-step
        genre_objects_for_book = Gênero.objects.all()
        test_book.gênero.set(genre_objects_for_book)
        test_book.save()

        # Create a BookInstance object for test_user1
        return_date = datetime.date.today() + datetime.timedelta(days=5)
        self.test_bookinstance1 = BookInstance.objects.create(book=test_book,
                                                              due_back=return_date,
                                                              borrower=test_user1, status='o')

        # Create a BookInstance object for test_user2
        return_date = datetime.date.today() + datetime.timedelta(days=5)
        self.test_bookinstance2 = BookInstance.objects.create(book=test_book,
                                                              due_back=return_date, borrower=test_user2, status='o')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_forbidden_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(
            username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(
            reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}))
        self.assertEqual(response.status_code, 403)

    def test_logged_in_with_permission_borrowed_book(self):
        login = self.client.login(
            username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(
            reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance2.pk}))

        # Check that it lets us login - this is our book and we have the right permissions.
        self.assertEqual(response.status_code, 200)

    def test_logged_in_with_permission_another_users_borrowed_book(self):
        login = self.client.login(
            username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(
            reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}))

        # Check that it lets us login. We're a librarian, so we can view any users book
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        login = self.client.login(
            username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(
            reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}))
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'catalogo/book_renew_librarian.html')

    def test_form_renewal_date_initially_has_date_three_weeks_in_future(self):
        login = self.client.login(
            username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(
            reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}))
        self.assertEqual(response.status_code, 200)

        date_3_weeks_in_future = datetime.date.today() + datetime.timedelta(weeks=3)
        self.assertEqual(
            response.context['form'].initial['renewal_date'], date_3_weeks_in_future)

    def test_form_invalid_renewal_date_past(self):
        login = self.client.login(
            username='testuser2', password='2HJ1vRV0Z&3iD')

        date_in_past = datetime.date.today() - datetime.timedelta(weeks=1)
        response = self.client.post(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}),
                                    {'renewal_date': date_in_past})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context['form'], 'renewal_date', 'Data Inválida - renovação no passado')

    def test_form_invalid_renewal_date_future(self):
        login = self.client.login(
            username='testuser2', password='2HJ1vRV0Z&3iD')

        invalid_date_in_future = datetime.date.today() + datetime.timedelta(weeks=5)
        response = self.client.post(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}),
                                    {'renewal_date': invalid_date_in_future})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context['form'], 'renewal_date', 'Data Inválida - renovação com mais de 4 semanas')

    def test_redirects_to_all_borrowed_book_list_on_success(self):
        login = self.client.login(
            username='testuser2', password='2HJ1vRV0Z&3iD')
        valid_date_in_future = datetime.date.today() + datetime.timedelta(weeks=2)
        response = self.client.post(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}),
                                    {'renewal_date': valid_date_in_future})
        self.assertRedirects(response, reverse('all-borrowed'))

    def test_HTTP404_for_invalid_book_if_logged_in(self):
        import uuid
        test_uid = uuid.uuid4()  # unlikely UID to match our bookinstance!
        login = self.client.login(
            username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(
            reverse('renew-book-librarian', kwargs={'pk': test_uid}))
        self.assertEqual(response.status_code, 404)

from django.contrib.contenttypes.models import ContentType
class AutorCreateViewTest(TestCase):
    """Test case for the AutorCreate view (Created as Challenge)."""

    def setUp(self):
        # Create a user
        test_user1 = User.objects.create_user(
            username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(
            username='testuser2', password='2HJ1vRV0Z&3iD')

        test_user1.save()
        test_user2.save()

        content_typeBook = ContentType.objects.get_for_model(Book)

        permAddBook = Permission.objects.get(
            codename="add_book",
            content_type=content_typeBook,
        )

        content_typeAutor = ContentType.objects.get_for_model(Autor)
        permAddAutor = Permission.objects.get(
            codename="add_autor",
            content_type=content_typeAutor,
        )


        test_user2.user_permissions.add(permAddBook, permAddAutor)
        test_user2.save()

        # Create a book
        test_autor = Autor.objects.create(
            nome='John', sobrenome='Smith')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('autor-create'))
        self.assertRedirects(
            response, '/accounts/login/?next=/catalogo/autor/create/')

    def test_forbidden_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(
            username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('autor-create'))
        self.assertEqual(response.status_code, 403)

    def test_logged_in_with_permission(self):
        login = self.client.login(
            username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('autor-create'))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        login = self.client.login(
            username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('autor-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalogo/autor_form.html')
    
    def test_redirects_to_detail_view_on_success(self):
        login = self.client.login(
            username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.post(reverse('autor-create'),
                                    {'nome': 'Christian Name', 'sobrenome': 'Surname'})
        # Manually check redirect because we don't know what autor was created
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/catalogo/autor/'))