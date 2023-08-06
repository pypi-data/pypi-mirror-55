#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `cronshield` package."""

import os
from pathlib import Path

from click.testing import CliRunner

from cronshield import cli


def test_no_touchfile():
    """Test that we raise an error when we don't get a touchfile when a max_failure_interval is specified.."""
    runner = CliRunner()
    help_result = runner.invoke(cli.main, [
        "--max-failure-interval", 10,
        "--", "python", "-c", "import sys; print('hello'); sys.exit(1)"])
    assert help_result.exit_code != 0


def test_not_masked(tmp_path: Path):
    """Test that we don't mask an error that has happened recently."""
    error_touchfile = tmp_path / "error-touchfile"

    error_touchfile.touch()

    runner = CliRunner()
    help_result = runner.invoke(cli.main, [
        "--error-touchfile", error_touchfile,
        "--max-failure-interval", 1000,
        "--", "python", "-c", "import sys; print('hello'); sys.exit(1)"])
    assert help_result.exit_code == 1
    assert len(help_result.stdout) != 0

    assert error_touchfile.exists()


def test_masked(tmp_path: Path):
    """Test that we mask an error that has happened a long time ago."""
    error_touchfile = tmp_path / "error-touchfile"

    error_touchfile.touch()
    os.utime(error_touchfile, (0, 0))

    runner = CliRunner()
    help_result = runner.invoke(cli.main, [
        "--error-touchfile", error_touchfile,
        "--max-failure-interval", 1000,
        "--", "python", "-c", "import sys; print('hello'); sys.exit(1)"])
    assert help_result.exit_code == 1
    assert len(help_result.stdout) == 0

    assert error_touchfile.exists()
