"""Tests for the AST-based safe calculator."""
import pytest
from forgix.skills.builtin.calculator import calculate


@pytest.mark.asyncio
async def test_addition():
    result = await calculate("2 + 2")
    assert "4" in result


@pytest.mark.asyncio
async def test_subtraction():
    result = await calculate("10 - 7")
    assert "3" in result


@pytest.mark.asyncio
async def test_multiplication():
    result = await calculate("3 * 4")
    assert "12" in result


@pytest.mark.asyncio
async def test_division():
    result = await calculate("10 / 4")
    assert "2.5" in result


@pytest.mark.asyncio
async def test_integer_division():
    result = await calculate("10 // 3")
    assert "3" in result


@pytest.mark.asyncio
async def test_modulo():
    result = await calculate("10 % 3")
    assert "1" in result


@pytest.mark.asyncio
async def test_power():
    result = await calculate("2 ** 10")
    assert "1024" in result


@pytest.mark.asyncio
async def test_parentheses():
    result = await calculate("(2 + 3) * 4")
    assert "20" in result


@pytest.mark.asyncio
async def test_sqrt():
    result = await calculate("sqrt(16)")
    assert "4" in result


@pytest.mark.asyncio
async def test_negative_unary():
    result = await calculate("-5 + 3")
    assert "-2" in result


@pytest.mark.asyncio
async def test_pi_constant():
    result = await calculate("pi")
    assert "3.14" in result


@pytest.mark.asyncio
async def test_no_eval_import():
    result = await calculate("__import__('os').system('id')")
    assert "[Calculation error" in result or "[Error" in result


@pytest.mark.asyncio
async def test_no_attribute_access():
    result = await calculate("(1).__class__")
    assert "[Calculation error" in result or "[Error" in result


@pytest.mark.asyncio
async def test_string_constant_rejected():
    result = await calculate("'hello'")
    assert "[Calculation error" in result or "[Error" in result


@pytest.mark.asyncio
async def test_output_includes_expression():
    result = await calculate("2 + 2")
    assert "2 + 2" in result


@pytest.mark.asyncio
async def test_division_by_zero():
    result = await calculate("1 / 0")
    assert "zero" in result.lower() or "[Error" in result


@pytest.mark.asyncio
async def test_factorial():
    result = await calculate("factorial(5)")
    assert "120" in result
