# Copyright 2017 Graham Binns. This software is licensed under the MIT
# license. See the LICENSE file for more information.
"""Tests for usefulenums.enum."""


from unittest import TestCase

import enum
from usefulenums.enum import (
    Enum,
    enum_to_choices,
)


class EnumInitTestCase(TestCase):
    """Tests for Enum.__init__()."""

    def test_accepts_three_tuples_as_arguments(self):
        # __init__() will take three-tuples as arguments for setting up
        # enumeration items.
        try:
            Enum((1, "MY_FIRST_VALUE", "Display text"))
        except ValueError:
            self.fail("Enum() raised a ValueError when accepting a 3-tuple.")

    def test_accepts_two_tuples_as_arguments(self):
        # __init__() will take two-tuples as arguments for setting up
        # enumeration items.
        try:
            Enum(("MY_FIRST_VALUE", "Display text"))
        except ValueError:
            self.fail("Enum() raised a ValueError when accepting a 2-tuple.")

    def test_rejects_mixed_two_and_three_tuples(self):
        # __init__() does not allow 2-tuples to be mixed with 3-tuples.
        # Whichever comes first wins.
        self.assertRaises(
            ValueError, Enum, (1, "MY_FIRST_VALUE", "Display text"),
            ("MY_SECOND_VALUE", "Display text 2"))

    def test_assigns_2_tuple_ids_automatically(self):
        # When 2-tuples are passed to __init__(), IDs are assigned to
        # the items in order.
        enum = Enum(
            ("MY_FIRST_VALUE", "Display text"),
            ("MY_SECOND_VALUE", "Display text 2"))

        self.assertEqual(0, enum._id_mappings["MY_FIRST_VALUE"])
        self.assertEqual(1, enum._id_mappings["MY_SECOND_VALUE"])

    def test_python_name_must_conform_to_regex(self):
        # The python_name passed to __init__() must contain uppercase
        # letters, underscores or numbers only, with no leading digits.
        invalid_names = [
            "Not conforming at all",
            "1_NO_LEADING_NUMBERS",
            "UPPERCASE_letters_ONLY",
        ]

        for invalid_name in invalid_names:
            self.assertRaises(
                ValueError, Enum, (invalid_name, ""))
            self.assertRaises(
                ValueError, Enum, (1, invalid_name, ""))


class EnumGetAttrTestCase(TestCase):
    """Tests for Enum.__getattr__()."""

    def test_returns_id_for_python_name(self):
        # When Enum.FOO is accessed, the ID associated with the
        # python_name `FOO` is returned.
        enum = Enum((1, "TEST_VALUE", "Test value"))
        self.assertEqual(1, enum.TEST_VALUE)

    def test_raises_attribute_error_if_no_such_name(self):
        # If a given enum item does not exist, trying to access it will
        # raise an AttributeError.
        enum = Enum((1, "TEST_VALUE", "Test value"))
        self.assertRaises(AttributeError, lambda: enum.DOES_NOT_EXIST)


class EnumAsChoicesTestCase(TestCase):
    """Tests for Enum.as_choices()."""

    def test_returns_ordered_key_value_pairs(self):
        # Enum.as_choices() returns the enum's items in ID order as (ID,
        # display_name) pairs.
        enum = Enum(
            (1, "CHOICE_1", "Choice one"),
            (2, "CHOICE_2", "Choice two"),
            (0, "CHOICE_0", "Choice zero"),
        )
        expected_choices = (
            (0, "Choice zero"),
            (1, "Choice one"),
            (2, "Choice two"),
        )
        self.assertEqual(expected_choices, enum.as_choices())


class EnumGetDisplayNameTestCase(TestCase):
    """Tests for Enum.get_display_name()."""

    def test_returns_display_name_for_a_given_value(self):
        # When passed an Enum item, get_display_name() will return the
        # display name for that item.
        enum = Enum(
            (1, "CHOICE_1", "Choice one"),
            (2, "CHOICE_2", "Choice two"),
            (0, "CHOICE_0", "Choice zero"),
        )
        self.assertEqual("Choice one", enum.get_display_name(enum.CHOICE_1))

    def test_raises_value_error_if_no_such_id_present(self):
        # If passed an ID that it doesn't recognise, get_display_name()
        # will raise a ValueError.
        enum = Enum(
            (1, "CHOICE_1", "Choice one"),
            (2, "CHOICE_2", "Choice two"),
            (0, "CHOICE_0", "Choice zero"),
        )
        with self.assertRaises(ValueError):
            enum.get_display_name("123123123")


class EnumToChoicesTestCase(TestCase):
    """Tests for enum_to_choices()."""

    def test_returns_choices_from_classic_enum(self):
        # enum_to_choices() will take a regular Python Enum and return a
        # tuple of two-tuples of (value, stringified name) for each item
        # in the Enum.
        class TestEnum(enum.Enum):
            value_1 = "a value"
            value_2 = "another value"

        expected_choices = (
            ("a value", "Value 1"),
            ("another value", "Value 2"),
        )
        self.assertEqual(expected_choices, enum_to_choices(TestEnum))

    def test_uses_passed_stringification_function(self):
        # enum_to_choices() accepts a stringifier argument which
        # dictates how the enum item names are turned into strings.
        class TestEnum(enum.Enum):
            value_1 = "a value"
            value_2 = "another value"

        expected_choices = (
            ("a value", "VALUE_1"),
            ("another value", "VALUE_2"),
        )
        self.assertEqual(
            expected_choices,
            enum_to_choices(TestEnum, stringifier=lambda s: s.upper())
        )

    def test_name_as_value_converts_name_to_string(self):
        # If name_as_value is True, enum_to_choices() will return a two
        # tuple of (name, stringified_name) instead of (value,
        # stringified_name).
        class TestEnum(enum.Enum):
            value_1 = "a value"
            value_2 = "another value"

        expected_choices = (
            ("value_1", "Value 1"),
            ("value_2", "Value 2"),
        )
        self.assertEqual(
            expected_choices,
            enum_to_choices(TestEnum, name_as_value=True),
        )
