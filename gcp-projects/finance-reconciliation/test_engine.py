import unittest
from pathlib import Path

from engine import reconcile

SAMPLES = Path(__file__).parent / "samples"


class ReconciliationTest(unittest.TestCase):
    def test_sample_exception_classes(self):
        rows = reconcile((SAMPLES / "ledger.csv").read_text(), (SAMPLES / "settlement.csv").read_text())
        self.assertEqual({row["transaction_id"]: row["status"] for row in rows}, {
            "TX-100": "matched", "TX-101": "amount_mismatch", "TX-102": "currency_mismatch",
            "TX-103": "ledger_only", "TX-104": "settlement_only"})

    def test_duplicate_key_rejected(self):
        row = "transaction_id,amount,currency\nA,1.00,GBP\n"
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            reconcile(row + "A,1.00,GBP\n", row)

    def test_invalid_amount_rejected(self):
        with self.assertRaisesRegex(ValueError, "Invalid amount"):
            reconcile("transaction_id,amount,currency\nA,NaN,GBP\n",
                      "transaction_id,amount,currency\nA,1,GBP\n")


if __name__ == "__main__":
    unittest.main()
