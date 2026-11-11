import string
import unittest

try:
    from .password_generator import generate_password
except ImportError:
    from password_generator import generate_password


class PasswordGeneratorTests(unittest.TestCase):
    def test_default_password_has_requested_length_and_all_groups(self):
        password = generate_password()
        self.assertEqual(len(password), 16)
        self.assertTrue(any(char in string.ascii_lowercase for char in password))
        self.assertTrue(any(char in string.ascii_uppercase for char in password))
        self.assertTrue(any(char in string.digits for char in password))
        self.assertTrue(any(char in string.punctuation for char in password))

    def test_custom_password_uses_only_enabled_groups(self):
        password = generate_password(
            12, lowercase=True, uppercase=False, digits=True, symbols=False
        )
        self.assertEqual(len(password), 12)
        self.assertTrue(any(char in string.ascii_lowercase for char in password))
        self.assertTrue(any(char in string.digits for char in password))
        self.assertTrue(all(char in string.ascii_lowercase + string.digits for char in password))

    def test_each_enabled_group_is_present(self):
        password = generate_password(
            3, lowercase=True, uppercase=True, digits=True, symbols=False
        )
        self.assertTrue(any(char in string.ascii_lowercase for char in password))
        self.assertTrue(any(char in string.ascii_uppercase for char in password))
        self.assertTrue(any(char in string.digits for char in password))

    def test_rejects_short_length_for_enabled_groups(self):
        with self.assertRaises(ValueError):
            generate_password(2)

    def test_rejects_no_enabled_groups(self):
        with self.assertRaises(ValueError):
            generate_password(
                10, lowercase=False, uppercase=False, digits=False, symbols=False
            )

    def test_rejects_non_integer_length(self):
        with self.assertRaises(ValueError):
            generate_password(4.5)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
