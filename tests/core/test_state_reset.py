import pytest

from eth_tester import EthereumTester, MockBackend
from eth_tester.exceptions import TransactionNotFound


def test_reset_to_genesis_discards_queued_transactions():
    tester = EthereumTester(backend=MockBackend())
    tester.disable_auto_mine_transactions()
    transaction_hash = tester.send_transaction(
        {
            "from": "0x" + "1" * 40,
            "to": "0x" + "2" * 40,
            "gas": 21000,
            "value": 1,
            "data": "0x1234",
            "nonce": 0,
        }
    )

    tester.reset_to_genesis()
    tester.mine_block()

    with pytest.raises(TransactionNotFound):
        tester.get_transaction_receipt(transaction_hash)
