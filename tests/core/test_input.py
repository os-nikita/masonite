from src.masonite.testing import TestCase
from src.masonite.input.InputBag import InputBag
from src.masonite.testing.generate_wsgi import MockWsgiInput

class TestInput(TestCase):

    def setUp(self):
        super().setUp()
        self.post_data = MockWsgiInput('{"param": "hey", "foo": [9, 8, 7, 6], "bar": "baz"}')
        self.bytes_data = MockWsgiInput(b'jack=Daniels')

    def test_can_parse_query_string(self):
        bag = InputBag()
        bag.load({"QUERY_STRING": "hello=you&goodbye=me"})
        self.assertEqual(bag.get('hello'), 'you')
        self.assertEqual(bag.get('goodbye'), 'me')

    def test_can_parse_duplicate_values(self):
        bag = InputBag()
        bag.load({"QUERY_STRING": "filter[name]=Joe&filter[last]=Bill"})
        """
            {"filter": [{}]}
        """
        self.assertTrue("name" in bag.get('filter'))
        self.assertTrue("last" in bag.get('filter'))

    def test_all_with_values(self):
        bag = InputBag()
        bag.load({"QUERY_STRING": "hello=you"})
        """
            {"filter": [{}]}
        """
        self.assertEquals(bag.all_as_values(), {"hello": "you"})

    def test_all_without_internal_values(self):
        bag = InputBag()
        bag.load({"QUERY_STRING": "hello=you&__token=tok"})
        """
            {"filter": [{}]}
        """
        self.assertEquals(bag.all_as_values(internal_variables=False), {"hello": "you"})

    def test_has(self):
        bag = InputBag()
        bag.load({"QUERY_STRING": "hello=you&goodbye=me"})
        self.assertTrue(bag.has('hello', 'goodbye'))

    def test_can_parse_post_params(self):
        bag = InputBag()
        bag.load({"wsgi.input": self.post_data, 'CONTENT_TYPE': 'application/json'})
        self.assertEqual(bag.get('param'), 'hey')

    def test_can_parse_post_params_from_url_encoded(self):
        bag = InputBag()
        bag.load({"wsgi.input": self.bytes_data, 'CONTENT_TYPE': 'application/x-www-form-urlencoded'})
        self.assertEqual(bag.get('jack'), 'Daniels')
