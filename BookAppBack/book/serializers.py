from rest_framework import serializers
from .models import Author, Book, Category, Subcategory, Review,BookCategory

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']



class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'synopsis', 'author', 'price',"created_at","updated_at"]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class SubcategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Subcategory
        fields = ['id', 'name', 'category']


class ReviewSerializer(serializers.ModelSerializer):
    book = BookSerializer()

    class Meta:
        model = Review
        fields = ['id', 'book', 'review_text']


class BookCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCategory
        fields = ['book', 'category', 'subcategory']

    def validate(self, data):
        book = data.get('book')
        category = data.get('category')
        subcategory = data.get('subcategory')

        # Check if the combination already exists
        if BookCategory.objects.filter(book=book, category=category, subcategory=subcategory).exists():
            raise serializers.ValidationError("This combination of book, category, and subcategory already exists.")
        return data