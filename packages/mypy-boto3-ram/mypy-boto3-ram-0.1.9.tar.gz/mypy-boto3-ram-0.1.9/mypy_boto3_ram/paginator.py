"Main interface for ram Paginators"
from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List
from botocore.paginate import Paginator as Boto3Paginator


class GetResourcePolicies(Boto3Paginator):
    def paginate(
        self,
        resourceArns: List[Any],
        principal: str = None,
        PaginationConfig: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Creates an iterator that will paginate through responses from :py:meth:`RAM.Client.get_resource_policies`.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/ram-2018-01-04/GetResourcePolicies>`_

        **Request Syntax**
        ::

          response_iterator = paginator.paginate(
              resourceArns=[
                  'string',
              ],
              principal='string',
              PaginationConfig={
                  'MaxItems': 123,
                  'PageSize': 123,
                  'StartingToken': 'string'
              }
          )
        :type resourceArns: list
        :param resourceArns: **[REQUIRED]**

          The Amazon Resource Names (ARN) of the resources.

          - *(string) --*

        :type principal: string
        :param principal:

          The principal.

        :type PaginationConfig: dict
        :param PaginationConfig:

          A dictionary that provides parameters to control pagination.

          - **MaxItems** *(integer) --*

            The total number of items to return. If the total number of items available is more than the value specified in max-items then a ``NextToken`` will be provided in the output that you can use to resume pagination.

          - **PageSize** *(integer) --*

            The size of each page.

          - **StartingToken** *(string) --*

            A token to specify where to start paginating. This is the ``NextToken`` from a previous response.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'policies': [
                    'string',
                ],
                'NextToken': 'string'
            }
          **Response Structure**

          - *(dict) --*

            - **policies** *(list) --*

              A key policy document, in JSON format.

              - *(string) --*

            - **NextToken** *(string) --*

              A token to resume pagination.

        """
        pass


class GetResourceShareAssociations(Boto3Paginator):
    def paginate(
        self,
        associationType: str,
        resourceShareArns: List[Any] = None,
        resourceArn: str = None,
        principal: str = None,
        associationStatus: str = None,
        PaginationConfig: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Creates an iterator that will paginate through responses from :py:meth:`RAM.Client.get_resource_share_associations`.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/ram-2018-01-04/GetResourceShareAssociations>`_

        **Request Syntax**
        ::

          response_iterator = paginator.paginate(
              associationType='PRINCIPAL'|'RESOURCE',
              resourceShareArns=[
                  'string',
              ],
              resourceArn='string',
              principal='string',
              associationStatus='ASSOCIATING'|'ASSOCIATED'|'FAILED'|'DISASSOCIATING'|'DISASSOCIATED',
              PaginationConfig={
                  'MaxItems': 123,
                  'PageSize': 123,
                  'StartingToken': 'string'
              }
          )
        :type associationType: string
        :param associationType: **[REQUIRED]**

          The association type.

        :type resourceShareArns: list
        :param resourceShareArns:

          The Amazon Resource Names (ARN) of the resource shares.

          - *(string) --*

        :type resourceArn: string
        :param resourceArn:

          The Amazon Resource Name (ARN) of the resource. You cannot specify this parameter if the association type is ``PRINCIPAL`` .

        :type principal: string
        :param principal:

          The principal. You cannot specify this parameter if the association type is ``RESOURCE`` .

        :type associationStatus: string
        :param associationStatus:

          The association status.

        :type PaginationConfig: dict
        :param PaginationConfig:

          A dictionary that provides parameters to control pagination.

          - **MaxItems** *(integer) --*

            The total number of items to return. If the total number of items available is more than the value specified in max-items then a ``NextToken`` will be provided in the output that you can use to resume pagination.

          - **PageSize** *(integer) --*

            The size of each page.

          - **StartingToken** *(string) --*

            A token to specify where to start paginating. This is the ``NextToken`` from a previous response.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'resourceShareAssociations': [
                    {
                        'resourceShareArn': 'string',
                        'resourceShareName': 'string',
                        'associatedEntity': 'string',
                        'associationType': 'PRINCIPAL'|'RESOURCE',
                        'status': 'ASSOCIATING'|'ASSOCIATED'|'FAILED'|'DISASSOCIATING'|'DISASSOCIATED',
                        'statusMessage': 'string',
                        'creationTime': datetime(2015, 1, 1),
                        'lastUpdatedTime': datetime(2015, 1, 1),
                        'external': True|False
                    },
                ],
                'NextToken': 'string'
            }
          **Response Structure**

          - *(dict) --*

            - **resourceShareAssociations** *(list) --*

              Information about the associations.

              - *(dict) --*

                Describes an association with a resource share.

                - **resourceShareArn** *(string) --*

                  The Amazon Resource Name (ARN) of the resource share.

                - **resourceShareName** *(string) --*

                  The name of the resource share.

                - **associatedEntity** *(string) --*

                  The associated entity. For resource associations, this is the ARN of the resource. For principal associations, this is the ID of an AWS account or the ARN of an OU or organization from AWS Organizations.

                - **associationType** *(string) --*

                  The association type.

                - **status** *(string) --*

                  The status of the association.

                - **statusMessage** *(string) --*

                  A message about the status of the association.

                - **creationTime** *(datetime) --*

                  The time when the association was created.

                - **lastUpdatedTime** *(datetime) --*

                  The time when the association was last updated.

                - **external** *(boolean) --*

                  Indicates whether the principal belongs to the same AWS organization as the AWS account that owns the resource share.

            - **NextToken** *(string) --*

              A token to resume pagination.

        """
        pass


class GetResourceShareInvitations(Boto3Paginator):
    def paginate(
        self,
        resourceShareInvitationArns: List[Any] = None,
        resourceShareArns: List[Any] = None,
        PaginationConfig: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Creates an iterator that will paginate through responses from :py:meth:`RAM.Client.get_resource_share_invitations`.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/ram-2018-01-04/GetResourceShareInvitations>`_

        **Request Syntax**
        ::

          response_iterator = paginator.paginate(
              resourceShareInvitationArns=[
                  'string',
              ],
              resourceShareArns=[
                  'string',
              ],
              PaginationConfig={
                  'MaxItems': 123,
                  'PageSize': 123,
                  'StartingToken': 'string'
              }
          )
        :type resourceShareInvitationArns: list
        :param resourceShareInvitationArns:

          The Amazon Resource Names (ARN) of the invitations.

          - *(string) --*

        :type resourceShareArns: list
        :param resourceShareArns:

          The Amazon Resource Names (ARN) of the resource shares.

          - *(string) --*

        :type PaginationConfig: dict
        :param PaginationConfig:

          A dictionary that provides parameters to control pagination.

          - **MaxItems** *(integer) --*

            The total number of items to return. If the total number of items available is more than the value specified in max-items then a ``NextToken`` will be provided in the output that you can use to resume pagination.

          - **PageSize** *(integer) --*

            The size of each page.

          - **StartingToken** *(string) --*

            A token to specify where to start paginating. This is the ``NextToken`` from a previous response.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'resourceShareInvitations': [
                    {
                        'resourceShareInvitationArn': 'string',
                        'resourceShareName': 'string',
                        'resourceShareArn': 'string',
                        'senderAccountId': 'string',
                        'receiverAccountId': 'string',
                        'invitationTimestamp': datetime(2015, 1, 1),
                        'status': 'PENDING'|'ACCEPTED'|'REJECTED'|'EXPIRED',
                        'resourceShareAssociations': [
                            {
                                'resourceShareArn': 'string',
                                'resourceShareName': 'string',
                                'associatedEntity': 'string',
                                'associationType': 'PRINCIPAL'|'RESOURCE',
                                'status': 'ASSOCIATING'|'ASSOCIATED'|'FAILED'|'DISASSOCIATING'|'DISASSOCIATED',
                                'statusMessage': 'string',
                                'creationTime': datetime(2015, 1, 1),
                                'lastUpdatedTime': datetime(2015, 1, 1),
                                'external': True|False
                            },
                        ]
                    },
                ],
                'NextToken': 'string'
            }
          **Response Structure**

          - *(dict) --*

            - **resourceShareInvitations** *(list) --*

              Information about the invitations.

              - *(dict) --*

                Describes an invitation to join a resource share.

                - **resourceShareInvitationArn** *(string) --*

                  The Amazon Resource Name (ARN) of the invitation.

                - **resourceShareName** *(string) --*

                  The name of the resource share.

                - **resourceShareArn** *(string) --*

                  The Amazon Resource Name (ARN) of the resource share.

                - **senderAccountId** *(string) --*

                  The ID of the AWS account that sent the invitation.

                - **receiverAccountId** *(string) --*

                  The ID of the AWS account that received the invitation.

                - **invitationTimestamp** *(datetime) --*

                  The date and time when the invitation was sent.

                - **status** *(string) --*

                  The status of the invitation.

                - **resourceShareAssociations** *(list) --*

                  To view the resources associated with a pending resource share invitation, use `ListPendingInvitationResources <https://docs.aws.amazon.com/ram/latest/APIReference/API_ListPendingInvitationResources.html>`__ .

                  - *(dict) --*

                    Describes an association with a resource share.

                    - **resourceShareArn** *(string) --*

                      The Amazon Resource Name (ARN) of the resource share.

                    - **resourceShareName** *(string) --*

                      The name of the resource share.

                    - **associatedEntity** *(string) --*

                      The associated entity. For resource associations, this is the ARN of the resource. For principal associations, this is the ID of an AWS account or the ARN of an OU or organization from AWS Organizations.

                    - **associationType** *(string) --*

                      The association type.

                    - **status** *(string) --*

                      The status of the association.

                    - **statusMessage** *(string) --*

                      A message about the status of the association.

                    - **creationTime** *(datetime) --*

                      The time when the association was created.

                    - **lastUpdatedTime** *(datetime) --*

                      The time when the association was last updated.

                    - **external** *(boolean) --*

                      Indicates whether the principal belongs to the same AWS organization as the AWS account that owns the resource share.

            - **NextToken** *(string) --*

              A token to resume pagination.

        """
        pass


class GetResourceShares(Boto3Paginator):
    def paginate(
        self,
        resourceOwner: str,
        resourceShareArns: List[Any] = None,
        resourceShareStatus: str = None,
        name: str = None,
        tagFilters: List[Any] = None,
        PaginationConfig: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Creates an iterator that will paginate through responses from :py:meth:`RAM.Client.get_resource_shares`.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/ram-2018-01-04/GetResourceShares>`_

        **Request Syntax**
        ::

          response_iterator = paginator.paginate(
              resourceShareArns=[
                  'string',
              ],
              resourceShareStatus='PENDING'|'ACTIVE'|'FAILED'|'DELETING'|'DELETED',
              resourceOwner='SELF'|'OTHER-ACCOUNTS',
              name='string',
              tagFilters=[
                  {
                      'tagKey': 'string',
                      'tagValues': [
                          'string',
                      ]
                  },
              ],
              PaginationConfig={
                  'MaxItems': 123,
                  'PageSize': 123,
                  'StartingToken': 'string'
              }
          )
        :type resourceShareArns: list
        :param resourceShareArns:

          The Amazon Resource Names (ARN) of the resource shares.

          - *(string) --*

        :type resourceShareStatus: string
        :param resourceShareStatus:

          The status of the resource share.

        :type resourceOwner: string
        :param resourceOwner: **[REQUIRED]**

          The type of owner.

        :type name: string
        :param name:

          The name of the resource share.

        :type tagFilters: list
        :param tagFilters:

          One or more tag filters.

          - *(dict) --*

            Used to filter information based on tags.

            - **tagKey** *(string) --*

              The tag key.

            - **tagValues** *(list) --*

              The tag values.

              - *(string) --*

        :type PaginationConfig: dict
        :param PaginationConfig:

          A dictionary that provides parameters to control pagination.

          - **MaxItems** *(integer) --*

            The total number of items to return. If the total number of items available is more than the value specified in max-items then a ``NextToken`` will be provided in the output that you can use to resume pagination.

          - **PageSize** *(integer) --*

            The size of each page.

          - **StartingToken** *(string) --*

            A token to specify where to start paginating. This is the ``NextToken`` from a previous response.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'resourceShares': [
                    {
                        'resourceShareArn': 'string',
                        'name': 'string',
                        'owningAccountId': 'string',
                        'allowExternalPrincipals': True|False,
                        'status': 'PENDING'|'ACTIVE'|'FAILED'|'DELETING'|'DELETED',
                        'statusMessage': 'string',
                        'tags': [
                            {
                                'key': 'string',
                                'value': 'string'
                            },
                        ],
                        'creationTime': datetime(2015, 1, 1),
                        'lastUpdatedTime': datetime(2015, 1, 1)
                    },
                ],
                'NextToken': 'string'
            }
          **Response Structure**

          - *(dict) --*

            - **resourceShares** *(list) --*

              Information about the resource shares.

              - *(dict) --*

                Describes a resource share.

                - **resourceShareArn** *(string) --*

                  The Amazon Resource Name (ARN) of the resource share.

                - **name** *(string) --*

                  The name of the resource share.

                - **owningAccountId** *(string) --*

                  The ID of the AWS account that owns the resource share.

                - **allowExternalPrincipals** *(boolean) --*

                  Indicates whether principals outside your AWS organization can be associated with a resource share.

                - **status** *(string) --*

                  The status of the resource share.

                - **statusMessage** *(string) --*

                  A message about the status of the resource share.

                - **tags** *(list) --*

                  The tags for the resource share.

                  - *(dict) --*

                    Information about a tag.

                    - **key** *(string) --*

                      The key of the tag.

                    - **value** *(string) --*

                      The value of the tag.

                - **creationTime** *(datetime) --*

                  The time when the resource share was created.

                - **lastUpdatedTime** *(datetime) --*

                  The time when the resource share was last updated.

            - **NextToken** *(string) --*

              A token to resume pagination.

        """
        pass


class ListPrincipals(Boto3Paginator):
    def paginate(
        self,
        resourceOwner: str,
        resourceArn: str = None,
        principals: List[Any] = None,
        resourceType: str = None,
        resourceShareArns: List[Any] = None,
        PaginationConfig: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Creates an iterator that will paginate through responses from :py:meth:`RAM.Client.list_principals`.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/ram-2018-01-04/ListPrincipals>`_

        **Request Syntax**
        ::

          response_iterator = paginator.paginate(
              resourceOwner='SELF'|'OTHER-ACCOUNTS',
              resourceArn='string',
              principals=[
                  'string',
              ],
              resourceType='string',
              resourceShareArns=[
                  'string',
              ],
              PaginationConfig={
                  'MaxItems': 123,
                  'PageSize': 123,
                  'StartingToken': 'string'
              }
          )
        :type resourceOwner: string
        :param resourceOwner: **[REQUIRED]**

          The type of owner.

        :type resourceArn: string
        :param resourceArn:

          The Amazon Resource Name (ARN) of the resource.

        :type principals: list
        :param principals:

          The principals.

          - *(string) --*

        :type resourceType: string
        :param resourceType:

          The resource type.

          Valid values: ``route53resolver:ResolverRule`` | ``ec2:TransitGateway`` | ``ec2:Subnet`` | ``license-manager:LicenseConfiguration``

        :type resourceShareArns: list
        :param resourceShareArns:

          The Amazon Resource Names (ARN) of the resource shares.

          - *(string) --*

        :type PaginationConfig: dict
        :param PaginationConfig:

          A dictionary that provides parameters to control pagination.

          - **MaxItems** *(integer) --*

            The total number of items to return. If the total number of items available is more than the value specified in max-items then a ``NextToken`` will be provided in the output that you can use to resume pagination.

          - **PageSize** *(integer) --*

            The size of each page.

          - **StartingToken** *(string) --*

            A token to specify where to start paginating. This is the ``NextToken`` from a previous response.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'principals': [
                    {
                        'id': 'string',
                        'resourceShareArn': 'string',
                        'creationTime': datetime(2015, 1, 1),
                        'lastUpdatedTime': datetime(2015, 1, 1),
                        'external': True|False
                    },
                ],
                'NextToken': 'string'
            }
          **Response Structure**

          - *(dict) --*

            - **principals** *(list) --*

              The principals.

              - *(dict) --*

                Describes a principal for use with AWS Resource Access Manager.

                - **id** *(string) --*

                  The ID of the principal.

                - **resourceShareArn** *(string) --*

                  The Amazon Resource Name (ARN) of the resource share.

                - **creationTime** *(datetime) --*

                  The time when the principal was associated with the resource share.

                - **lastUpdatedTime** *(datetime) --*

                  The time when the association was last updated.

                - **external** *(boolean) --*

                  Indicates whether the principal belongs to the same AWS organization as the AWS account that owns the resource share.

            - **NextToken** *(string) --*

              A token to resume pagination.

        """
        pass


class ListResources(Boto3Paginator):
    def paginate(
        self,
        resourceOwner: str,
        principal: str = None,
        resourceType: str = None,
        resourceArns: List[Any] = None,
        resourceShareArns: List[Any] = None,
        PaginationConfig: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Creates an iterator that will paginate through responses from :py:meth:`RAM.Client.list_resources`.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/ram-2018-01-04/ListResources>`_

        **Request Syntax**
        ::

          response_iterator = paginator.paginate(
              resourceOwner='SELF'|'OTHER-ACCOUNTS',
              principal='string',
              resourceType='string',
              resourceArns=[
                  'string',
              ],
              resourceShareArns=[
                  'string',
              ],
              PaginationConfig={
                  'MaxItems': 123,
                  'PageSize': 123,
                  'StartingToken': 'string'
              }
          )
        :type resourceOwner: string
        :param resourceOwner: **[REQUIRED]**

          The type of owner.

        :type principal: string
        :param principal:

          The principal.

        :type resourceType: string
        :param resourceType:

          The resource type.

          Valid values: ``route53resolver:ResolverRule`` | ``ec2:TransitGateway`` | ``ec2:Subnet`` | ``license-manager:LicenseConfiguration``

        :type resourceArns: list
        :param resourceArns:

          The Amazon Resource Names (ARN) of the resources.

          - *(string) --*

        :type resourceShareArns: list
        :param resourceShareArns:

          The Amazon Resource Names (ARN) of the resource shares.

          - *(string) --*

        :type PaginationConfig: dict
        :param PaginationConfig:

          A dictionary that provides parameters to control pagination.

          - **MaxItems** *(integer) --*

            The total number of items to return. If the total number of items available is more than the value specified in max-items then a ``NextToken`` will be provided in the output that you can use to resume pagination.

          - **PageSize** *(integer) --*

            The size of each page.

          - **StartingToken** *(string) --*

            A token to specify where to start paginating. This is the ``NextToken`` from a previous response.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'resources': [
                    {
                        'arn': 'string',
                        'type': 'string',
                        'resourceShareArn': 'string',
                        'status': 'AVAILABLE'|'ZONAL_RESOURCE_INACCESSIBLE'|'LIMIT_EXCEEDED'|'UNAVAILABLE'|'PENDING',
                        'statusMessage': 'string',
                        'creationTime': datetime(2015, 1, 1),
                        'lastUpdatedTime': datetime(2015, 1, 1)
                    },
                ],
                'NextToken': 'string'
            }
          **Response Structure**

          - *(dict) --*

            - **resources** *(list) --*

              Information about the resources.

              - *(dict) --*

                Describes a resource associated with a resource share.

                - **arn** *(string) --*

                  The Amazon Resource Name (ARN) of the resource.

                - **type** *(string) --*

                  The resource type.

                - **resourceShareArn** *(string) --*

                  The Amazon Resource Name (ARN) of the resource share.

                - **status** *(string) --*

                  The status of the resource.

                - **statusMessage** *(string) --*

                  A message about the status of the resource.

                - **creationTime** *(datetime) --*

                  The time when the resource was associated with the resource share.

                - **lastUpdatedTime** *(datetime) --*

                  The time when the association was last updated.

            - **NextToken** *(string) --*

              A token to resume pagination.

        """
        pass
