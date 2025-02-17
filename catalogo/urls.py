from django.urls import path, include
from rest_framework import routers

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('autores/', views.AutorListView.as_view(), name='autores'),
    path('autor/<int:pk>',
         views.AutorDetailView.as_view(), name='autor-detail'),
]


urlpatterns += [
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path(r'borrowed/', views.LoanedBooksAllListView.as_view(), name='all-borrowed'),  # Added for challenge
]


# Add URLConf for librarian to renew a book.
urlpatterns += [
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
]


# Add URLConf to create, update, and delete authors
urlpatterns += [
    path('autor/create/', views.AutorCreate.as_view(), name='autor-create'),
    path('autor/<int:pk>/update/', views.AutorUpdate.as_view(), name='autor-update'),
    path('autor/<int:pk>/delete/', views.AutorDelete.as_view(), name='autor-delete'),
]

# Add URLConf to create, update, and delete books
urlpatterns += [
    path('book/create/', views.BookCreate.as_view(), name='book-create'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book-delete'),
]


# Add URLConf to list, view, create, update, and delete gênero
urlpatterns += [
    path('gêneros/', views.GêneroListView.as_view(), name='gêneros'),
    path('gênero/<int:pk>', views.GêneroDetailView.as_view(), name='gênero-detail'),
    path('gênero/create/', views.GêneroCreate.as_view(), name='gênero-create'),
    path('gênero/<int:pk>/update/', views.GêneroUpdate.as_view(), name='gênero-update'),
    path('gênero/<int:pk>/delete/', views.GêneroDelete.as_view(), name='gênero-delete'),
]

# Add URLConf to list, view, create, update, and delete languages
urlpatterns += [
    path('languages/', views.LanguageListView.as_view(), name='languages'),
    path('language/<int:pk>', views.LanguageDetailView.as_view(),
         name='language-detail'),
    path('language/create/', views.LanguageCreate.as_view(), name='language-create'),
    path('language/<int:pk>/update/',
         views.LanguageUpdate.as_view(), name='language-update'),
    path('language/<int:pk>/delete/',
         views.LanguageDelete.as_view(), name='language-delete'),
]

# Add URLConf to list, view, create, update, and delete bookinstances
urlpatterns += [
    path('bookinstances/', views.BookInstanceListView.as_view(), name='bookinstances'),
    path('bookinstance/<uuid:pk>', views.BookInstanceDetailView.as_view(),
         name='bookinstance-detail'),
    path('bookinstance/create/', views.BookInstanceCreate.as_view(),
         name='bookinstance-create'),
    path('bookinstance/<uuid:pk>/update/',
         views.BookInstanceUpdate.as_view(), name='bookinstance-update'),
    path('bookinstance/<uuid:pk>/delete/',
         views.BookInstanceDelete.as_view(), name='bookinstance-delete'),
]

#DRF
router = routers.DefaultRouter()
router.register(r'books', views.BookViewSet)

urlpatterns += [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
