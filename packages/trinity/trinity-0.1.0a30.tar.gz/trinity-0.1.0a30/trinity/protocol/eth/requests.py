from typing import (
    Any,
    Dict,
    Sequence,
)

from eth_typing import (
    BlockIdentifier,
    Hash32,
)
from p2p.abc import RequestAPI

from trinity.protocol.eth.constants import MAX_HEADERS_FETCH
from trinity.protocol.common.requests import (
    BaseHeaderRequest,
)

from .commands import (
    BlockBodies,
    BlockHeaders,
    GetBlockBodies,
    GetBlockHeaders,
    GetNodeData,
    GetReceipts,
    NodeData,
    Receipts,
)


class HeaderRequest(BaseHeaderRequest):
    """
    TODO: this should be removed from this module.  It exists to allow
    `trinity.protocol.eth.servers.PeerRequestHandler` to have a common API between light and
    full chains so maybe it should go there
    """
    max_size = MAX_HEADERS_FETCH

    def __init__(self,
                 block_number_or_hash: BlockIdentifier,
                 max_headers: int,
                 skip: int,
                 reverse: bool) -> None:
        self.block_number_or_hash = block_number_or_hash
        self.max_headers = max_headers
        self.skip = skip
        self.reverse = reverse


class GetBlockHeadersRequest(RequestAPI[Dict[str, Any]]):
    cmd_type = GetBlockHeaders
    response_type = BlockHeaders

    def __init__(self,
                 block_number_or_hash: BlockIdentifier,
                 max_headers: int,
                 skip: int,
                 reverse: bool) -> None:
        self.command_payload = {
            'block_number_or_hash': block_number_or_hash,
            'max_headers': max_headers,
            'skip': skip,
            'reverse': reverse
        }


class GetReceiptsRequest(RequestAPI[Sequence[Hash32]]):
    cmd_type = GetReceipts
    response_type = Receipts

    def __init__(self, block_hashes: Sequence[Hash32]) -> None:
        self.command_payload = block_hashes


class GetNodeDataRequest(RequestAPI[Sequence[Hash32]]):
    cmd_type = GetNodeData
    response_type = NodeData

    def __init__(self, node_hashes: Sequence[Hash32]) -> None:
        self.command_payload = node_hashes


class GetBlockBodiesRequest(RequestAPI[Sequence[Hash32]]):
    cmd_type = GetBlockBodies
    response_type = BlockBodies

    def __init__(self, block_hashes: Sequence[Hash32]) -> None:
        self.command_payload = block_hashes
