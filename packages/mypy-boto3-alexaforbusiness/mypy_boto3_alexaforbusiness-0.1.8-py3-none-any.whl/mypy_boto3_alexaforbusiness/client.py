from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List

from botocore.client import BaseClient
from botocore.paginate import Paginator
from botocore.waiter import Waiter


class Client(BaseClient):
    # pylint: disable=arguments-differ
    def approve_skill(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def associate_contact_with_address_book(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def associate_device_with_network_profile(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def associate_device_with_room(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def associate_skill_group_with_room(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def associate_skill_with_skill_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def associate_skill_with_users(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def can_paginate(self, operation_name: str = None) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_address_book(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_business_report_schedule(
        self,
        Format: str,
        ContentRange: Dict[str, Any],
        ScheduleName: str = None,
        S3BucketName: str = None,
        S3KeyPrefix: str = None,
        Recurrence: Dict[str, Any] = None,
        ClientRequestToken: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_conference_provider(
        self,
        ConferenceProviderName: str,
        ConferenceProviderType: str,
        MeetingSetting: Dict[str, Any],
        IPDialIn: Dict[str, Any] = None,
        PSTNDialIn: Dict[str, Any] = None,
        ClientRequestToken: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_contact(
        self,
        FirstName: str,
        DisplayName: str = None,
        LastName: str = None,
        PhoneNumber: str = None,
        PhoneNumbers: List[Any] = None,
        SipAddresses: List[Any] = None,
        ClientRequestToken: str = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_gateway_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_network_profile(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_profile(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_room(
        self,
        RoomName: str,
        Description: str = None,
        ProfileArn: str = None,
        ProviderCalendarId: str = None,
        ClientRequestToken: str = None,
        Tags: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def create_skill_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def create_user(
        self,
        UserId: str,
        FirstName: str = None,
        LastName: str = None,
        Email: str = None,
        ClientRequestToken: str = None,
        Tags: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def delete_address_book(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_business_report_schedule(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_conference_provider(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_contact(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_device(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_device_usage_data(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_gateway_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_network_profile(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_profile(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_room(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_room_skill_parameter(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_skill_authorization(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_skill_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def delete_user(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def disassociate_contact_from_address_book(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def disassociate_device_from_room(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def disassociate_skill_from_skill_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def disassociate_skill_from_users(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def disassociate_skill_group_from_room(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def forget_smart_home_appliances(self) -> None:
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
    def get_address_book(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_conference_preference(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_conference_provider(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_contact(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_device(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_gateway(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_gateway_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_invitation_configuration(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_network_profile(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_paginator(self, operation_name: str = None) -> Paginator:
        pass

    # pylint: disable=arguments-differ
    def get_profile(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_room(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_room_skill_parameter(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_skill_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    # pylint: disable=arguments-differ
    def list_business_report_schedules(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_conference_providers(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_device_events(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_gateway_groups(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_gateways(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_skills(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_skills_store_categories(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_skills_store_skills_by_category(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_smart_home_appliances(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def list_tags(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_conference_preference(
        self, ConferencePreference: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def put_invitation_configuration(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def put_room_skill_parameter(
        self, SkillId: str, RoomSkillParameter: Dict[str, Any], RoomArn: str = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def put_skill_authorization(
        self, AuthorizationResult: Dict[str, Any], SkillId: str, RoomArn: str = None
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def register_avs_device(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def reject_skill(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def resolve_room(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def revoke_invitation(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def search_address_books(
        self,
        Filters: List[Any] = None,
        SortCriteria: List[Any] = None,
        NextToken: str = None,
        MaxResults: int = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def search_contacts(
        self,
        Filters: List[Any] = None,
        SortCriteria: List[Any] = None,
        NextToken: str = None,
        MaxResults: int = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def search_devices(
        self,
        NextToken: str = None,
        MaxResults: int = None,
        Filters: List[Any] = None,
        SortCriteria: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def search_network_profiles(
        self,
        NextToken: str = None,
        MaxResults: int = None,
        Filters: List[Any] = None,
        SortCriteria: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def search_profiles(
        self,
        NextToken: str = None,
        MaxResults: int = None,
        Filters: List[Any] = None,
        SortCriteria: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def search_rooms(
        self,
        NextToken: str = None,
        MaxResults: int = None,
        Filters: List[Any] = None,
        SortCriteria: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def search_skill_groups(
        self,
        NextToken: str = None,
        MaxResults: int = None,
        Filters: List[Any] = None,
        SortCriteria: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def search_users(
        self,
        NextToken: str = None,
        MaxResults: int = None,
        Filters: List[Any] = None,
        SortCriteria: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def send_announcement(
        self,
        RoomFilters: List[Any],
        Content: Dict[str, Any],
        ClientRequestToken: str,
        TimeToLiveInSeconds: int = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def send_invitation(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def start_device_sync(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def start_smart_home_appliance_discovery(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def tag_resource(self, Arn: str, Tags: List[Any]) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def untag_resource(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_address_book(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_business_report_schedule(
        self,
        ScheduleArn: str,
        S3BucketName: str = None,
        S3KeyPrefix: str = None,
        Format: str = None,
        ScheduleName: str = None,
        Recurrence: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def update_conference_provider(
        self,
        ConferenceProviderArn: str,
        ConferenceProviderType: str,
        MeetingSetting: Dict[str, Any],
        IPDialIn: Dict[str, Any] = None,
        PSTNDialIn: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def update_contact(
        self,
        ContactArn: str,
        DisplayName: str = None,
        FirstName: str = None,
        LastName: str = None,
        PhoneNumber: str = None,
        PhoneNumbers: List[Any] = None,
        SipAddresses: List[Any] = None,
    ) -> Dict[str, Any]:
        pass

    # pylint: disable=arguments-differ
    def update_device(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_gateway(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_gateway_group(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_network_profile(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_profile(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_room(self) -> None:
        pass

    # pylint: disable=arguments-differ
    def update_skill_group(self) -> None:
        pass
