from eth_utils import (
    decode_hex,
    encode_hex,
    to_canonical_address,
)
from eth_utils.toolz import (
    identity,
)

from .base import (
    BaseNormalizer,
)
from .common import (
    int_to_32byte_hex,
    to_integer_if_hex,
)
from .inbound import (
    normalize_filter_params as normalize_inbound_filter_params,
)
from .inbound import (
    normalize_log_entry as normalize_inbound_log_entry,
)
from .inbound import (
    normalize_private_key as normalize_inbound_private_key,
)
from .inbound import (
    normalize_raw_transaction as normalize_inbound_raw_transaction,
)
from .inbound import (
    normalize_transaction as normalize_inbound_transaction,
)
from .outbound import (
    normalize_account as normalize_outbound_account,
)
from .outbound import (
    normalize_account_list as normalize_outbound_account_list,
)
from .outbound import (
    normalize_block as normalize_outbound_block,
)
from .outbound import (
    normalize_log_entry as normalize_outbound_log_entry,
)
from .outbound import (
    normalize_receipt as normalize_outbound_receipt,
)
from .outbound import (
    normalize_transaction as normalize_outbound_transaction,
)


class DefaultNormalizer(BaseNormalizer):
    #
    # Inbound
    #
    normalize_inbound_account = staticmethod(to_canonical_address)
    normalize_inbound_block_hash = staticmethod(decode_hex)
    normalize_inbound_block_number = staticmethod(identity)
    normalize_inbound_filter_id = staticmethod(identity)
    normalize_inbound_filter_params = staticmethod(normalize_inbound_filter_params)
    normalize_inbound_log_entry = staticmethod(normalize_inbound_log_entry)
    normalize_inbound_private_key = staticmethod(normalize_inbound_private_key)
    normalize_inbound_raw_transaction = staticmethod(normalize_inbound_raw_transaction)
    normalize_inbound_storage_slot = staticmethod(to_integer_if_hex)
    normalize_inbound_timestamp = staticmethod(identity)
    normalize_inbound_transaction = staticmethod(normalize_inbound_transaction)
    normalize_inbound_transaction_hash = staticmethod(decode_hex)

    # Outbound
    normalize_outbound_account = staticmethod(normalize_outbound_account)
    normalize_outbound_account_list = staticmethod(normalize_outbound_account_list)
    normalize_outbound_balance = staticmethod(identity)
    normalize_outbound_block_hash = staticmethod(encode_hex)
    normalize_outbound_block = staticmethod(normalize_outbound_block)
    normalize_outbound_code = staticmethod(encode_hex)
    normalize_outbound_filter_id = staticmethod(identity)
    normalize_outbound_log_entry = staticmethod(normalize_outbound_log_entry)
    normalize_outbound_gas_estimate = staticmethod(identity)
    normalize_outbound_nonce = staticmethod(identity)
    normalize_outbound_receipt = staticmethod(normalize_outbound_receipt)
    normalize_outbound_return_data = staticmethod(encode_hex)
    normalize_outbound_storage = staticmethod(int_to_32byte_hex)
    normalize_outbound_transaction = staticmethod(normalize_outbound_transaction)
    normalize_outbound_transaction_hash = staticmethod(encode_hex)
