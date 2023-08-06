from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List

from botocore.client import BaseClient
from botocore.paginate import Paginator
from botocore.waiter import Waiter


class Client(BaseClient):

    # pylint: disable=arguments-differ
    def accept_direct_connect_gateway_association_proposal(
        self,
        directConnectGatewayId: str,
        proposalId: str,
        associatedGatewayOwnerAccount: str,
        overrideAllowedPrefixesToDirectConnectGateway: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def allocate_connection_on_interconnect(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def allocate_hosted_connection(
        self,
        connectionId: str,
        ownerAccount: str,
        bandwidth: str,
        connectionName: str,
        vlan: int,
        tags: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def allocate_private_virtual_interface(
        self,
        connectionId: str,
        ownerAccount: str,
        newPrivateVirtualInterfaceAllocation: Dict[str, Any],
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def allocate_public_virtual_interface(
        self,
        connectionId: str,
        ownerAccount: str,
        newPublicVirtualInterfaceAllocation: Dict[str, Any],
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def allocate_transit_virtual_interface(
        self,
        connectionId: str,
        ownerAccount: str,
        newTransitVirtualInterfaceAllocation: Dict[str, Any],
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def associate_connection_with_lag(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def associate_hosted_connection(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def associate_virtual_interface(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def can_paginate(self, operation_name: str = None) -> None:
        pass

    # pylint: disable=arguments-differ
    def confirm_connection(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def confirm_private_virtual_interface(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def confirm_public_virtual_interface(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def confirm_transit_virtual_interface(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_bgp_peer(
        self, virtualInterfaceId: str = None, newBGPPeer: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_connection(
        self,
        location: str,
        bandwidth: str,
        connectionName: str,
        lagId: str = None,
        tags: List[Any] = None,
        providerName: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_direct_connect_gateway(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_direct_connect_gateway_association(
        self,
        directConnectGatewayId: str,
        gatewayId: str = None,
        addAllowedPrefixesToDirectConnectGateway: List[Any] = None,
        virtualGatewayId: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_direct_connect_gateway_association_proposal(
        self,
        directConnectGatewayId: str,
        directConnectGatewayOwnerAccount: str,
        gatewayId: str,
        addAllowedPrefixesToDirectConnectGateway: List[Any] = None,
        removeAllowedPrefixesToDirectConnectGateway: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_interconnect(
        self,
        interconnectName: str,
        bandwidth: str,
        location: str,
        lagId: str = None,
        tags: List[Any] = None,
        providerName: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_lag(
        self,
        numberOfConnections: int,
        location: str,
        connectionsBandwidth: str,
        lagName: str,
        connectionId: str = None,
        tags: List[Any] = None,
        childConnectionTags: List[Any] = None,
        providerName: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_private_virtual_interface(
        self, connectionId: str, newPrivateVirtualInterface: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_public_virtual_interface(
        self, connectionId: str, newPublicVirtualInterface: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_transit_virtual_interface(
        self, connectionId: str, newTransitVirtualInterface: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def delete_bgp_peer(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_connection(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_direct_connect_gateway(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_direct_connect_gateway_association(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_direct_connect_gateway_association_proposal(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_interconnect(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_lag(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_virtual_interface(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_connection_loa(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_connections(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_connections_on_interconnect(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_direct_connect_gateway_association_proposals(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_direct_connect_gateway_associations(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_direct_connect_gateway_attachments(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_direct_connect_gateways(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_hosted_connections(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_interconnect_loa(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_interconnects(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_lags(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_loa(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_locations(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_tags(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_virtual_gateways(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def describe_virtual_interfaces(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def disassociate_connection_from_lag(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def generate_presigned_url(
        self,
        ClientMethod: str = None,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = None,
        HttpMethod: str = None,
    ) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_paginator(self, operation_name: str = None) -> Paginator:
        pass

    # pylint: disable=arguments-differ
    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    # pylint: disable=arguments-differ
    def tag_resource(self, resourceArn: str, tags: List[Any]) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def untag_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_direct_connect_gateway_association(
        self,
        associationId: str = None,
        addAllowedPrefixesToDirectConnectGateway: List[Any] = None,
        removeAllowedPrefixesToDirectConnectGateway: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def update_lag(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_virtual_interface_attributes(self) -> None:
        pass
