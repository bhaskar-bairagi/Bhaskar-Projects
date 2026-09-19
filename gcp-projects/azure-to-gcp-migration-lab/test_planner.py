import unittest

from planner import Application, assess


class PlannerTest(unittest.TestCase):
    def test_stateless_pilot(self):
        result = assess(Application("orders", "Azure VM", "Linux", False, True, 1, 10, False))
        self.assertEqual((result["route"], result["wave"]), ("Containerize and deploy", "Pilot wave"))

    def test_stateful_regulated_later(self):
        result = assess(Application("billing", "Azure VM", "Windows", True, False, 4, 200, True))
        self.assertEqual((result["route"], result["wave"]), ("VM first, then modernize", "Later wave"))

    def test_invalid_inventory(self):
        with self.assertRaises(ValueError):
            assess(Application("", "Azure VM", "Linux", False, False, -1, 0, False))


if __name__ == "__main__":
    unittest.main()
