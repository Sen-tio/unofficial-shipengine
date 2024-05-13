import unittest

if __name__ == "__main__":
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover(".", pattern="test_*.py")

    runner = unittest.TextTestRunner()
    runner.run(test_suite)
