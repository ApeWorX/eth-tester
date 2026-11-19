import pytest
from eth_bloom import BloomFilter
from eth_utils import decode_hex, encode_hex

from eth_tester import EthereumTester, MockBackend, PyEVMBackend


@pytest.mark.parametrize("backend_class", [MockBackend, PyEVMBackend])
def test_receipt_logs_bloom_for_empty_logs(backend_class):
    tester = EthereumTester(backend=backend_class())
    accounts = tester.get_accounts()
    tx_hash = tester.send_transaction(
        {"from": accounts[0], "to": accounts[1], "gas": 21_000}
    )
    receipt = tester.get_transaction_receipt(tx_hash)
    assert receipt["logs"] == []
    assert receipt["logs_bloom"] == 0


@pytest.mark.parametrize("backend_class", [MockBackend, PyEVMBackend])
def test_pending_backend_receipt_logs_bloom(backend_class):
    backend = backend_class()
    accounts = backend.get_accounts()
    tx_hash = backend.send_transaction(
        {"from": accounts[0], "to": accounts[1], "gas": 21_000}
    )
    receipt = backend.get_transaction_receipt(tx_hash)
    assert receipt["block_number"] is None
    assert receipt["logs_bloom"] == 0


def test_receipt_logs_bloom_is_per_transaction():
    addresses = [b"\x11" * 20, b"\x22" * 20]
    genesis_state = PyEVMBackend.generate_genesis_state()
    for address, topic in zip(addresses, (42, 43), strict=True):
        genesis_state[address] = {
            "balance": 0,
            "nonce": 0,
            # PUSH1 topic; PUSH1 0; PUSH1 0; LOG1; STOP
            "code": bytes([0x60, topic, 0x60, 0, 0x60, 0, 0xA1, 0]),
            "storage": {},
        }
    tester = EthereumTester(backend=PyEVMBackend(genesis_state=genesis_state))
    tester.disable_auto_mine_transactions()
    accounts = tester.get_accounts()
    tx_hashes = [
        tester.send_transaction(
            {"from": account, "to": encode_hex(address), "gas": 50_000}
        )
        for account, address in zip(accounts[:2], addresses, strict=True)
    ]
    tester.mine_blocks()
    blooms = []
    for tx_hash in tx_hashes:
        receipt = tester.get_transaction_receipt(tx_hash)
        assert receipt["status"] == 1
        assert len(receipt["logs"]) == 1
        log = receipt["logs"][0]
        expected = int(
            BloomFilter.from_iterable(
                [decode_hex(log["address"]), *map(decode_hex, log["topics"])]
            )
        )
        assert receipt["logs_bloom"] == expected
        assert receipt["logs_bloom"] != 0
        blooms.append(receipt["logs_bloom"])
    assert blooms[0] != blooms[1]
    assert tester.get_block_by_number("latest")["logs_bloom"] == blooms[0] | blooms[1]
