import pytest
from main import BooksCollector

@pytest.fixture
def collector():
    return BooksCollector()

@pytest.fixture
def collector_with_books():
    collector = BooksCollector()
    collector.add_new_book('1984')
    collector.set_book_genre('1984', 'Фантастика')
    collector.add_new_book('Комедия')
    collector.set_book_genre('Комедия', 'Комедия')
    collector.add_new_book('Книга без жанра')
    return collector

@pytest.fixture
def collector_with_favorites():
    collector = BooksCollector()
    collector.add_new_book('Избранная 1')
    collector.add_new_book('Избранная 2')
    collector.add_book_in_favorites('Избранная 1')
    collector.add_book_in_favorites('Избранная 2')
    return collector

class TestAddNewBook:
    def test_add_single_book(self, collector):
        collector.add_new_book('Гарри Поттер')
        assert 'Гарри Поттер' in collector.books_genre
        assert collector.books_genre['Гарри Поттер'] == ''

    @pytest.mark.parametrize('name,expected', [
        ('Книга', True),
        ('К'*40, True),  
        ('', False),     
        ('К'*41, False)  
    ])
    def test_name_validation(self, collector, name, expected):
        collector.add_new_book(name)
        assert (name in collector.books_genre) == expected

    def test_add_duplicate_book(self, collector):
        collector.add_new_book('Дюна')
        collector.add_new_book('Дюна')
        assert len(collector.books_genre) == 1


class TestSetBookGenre:
    def test_set_valid_genre(self, collector):
        collector.books_genre['Новая книга'] = ''
        collector.set_book_genre('Новая книга', 'Фантастика')
        assert collector.books_genre['Новая книга'] == 'Фантастика'

    def test_set_invalid_genre(self, collector):
        collector.books_genre['Книга'] = ''
        collector.set_book_genre('Книга', 'Несуществующий жанр')
        assert collector.books_genre['Книга'] == ''

    def test_set_genre_to_nonexistent_book(self, collector):
        collector.set_book_genre('Несуществующая книга', 'Фантастика')
        assert 'Несуществующая книга' not in collector.books_genre


class TestGetBookGenre:
    def test_get_existing_book_genre(self, collector_with_books):
        assert collector_with_books.get_book_genre('1984') == 'Фантастика'

    def test_get_nonexistent_book_genre(self, collector):
        assert collector.get_book_genre('Несуществующая книга') is None

    def test_get_book_without_genre(self, collector_with_books):
        assert collector_with_books.get_book_genre('Книга без жанра') == ''


class TestGetBooksWithSpecificGenre:
    def test_get_books_by_genre(self, collector_with_books):
        result = collector_with_books.get_books_with_specific_genre('Фантастика')
        assert result == ['1984']

    def test_get_books_by_nonexistent_genre(self, collector_with_books):
        assert collector_with_books.get_books_with_specific_genre('Несуществующий жанр') == []


class TestGetBooksForChildren:
    def test_get_children_books(self, collector_with_books):
        result = collector_with_books.get_books_for_children()
        assert '1984' in result
        assert 'Ужастик' not in result


class TestAddBookInFavorites:
    def test_add_to_favorites(self, collector_with_books):
        collector_with_books.add_book_in_favorites('Комедия')
        assert 'Комедия' in collector_with_books.favorites

    def test_add_to_favorites_twice(self, collector_with_books):
        collector_with_books.add_book_in_favorites('Комедия')
        collector_with_books.add_book_in_favorites('Комедия')
        assert len(collector_with_books.favorites) == 1

class TestDeleteBookFromFavorites:
    def test_remove_from_favorites(self, collector_with_favorites):
        collector_with_favorites.delete_book_from_favorites('Избранная 1')
        assert 'Избранная 1' not in collector_with_favorites.favorites

class TestGetListOfFavoritesBooks:
    def test_get_favorites_list(self, collector_with_favorites):
        assert sorted(collector_with_favorites.get_list_of_favorites_books()) == ['Избранная 1', 'Избранная 2']