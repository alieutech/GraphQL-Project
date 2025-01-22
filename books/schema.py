import graphene
from graphene_django.types import DjangoObjectType
from .models import Books


class BookType(DjangoObjectType):
    class Meta:
        model = Books


# Mutation to create a book
class CreateBook(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        author = graphene.String(required=True)
        published_date = graphene.Date(required=True)

    book = graphene.Field(BookType)

    def mutate(self, info, title, author, published_date):
        book = Books(title=title, author=author, published_date=published_date)
        book.save()
        return CreateBook(book=book)


# Mutation to update a book
class UpdateBook(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        author = graphene.String()
        published_date = graphene.Date()

    book = graphene.Field(BookType)

    def mutate(self, info, id, title=None, author=None, published_date=None):
        try:
            book = Books.objects.get(pk=id)
        except Books.DoesNotExist:
            raise Exception("Book not found")

        if title:
            book.title = title
        if author:
            book.author = author
        if published_date:
            book.published_date = published_date

        book.save()
        return UpdateBook(book=book)


# Mutation to delete a book
class DeleteBook(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            book = Books.objects.get(pk=id)
            book.delete()
            return DeleteBook(success=True)
        except Books.DoesNotExist:
            raise Exception("Book not found")


# Combine mutations into a single class
class Mutation(graphene.ObjectType):
    create_book = CreateBook.Field()
    update_book = UpdateBook.Field()
    delete_book = DeleteBook.Field()


# Query class
class Query(graphene.ObjectType):
    all_books = graphene.List(BookType)

    def resolve_all_books(self, info, **kwargs):
        return Books.objects.all()


# Define the schema
schema = graphene.Schema(query=Query, mutation=Mutation)
