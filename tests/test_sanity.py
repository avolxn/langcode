"""Sanity tests to ensure basic project setup is working."""


def test_imports() -> None:
    """Test that the package can be imported."""
    import langcode

    assert langcode is not None


def test_python_version() -> None:
    """Test that we're running on Python 3.11+."""
    import sys

    assert sys.version_info >= (3, 11)
