from pkg.calculator import Calculator

c = Calculator()
print("3 + 7 * 2 =", c.evaluate("3 + 7 * 2"))  # Should be 17
print("2 * 3 + 1 =", c.evaluate("2 * 3 + 1"))  # Should be 7
print("10 - 2 * 3 =", c.evaluate("10 - 2 * 3"))  # Should be 4
