#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `cronshield` package."""

import os
import re
from pathlib import Path

from click.testing import CliRunner

from cronshield import cli


def test_no_args():
    """Test the CLI with no args."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 2
    assert "Missing argument" in result.output


def test_help():
    """Test the CLI's --help option."""
    runner = CliRunner()
    help_result = runner.invoke(cli.main, ["--help"])
    assert help_result.exit_code == 0
    assert re.search(r"--help\s+Show this message and exit.", help_result.output) is not None


def test_success():
    """Test that the successful execution suppresses output."""
    runner = CliRunner()
    help_result = runner.invoke(cli.main, ["--", "python", "-c", "import sys; print('hello'); sys.exit(0)"])
    assert help_result.exit_code == 0
    assert len(help_result.output) == 0


def test_error():
    """Test that the error is reported."""
    runner = CliRunner()
    help_result = runner.invoke(cli.main, ["--", "python", "-c", "import sys; print('hello'); sys.exit(1)"])
    assert help_result.exit_code == 1
    assert re.search(r"cronshield detected failure or error output for the command", help_result.output) is not None
    assert "hello" in help_result.output


def test_touchfile(tmp_path: Path):
    """Test that a touchfile is created when the parameter is provided."""
    error_touchfile = tmp_path / "error-touchfile"

    assert not error_touchfile.exists()

    runner = CliRunner()
    help_result = runner.invoke(cli.main, [
        "--error-touchfile", error_touchfile,
        "--", "python", "-c", "import sys; print('hello'); sys.exit(1)"])
    assert help_result.exit_code == 1

    assert error_touchfile.exists()


def test_touchfile_update(tmp_path: Path):
    """Test that a touchfile's mtime is updated."""
    error_touchfile = tmp_path / "error-touchfile"

    error_touchfile.touch()
    os.utime(error_touchfile, (0, 0))
    assert error_touchfile.stat().st_mtime == 0

    runner = CliRunner()
    help_result = runner.invoke(cli.main, [
        "--error-touchfile", error_touchfile,
        "--", "python", "-c", "import sys; print('hello'); sys.exit(1)"])
    assert help_result.exit_code == 1

    assert error_touchfile.exists()
    assert error_touchfile.stat().st_mtime != 0


def test_report_probability():
    """Test that the error is not reported when report-probability is set to 0."""
    runner = CliRunner()
    help_result = runner.invoke(cli.main, [
        "--report-probability", 0,
        "--", "python", "-c", "import sys; print('hello'); sys.exit(1)"])
    assert help_result.exit_code == 1
    assert len(help_result.output) == 0
