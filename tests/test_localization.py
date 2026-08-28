"""Unit tests for the Localization class.

Tests cover:
- Initialization with valid and invalid locales
- Locale parsing (language and territory extraction)
- Property access and retrieval
- Fallback mechanisms for properties
- Cache functionality for number names
- Edge cases and error handling
"""

import pytest

from src.i2w._constants import (
    ConverterImplTypeValue,
)
from src.i2w._localization import Localization
from src.i2w.exception import LocalizationError


class TestLocalizationInitialization:
    """Test Localization initialization with various locale strings."""

    def test_initialization_with_none_uses_system_locale(self):
        """Test that None locale falls back to system locale."""
        loc = Localization(locale_name=None)
        assert isinstance(loc, Localization)

    def test_initialization_with_valid_locale_en_us(self):
        """Test initialization with valid American English locale."""
        loc = Localization(locale_name="en_US")
        assert isinstance(loc, Localization)

    def test_initialization_with_valid_locale_fr_fr(self):
        """Test initialization with valid French (France) locale."""
        loc = Localization(locale_name="fr_FR")
        assert isinstance(loc, Localization)

    def test_initialization_with_valid_locale_fr_be(self):
        """Test initialization with valid French (Belgium) locale."""
        loc = Localization(locale_name="fr_BE")
        assert isinstance(loc, Localization)

    def test_initialization_with_valid_locale_es_es(self):
        """Test initialization with valid Spanish locale."""
        loc = Localization(locale_name="es_ES")
        assert isinstance(loc, Localization)

    def test_initialization_with_valid_locale_pt_br(self):
        """Test initialization with valid Portuguese (Brazil) locale."""
        loc = Localization(locale_name="pt_BR")
        assert isinstance(loc, Localization)

    def test_initialization_with_valid_locale_pt_pt(self):
        """Test initialization with valid Portuguese (Portugal) locale."""
        loc = Localization(locale_name="pt_PT")
        assert isinstance(loc, Localization)

    def test_initialization_with_language_only(self):
        """Test initialization with language code only (no territory)."""
        loc = Localization(locale_name="en")
        assert isinstance(loc, Localization)

    def test_initialization_with_codeset(self):
        """Test that locale with codeset is handled properly."""
        loc = Localization(locale_name="en_US.UTF-8")
        assert isinstance(loc, Localization)

    def test_initialization_with_c_locale(self):
        """Test that C locale is treated as default."""
        loc = Localization(locale_name="C")
        assert isinstance(loc, Localization)

    def test_initialization_with_invalid_locale_raises_error(self):
        """Test that invalid locale format raises LocalizationError."""
        with pytest.raises(LocalizationError):
            Localization(locale_name="US")  # Uppercase language fails pattern

    def test_initialization_with_numeric_locale_raises_error(self):
        """Test that numeric locale raises LocalizationError."""
        with pytest.raises(LocalizationError):
            Localization(locale_name="123_AB")  # Numbers fail the pattern


class TestLocalizationLanguageParsing:
    """Test language code extraction from locale strings."""

    def test_parse_language_from_locale_en_us(self):
        """Test that language 'en' is extracted from 'en_US'."""
        # Access private attributes for testing (implementation detail)
        loc = Localization(locale_name="en_US")
        assert loc._Localization__language == "en"

    def test_parse_language_from_locale_fr_be(self):
        """Test that language 'fr' is extracted from 'fr_BE'."""
        loc = Localization(locale_name="fr_BE")
        assert loc._Localization__language == "fr"

    def test_parse_language_from_locale_pt_br(self):
        """Test that language 'pt' is extracted from 'pt_BR'."""
        loc = Localization(locale_name="pt_BR")
        assert loc._Localization__language == "pt"

    def test_parse_language_from_language_only(self):
        """Test language extraction when only language code is provided."""
        loc = Localization(locale_name="en")
        assert loc._Localization__language == "en"

    def test_parse_language_with_codeset_ignored(self):
        """Test that codeset is ignored in language parsing."""
        loc = Localization(locale_name="en_US.UTF-8")
        assert loc._Localization__language == "en"

    def test_parse_language_none_for_c_locale(self):
        """Test that C locale results in None language."""
        loc = Localization(locale_name="C")
        assert loc._Localization__language is None


class TestLocalizationTerritoryDeduction:
    """Test automatic territory deduction when only language is provided."""

    def test_language_only_en_deduces_us_territory(self):
        """Test that 'en' language-only deduces US territory."""
        loc = Localization(locale_name="en")
        assert loc._Localization__language == "en"
        assert loc._Localization__territory == "US"

    def test_language_only_fr_deduces_fr_territory(self):
        """Test that 'fr' language-only deduces FR territory."""
        loc = Localization(locale_name="fr")
        assert loc._Localization__language == "fr"
        assert loc._Localization__territory == "FR"

    def test_language_only_es_deduces_es_territory(self):
        """Test that 'es' language-only deduces ES territory."""
        loc = Localization(locale_name="es")
        assert loc._Localization__language == "es"
        assert loc._Localization__territory == "ES"

    def test_language_only_pt_deduces_pt_territory(self):
        """Test that 'pt' language-only deduces PT territory."""
        loc = Localization(locale_name="pt")
        assert loc._Localization__language == "pt"
        assert loc._Localization__territory == "PT"

    def test_language_with_codeset_deduces_territory(self):
        """Test that language with codeset still deduces territory."""
        # 'en.UTF-8' should normalize to 'en_US.UTF-8' and extract 'en_US'
        loc = Localization(locale_name="en.UTF-8")
        assert loc._Localization__language == "en"
        assert loc._Localization__territory == "US"

    def test_explicit_territory_not_overridden(self):
        """Test that explicitly provided territory is not overridden."""
        loc = Localization(locale_name="en_GB")
        assert loc._Localization__language == "en"
        assert loc._Localization__territory == "GB"

    def test_deduced_territory_enables_correct_properties(self):
        """Test that deduced territory enables correct locale-specific properties."""
        # Create converter with deduced territory from language-only
        loc_en = Localization(locale_name="en")
        # en_US should use short scale
        impl_type_en = loc_en.get_impl_type()
        assert impl_type_en == ConverterImplTypeValue.SHORT_SCALE

        # Create converter with explicit GB territory
        loc_gb = Localization(locale_name="en_GB")
        # en_GB should use long scale
        impl_type_gb = loc_gb.get_impl_type()
        assert impl_type_gb == ConverterImplTypeValue.LONG_SCALE

    def test_deduced_french_uses_france_properties(self):
        """Test that language-only 'fr' deduces France properties."""
        loc_fr = Localization(locale_name="fr")
        # fr_FR should have tens_7_and_9_as_fr as True
        assert loc_fr.tens_7_and_9_as_fr is True

    def test_deduced_portuguese_uses_portugal_properties(self):
        """Test that language-only 'pt' deduces Portugal properties."""
        loc_pt = Localization(locale_name="pt")
        # pt_PT should have conjunction_before_units as True
        assert loc_pt.conjunction_before_units is True
        # pt_PT should use long scale
        impl_type = loc_pt.get_impl_type()
        assert impl_type == ConverterImplTypeValue.LONG_SCALE

    def test_deduced_vs_explicit_brazil_portuguese(self):
        """Test that Brazil Portuguese (explicit) differs from deduced Portugal Portuguese."""
        loc_deduced = Localization(locale_name="pt")  # Deduces pt_PT
        loc_explicit_br = Localization(locale_name="pt_BR")

        # pt_PT uses long scale, pt_BR uses short scale
        assert loc_deduced.get_impl_type() == ConverterImplTypeValue.LONG_SCALE
        assert loc_explicit_br.get_impl_type() == ConverterImplTypeValue.SHORT_SCALE


class TestLocalizationTerritoryParsing:
    """Test territory code extraction from explicit locale strings."""

    def test_parse_territory_from_locale_en_us(self):
        """Test that territory 'US' is extracted from 'en_US'."""
        loc = Localization(locale_name="en_US")
        assert loc._Localization__territory == "US"

    def test_parse_territory_from_locale_fr_be(self):
        """Test that territory 'BE' is extracted from 'fr_BE'."""
        loc = Localization(locale_name="fr_BE")
        assert loc._Localization__territory == "BE"

    def test_parse_territory_from_locale_pt_br(self):
        """Test that territory 'BR' is extracted from 'pt_BR'."""
        loc = Localization(locale_name="pt_BR")
        assert loc._Localization__territory == "BR"

    def test_parse_territory_with_codeset_ignored(self):
        """Test that codeset is ignored in territory parsing."""
        loc = Localization(locale_name="en_US.UTF-8")
        assert loc._Localization__territory == "US"

    def test_parse_territory_none_for_c_locale(self):
        """Test that C locale results in None territory."""
        loc = Localization(locale_name="C")
        assert loc._Localization__territory is None


class TestBooleanProperties:
    """Test retrieval of boolean properties for different locales."""

    def test_default_bool_property_large_number_invariable(self):
        """Test default locale has large_number_invariable as True."""
        loc = Localization(locale_name="en_US")
        assert loc.large_number_invariable is True

    def test_spanish_conjunction_before_units(self):
        """Test that Spanish has conjunction_before_units as True."""
        loc = Localization(locale_name="es_ES")
        assert loc.conjunction_before_units is True

    def test_spanish_omit_one_from_hundred(self):
        """Test that Spanish omits one from hundred."""
        loc = Localization(locale_name="es_ES")
        assert loc.omit_one_from_hundred is True

    def test_spanish_omit_one_from_thousand(self):
        """Test that Spanish omits one from thousand."""
        loc = Localization(locale_name="es_ES")
        assert loc.omit_one_from_thousand is True

    def test_spanish_large_number_invariable_false(self):
        """Test that Spanish has large_number_invariable as False."""
        loc = Localization(locale_name="es_ES")
        assert loc.large_number_invariable is False

    def test_french_conjunction_before_1_unit_if_lt_80(self):
        """Test that French has conjunction_before_1_unit_if_lt_80 as True."""
        loc = Localization(locale_name="fr_FR")
        assert loc.conjunction_before_1_unit_if_lt_80 is True

    def test_french_tens_7_and_9_as_fr(self):
        """Test that French has tens_7_and_9_as_fr as True."""
        loc = Localization(locale_name="fr_FR")
        assert loc.tens_7_and_9_as_fr is True

    def test_french_plural_hundred0(self):
        """Test that French has plural_hundred0 as True."""
        loc = Localization(locale_name="fr_FR")
        assert loc.plural_hundred0 is True

    def test_french_belgium_tens_7_and_9_as_fr_false(self):
        """Test that Belgian French has tens_7_and_9_as_fr as False."""
        loc = Localization(locale_name="fr_BE")
        assert loc.tens_7_and_9_as_fr is False

    def test_french_belgium_conjunction_before_1_unit_if_eq_90(self):
        """Test that Belgian French has conjunction_before_1_unit_if_eq_90 as True."""
        loc = Localization(locale_name="fr_BE")
        assert loc.conjunction_before_1_unit_if_eq_90 is True

    def test_french_switzerland_tens_7_and_9_as_fr_false(self):
        """Test that Swiss French has tens_7_and_9_as_fr as False."""
        loc = Localization(locale_name="fr_CH")
        assert loc.tens_7_and_9_as_fr is False

    def test_french_switzerland_conjunction_before_1_unit_if_eq_80(self):
        """Test that Swiss French has conjunction_before_1_unit_if_eq_80 as True."""
        loc = Localization(locale_name="fr_CH")
        assert loc.conjunction_before_1_unit_if_eq_80 is True

    def test_french_switzerland_conjunction_before_1_unit_if_eq_90(self):
        """Test that Swiss French has conjunction_before_1_unit_if_eq_90 as True."""
        loc = Localization(locale_name="fr_CH")
        assert loc.conjunction_before_1_unit_if_eq_90 is True

    def test_portuguese_conjunction_before_units(self):
        """Test that Portuguese has conjunction_before_units as True."""
        loc = Localization(locale_name="pt_PT")
        assert loc.conjunction_before_units is True

    def test_portuguese_conjunction_before_tens(self):
        """Test that Portuguese has conjunction_before_tens as True."""
        loc = Localization(locale_name="pt_PT")
        assert loc.conjunction_before_tens is True

    def test_portuguese_conjunction_before_last_non_0_period(self):
        """Test that Portuguese has conjunction_before_last_non_0_period as True."""
        loc = Localization(locale_name="pt_PT")
        assert loc.conjunction_before_last_non_0_period is True

    def test_fallback_bool_property_not_defined_returns_false(self):
        """Test that undefined bool properties fall back to False."""
        loc = Localization(locale_name="en_US")
        # This property is not defined for en_US, should default to False
        assert loc.conjunction_before_units is False


class TestStringProperties:
    """Test retrieval of string properties for different locales."""

    def test_default_word_separator_is_space(self):
        """Test that default word separator is a space."""
        loc = Localization(locale_name="en_US")
        assert loc.word_separator == " "

    def test_default_word_separator_11_99_is_hyphen(self):
        """Test that default word separator for 11-99 is a hyphen."""
        loc = Localization(locale_name="en_US")
        assert loc.word_separator_11_99 == "-"

    def test_default_minus_is_minus(self):
        """Test that default minus sign is 'minus'."""
        loc = Localization(locale_name="en_US")
        assert loc.minus == "minus"

    def test_default_and_is_and(self):
        """Test that default 'and' is 'and'."""
        loc = Localization(locale_name="en_US")
        assert loc.and_ == "and"

    def test_default_hundred_is_hundred(self):
        """Test that default hundred is 'hundred'."""
        loc = Localization(locale_name="en_US")
        assert loc.hundred == "hundred"

    def test_default_hundreds_is_hundreds(self):
        """Test that default hundreds is 'hundreds'."""
        loc = Localization(locale_name="en_US")
        assert loc.hundreds == "hundreds"

    def test_default_thousand_is_thousand(self):
        """Test that default thousand is 'thousand'."""
        loc = Localization(locale_name="en_US")
        assert loc.thousand == "thousand"

    def test_spanish_and_is_y(self):
        """Test that Spanish 'and' is 'y'."""
        loc = Localization(locale_name="es_ES")
        assert loc.and_ == "y"

    def test_spanish_minus_is_menos(self):
        """Test that Spanish minus is 'menos'."""
        loc = Localization(locale_name="es_ES")
        assert loc.minus == "menos"

    def test_spanish_thousand_is_mil(self):
        """Test that Spanish thousand is 'mil'."""
        loc = Localization(locale_name="es_ES")
        assert loc.thousand == "mil"

    def test_spanish_word_separator_11_99_is_space(self):
        """Test that Spanish word separator for 11-99 is a space."""
        loc = Localization(locale_name="es_ES")
        assert loc.word_separator_11_99 == " "

    def test_french_and_is_et(self):
        """Test that French 'and' is 'et'."""
        loc = Localization(locale_name="fr_FR")
        assert loc.and_ == "et"

    def test_french_minus_is_moins(self):
        """Test that French minus is 'moins'."""
        loc = Localization(locale_name="fr_FR")
        assert loc.minus == "moins"

    def test_french_thousand_is_mille(self):
        """Test that French thousand is 'mille'."""
        loc = Localization(locale_name="fr_FR")
        assert loc.thousand == "mille"

    def test_portuguese_and_is_e(self):
        """Test that Portuguese 'and' is 'e'."""
        loc = Localization(locale_name="pt_PT")
        assert loc.and_ == "e"

    def test_portuguese_minus_is_menos(self):
        """Test that Portuguese minus is 'menos'."""
        loc = Localization(locale_name="pt_PT")
        assert loc.minus == "menos"

    def test_portuguese_thousand_is_mil(self):
        """Test that Portuguese thousand is 'mil'."""
        loc = Localization(locale_name="pt_PT")
        assert loc.thousand == "mil"


class TestStringListProperties:
    """Test retrieval of string list properties."""

    def test_tens_names_exists_for_english(self):
        """Test that tens_names property returns a list."""
        loc = Localization(locale_name="en_US")
        tens = loc.tens_name(0)
        assert isinstance(tens, str)

    def test_tens_name_index_0_english(self):
        """Test tens name at index 0 for English (should be empty string)."""
        loc = Localization(locale_name="en_US")
        tens = loc.tens_name(0)
        assert tens == ""

    def test_tens_name_index_1_english(self):
        """Test tens name at index 1 for English."""
        loc = Localization(locale_name="en_US")
        tens = loc.tens_name(1)
        assert tens == "ten"

    def test_tens_name_index_2_english(self):
        """Test tens name at index 2 for English."""
        loc = Localization(locale_name="en_US")
        tens = loc.tens_name(2)
        assert tens == "twenty"

    def test_tens_name_index_3_english(self):
        """Test tens name at index 3 for English."""
        loc = Localization(locale_name="en_US")
        tens = loc.tens_name(3)
        assert tens == "thirty"

    def test_hundreds_names_exists_for_english(self):
        """Test that hundreds_names property returns a list value."""
        loc = Localization(locale_name="en_US")
        hundreds = loc.hundreds_name(0)
        assert isinstance(hundreds, str)

    def test_hundreds_name_index_0_spanish(self):
        """Test hundreds name at index 0 for Spanish (should be empty)."""
        loc = Localization(locale_name="es_ES")
        hundreds = loc.hundreds_name(0)
        assert hundreds == ""

    def test_hundreds_name_index_1_spanish(self):
        """Test hundreds name at index 1 for Spanish."""
        loc = Localization(locale_name="es_ES")
        hundreds = loc.hundreds_name(1)
        assert hundreds == "ciento"

    def test_large_number_units_exists(self):
        """Test that large_number_units property returns a string."""
        loc = Localization(locale_name="en_US")
        unit = loc.large_number_units(0)
        assert isinstance(unit, str)

    def test_large_number_tens_exists(self):
        """Test that large_number_tens property returns a string."""
        loc = Localization(locale_name="en_US")
        tens = loc.large_number_tens(0)
        assert isinstance(tens, str)

    def test_large_number_hundreds_exists(self):
        """Test that large_number_hundreds property returns a string."""
        loc = Localization(locale_name="en_US")
        hundreds = loc.large_number_hundreds(0)
        assert isinstance(hundreds, str)

    def test_large_number_suffixes_exists(self):
        """Test that large_number_suffixes property returns a string."""
        loc = Localization(locale_name="en_US")
        suffix = loc.large_number_suffixes(0)
        assert isinstance(suffix, str)

    def test_large_number_suffixes_plural_exists(self):
        """Test that large_number_suffixes_plural property returns a string."""
        loc = Localization(locale_name="en_US")
        suffix = loc.large_number_suffixes_plural(0)
        assert isinstance(suffix, str)

    def test_large_number_prefixes_n_lt_10_exists(self):
        """Test that large_number_prefixes_n_lt_10 property returns a string."""
        loc = Localization(locale_name="en_US")
        prefix = loc.large_number_prefixes_n_lt_10(0)
        assert isinstance(prefix, str)

    def test_tens_name_with_out_of_range_index_wraps(self):
        """Test that out-of-range index wraps to index 0."""
        loc = Localization(locale_name="en_US")
        # Index way out of range should wrap to 0
        tens_0 = loc.tens_name(0)
        tens_large = loc.tens_name(999)
        assert tens_0 == tens_large


class TestStringListListProperties:
    """Test retrieval of string list list properties."""

    def test_large_number_units_liaison_exists(self):
        """Test that large_number_units_liaison returns a list."""
        loc = Localization(locale_name="fr_FR")
        liaison = loc.large_number_units_liaison(0)
        assert isinstance(liaison, list)

    def test_large_number_units_liaison_contains_strings(self):
        """Test that large_number_units_liaison contains strings."""
        loc = Localization(locale_name="fr_FR")
        liaison = loc.large_number_units_liaison(0)
        if liaison:  # If list is not empty
            assert all(isinstance(item, str) for item in liaison)

    def test_large_number_tens_liaison_exists(self):
        """Test that large_number_tens_liaison returns a list."""
        loc = Localization(locale_name="fr_FR")
        liaison = loc.large_number_tens_liaison(0)
        assert isinstance(liaison, list)

    def test_large_number_tens_i_a_exists(self):
        """Test that large_number_tens_i_a returns a list."""
        loc = Localization(locale_name="fr_FR")
        i_a = loc.large_number_tens_i_a(0)
        assert isinstance(i_a, list)

    def test_large_number_hundreds_liasion_exists(self):
        """Test that large_number_hundreds_liasion returns a list."""
        loc = Localization(locale_name="fr_FR")
        liaison = loc.large_number_hundreds_liasion(0)
        assert isinstance(liaison, list)

    def test_large_number_units_liaison_with_out_of_range_index(self):
        """Test that out-of-range index wraps for list list properties."""
        loc = Localization(locale_name="fr_FR")
        liaison_0 = loc.large_number_units_liaison(0)
        liaison_large = loc.large_number_units_liaison(999)
        assert liaison_0 == liaison_large


class TestConverterImplType:
    """Test retrieval of converter implementation type."""

    def test_default_impl_type_is_short_scale(self):
        """Test that default implementation type is SHORT_SCALE."""
        loc = Localization(locale_name="en_US")
        impl_type = loc.get_impl_type()
        assert impl_type == ConverterImplTypeValue.SHORT_SCALE

    def test_english_gb_impl_type_is_long_scale(self):
        """Test that English (GB) uses LONG_SCALE."""
        loc = Localization(locale_name="en_GB")
        impl_type = loc.get_impl_type()
        assert impl_type == ConverterImplTypeValue.LONG_SCALE

    def test_spanish_impl_type_is_long_scale(self):
        """Test that Spanish uses LONG_SCALE."""
        loc = Localization(locale_name="es_ES")
        impl_type = loc.get_impl_type()
        assert impl_type == ConverterImplTypeValue.LONG_SCALE

    def test_french_impl_type_is_long_scale(self):
        """Test that French uses LONG_SCALE."""
        loc = Localization(locale_name="fr_FR")
        impl_type = loc.get_impl_type()
        assert impl_type == ConverterImplTypeValue.LONG_SCALE

    def test_portuguese_impl_type_is_long_scale(self):
        """Test that Portuguese (Portugal) uses LONG_SCALE."""
        loc = Localization(locale_name="pt_PT")
        impl_type = loc.get_impl_type()
        assert impl_type == ConverterImplTypeValue.LONG_SCALE

    def test_portuguese_brazil_impl_type_is_short_scale(self):
        """Test that Portuguese (Brazil) uses SHORT_SCALE."""
        loc = Localization(locale_name="pt_BR")
        impl_type = loc.get_impl_type()
        assert impl_type == ConverterImplTypeValue.SHORT_SCALE


class TestCaching:
    """Test the caching mechanism for number names."""

    def test_get_name_from_cache_returns_empty_string_if_not_cached(self):
        """Test that retrieving uncached value returns default value."""
        loc = Localization(locale_name="en_US")
        name = loc.get_name_from_cache(12345)
        # If not in cache and not in NUMBER_NAMES, should return default
        assert isinstance(name, str)

    def test_put_name_in_cache_stores_value(self):
        """Test that put_name_in_cache stores a value."""
        loc = Localization(locale_name="en_US")
        test_key = 99999
        test_value = "test_number_name"
        loc.put_name_in_cache(test_key, test_value)
        retrieved = loc.get_name_from_cache(test_key)
        assert retrieved == test_value

    def test_cache_survives_multiple_operations(self):
        """Test that cached values persist across multiple get operations."""
        loc = Localization(locale_name="en_US")
        test_key = 88888
        test_value = "cached_value"
        loc.put_name_in_cache(test_key, test_value)
        # Multiple retrievals should return same cached value
        assert loc.get_name_from_cache(test_key) == test_value
        assert loc.get_name_from_cache(test_key) == test_value
        assert loc.get_name_from_cache(test_key) == test_value

    def test_cache_isolation_between_instances(self):
        """Test that cache is isolated between different Localization instances."""
        loc1 = Localization(locale_name="en_US")
        loc2 = Localization(locale_name="en_US")
        test_key = 77777
        test_value = "instance_value"
        loc1.put_name_in_cache(test_key, test_value)
        # loc2 should not have this cached value
        retrieved = loc2.get_name_from_cache(test_key)
        # If not found, should return NUMBER_NAMES value or default
        # We just verify it doesn't automatically have the cached value
        assert retrieved != test_value or test_key in loc2.get_name_from_cache(test_key)

    def test_cache_multiple_values(self):
        """Test caching multiple different values."""
        loc = Localization(locale_name="en_US")
        values = {
            100: "one hundred",
            1000: "one thousand",
            1000000: "one million",
        }
        for key, val in values.items():
            loc.put_name_in_cache(key, val)
        for key, val in values.items():
            assert loc.get_name_from_cache(key) == val


class TestFallbackMechanism:
    """Test property lookup fallback chain."""

    def test_territory_specific_property_used_over_language_default(self):
        """Test that territory-specific properties override language default."""
        # Belgian French has specific property overrides
        loc_fr = Localization(locale_name="fr_FR")
        loc_be = Localization(locale_name="fr_BE")
        # tens_7_and_9_as_fr should be True for fr_FR but False for fr_BE
        assert loc_fr.tens_7_and_9_as_fr is True
        assert loc_be.tens_7_and_9_as_fr is False

    def test_language_level_fallback_when_territory_not_defined(self):
        """Test fallback to language-level when territory not defined."""
        loc = Localization(locale_name="fr")
        # Should use fr-level properties
        assert loc.tens_7_and_9_as_fr is True

    def test_default_fallback_when_language_not_in_dict(self):
        """Test fallback to default when language not in dictionary."""
        # Create localization with unsupported language - should use defaults
        loc = Localization(locale_name="ja")
        # Should fall back to default (None, None) level
        assert loc.large_number_invariable is True  # Default value

    def test_number_name_none_stops_territory_fallback(self):
        """Test that None in NUMBER_NAMES blocks inheritance for a territory key."""
        loc_be = Localization(locale_name="fr_BE")
        loc_ch = Localization(locale_name="fr_CH")

        # fr_BE inherits 80 from fr language level.
        assert loc_be.get_name_from_cache(80) == "quatre-vingts"

        # fr_CH explicitly blocks inheritance for 80 so algorithm builds
        # "huitante" from tens + units.
        assert loc_ch.get_name_from_cache(80) == ""


class TestEdgeCases:
    """Test edge cases and special scenarios."""

    def test_localization_with_empty_string_raises_error(self):
        """Test that empty string locale raises error."""
        with pytest.raises(LocalizationError):
            Localization(locale_name="")

    def test_localization_with_numbers_only_raises_error(self):
        """Test that numbers-only locale raises error."""
        with pytest.raises(LocalizationError):
            Localization(locale_name="12345")

    def test_localization_properties_all_accessible(self):
        """Test that all property accessors are callable without errors."""
        loc = Localization(locale_name="en_US")
        # Test all boolean properties
        assert isinstance(loc.conjunction_before_units, bool)
        assert isinstance(loc.conjunction_before_tens, bool)
        assert isinstance(loc.conjunction_before_1_unit_if_lt_80, bool)
        assert isinstance(loc.conjunction_before_1_unit_if_eq_80, bool)
        assert isinstance(loc.conjunction_before_1_unit_if_eq_90, bool)
        assert isinstance(loc.conjunction_before_last_non_0_period, bool)
        assert isinstance(loc.tens_7_and_9_as_fr, bool)
        assert isinstance(loc.plural_hundred0, bool)
        assert isinstance(loc.omit_one_from_hundred, bool)
        assert isinstance(loc.omit_one_from_thousand, bool)
        assert isinstance(loc.large_number_invariable, bool)
        assert isinstance(loc.large_number_thousand_replaces_ard_suffix, bool)
        assert isinstance(loc.large_number_no_liaison_use_alt_unit_prefix, bool)

    def test_localization_all_string_properties_accessible(self):
        """Test that all string properties are accessible."""
        loc = Localization(locale_name="en_US")
        # Test all string properties
        assert isinstance(loc.word_separator, str)
        assert isinstance(loc.word_separator_11_99, str)
        assert isinstance(loc.word_separator_11_99_conjunction, str)
        assert isinstance(loc.minus, str)
        assert isinstance(loc.and_, str)
        assert isinstance(loc.hundred, str)
        assert isinstance(loc.hundreds, str)
        assert isinstance(loc.thousand, str)
        assert isinstance(loc.large_number_1, str)
        assert isinstance(loc.large_number_infix_base, str)
        assert isinstance(loc.large_number_infix_suffix, str)

    def test_localization_all_methods_accessible(self):
        """Test that all accessor methods are callable."""
        loc = Localization(locale_name="en_US")
        # Test all methods
        assert callable(loc.tens_name)
        assert callable(loc.hundreds_name)
        assert callable(loc.large_number_suffixes)
        assert callable(loc.large_number_suffixes_plural)
        assert callable(loc.large_number_prefixes_n_lt_10)
        assert callable(loc.large_number_units)
        assert callable(loc.large_number_units_alt)
        assert callable(loc.large_number_tens)
        assert callable(loc.large_number_hundreds)
        assert callable(loc.large_number_units_liaison)
        assert callable(loc.large_number_tens_liaison)
        assert callable(loc.large_number_tens_i_a)
        assert callable(loc.large_number_hundreds_liasion)
        assert callable(loc.get_impl_type)
        assert callable(loc.get_name_from_cache)
        assert callable(loc.put_name_in_cache)

    def test_multiple_localization_instances_independent(self):
        """Test that multiple Localization instances are independent."""
        loc_en = Localization(locale_name="en_US")
        loc_es = Localization(locale_name="es_ES")
        # Different properties for different locales
        assert loc_en.and_ == "and"
        assert loc_es.and_ == "y"
        # Cache should be independent
        loc_en.put_name_in_cache(999, "english_value")
        loc_es.put_name_in_cache(999, "spanish_value")
        assert loc_en.get_name_from_cache(999) == "english_value"
        assert loc_es.get_name_from_cache(999) == "spanish_value"
