from django.urls import path
from .views import (
    AuthorList, AuthorDetail, 
    BookList, BookDetail, 
    CategoryList, CategoryDetail, 
    SubcategoryList, SubcategoryDetail, 
    ReviewList, ReviewDetail
)
urlpatterns = [
    path('api/authors/', AuthorList.as_view(), name='author-list'),
    path('api/authors/<int:pk>/', AuthorDetail.as_view(), name='author-detail'),

    path('api/books/', BookList.as_view(), name='book-list'),
    path('api/books/<int:pk>/', BookDetail.as_view(), name='book-detail'),

    path('api/categories/', CategoryList.as_view(), name='category-list'),
    path('api/categories/<int:pk>/', CategoryDetail.as_view(), name='category-detail'),

    path('api/subcategories/', SubcategoryList.as_view(), name='subcategory-list'),
    path('api/subcategories/<int:pk>/', SubcategoryDetail.as_view(), name='subcategory-detail'),

    path('api/reviews/', ReviewList.as_view(), name='review-list'),
    path('api/reviews/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),
]
