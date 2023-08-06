"Main interface for dlm Client"
from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List
from botocore.client import BaseClient
from botocore.paginate import Paginator
from botocore.waiter import Waiter


class Client(BaseClient):
    def can_paginate(self, operation_name: str = None) -> None:
        """
        Check if an operation can be paginated.

        :type operation_name: string
        :param operation_name: The operation name.  This is the same name
            as the method name on the client.  For example, if the
            method name is ``create_foo``, and you'd normally invoke the
            operation as ``client.create_foo(**kwargs)``, if the
            ``create_foo`` operation can be paginated, you can use the
            call ``client.get_paginator("create_foo")``.

        :return: ``True`` if the operation can be paginated,
            ``False`` otherwise.
        """
        pass

    def create_lifecycle_policy(
        self,
        ExecutionRoleArn: str,
        Description: str,
        State: str,
        PolicyDetails: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Creates a policy to manage the lifecycle of the specified AWS resources. You can create up to 100 lifecycle policies.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/dlm-2018-01-12/CreateLifecyclePolicy>`_

        **Request Syntax**
        ::

          response = client.create_lifecycle_policy(
              ExecutionRoleArn='string',
              Description='string',
              State='ENABLED'|'DISABLED',
              PolicyDetails={
                  'PolicyType': 'EBS_SNAPSHOT_MANAGEMENT',
                  'ResourceTypes': [
                      'VOLUME'|'INSTANCE',
                  ],
                  'TargetTags': [
                      {
                          'Key': 'string',
                          'Value': 'string'
                      },
                  ],
                  'Schedules': [
                      {
                          'Name': 'string',
                          'CopyTags': True|False,
                          'TagsToAdd': [
                              {
                                  'Key': 'string',
                                  'Value': 'string'
                              },
                          ],
                          'VariableTags': [
                              {
                                  'Key': 'string',
                                  'Value': 'string'
                              },
                          ],
                          'CreateRule': {
                              'Interval': 123,
                              'IntervalUnit': 'HOURS',
                              'Times': [
                                  'string',
                              ]
                          },
                          'RetainRule': {
                              'Count': 123
                          }
                      },
                  ],
                  'Parameters': {
                      'ExcludeBootVolume': True|False
                  }
              }
          )
        :type ExecutionRoleArn: string
        :param ExecutionRoleArn: **[REQUIRED]**

          The Amazon Resource Name (ARN) of the IAM role used to run the operations specified by the lifecycle policy.

        :type Description: string
        :param Description: **[REQUIRED]**

          A description of the lifecycle policy. The characters ^[0-9A-Za-z _-]+$ are supported.

        :type State: string
        :param State: **[REQUIRED]**

          The desired activation state of the lifecycle policy after creation.

        :type PolicyDetails: dict
        :param PolicyDetails: **[REQUIRED]**

          The configuration details of the lifecycle policy.

          Target tags cannot be re-used across lifecycle policies.

          - **PolicyType** *(string) --*

            This field determines the valid target resource types and actions a policy can manage. This field defaults to EBS_SNAPSHOT_MANAGEMENT if not present.

          - **ResourceTypes** *(list) --*

            The resource type.

            - *(string) --*

          - **TargetTags** *(list) --*

            The single tag that identifies targeted resources for this policy.

            - *(dict) --*

              Specifies a tag for a resource.

              - **Key** *(string) --* **[REQUIRED]**

                The tag key.

              - **Value** *(string) --* **[REQUIRED]**

                The tag value.

          - **Schedules** *(list) --*

            The schedule of policy-defined actions.

            - *(dict) --*

              Specifies a schedule.

              - **Name** *(string) --*

                The name of the schedule.

              - **CopyTags** *(boolean) --*

                Copy all user-defined tags on a source volume to snapshots of the volume created by this policy.

              - **TagsToAdd** *(list) --*

                The tags to apply to policy-created resources. These user-defined tags are in addition to the AWS-added lifecycle tags.

                - *(dict) --*

                  Specifies a tag for a resource.

                  - **Key** *(string) --* **[REQUIRED]**

                    The tag key.

                  - **Value** *(string) --* **[REQUIRED]**

                    The tag value.

              - **VariableTags** *(list) --*

                A collection of key/value pairs with values determined dynamically when the policy is executed. Keys may be any valid Amazon EC2 tag key. Values must be in one of the two following formats: ``$(instance-id)`` or ``$(timestamp)`` . Variable tags are only valid for EBS Snapshot Management – Instance policies.

                - *(dict) --*

                  Specifies a tag for a resource.

                  - **Key** *(string) --* **[REQUIRED]**

                    The tag key.

                  - **Value** *(string) --* **[REQUIRED]**

                    The tag value.

              - **CreateRule** *(dict) --*

                The create rule.

                - **Interval** *(integer) --* **[REQUIRED]**

                  The interval between snapshots. The supported values are 2, 3, 4, 6, 8, 12, and 24.

                - **IntervalUnit** *(string) --* **[REQUIRED]**

                  The interval unit.

                - **Times** *(list) --*

                  The time, in UTC, to start the operation. The supported format is hh:mm.

                  The operation occurs within a one-hour window following the specified time.

                  - *(string) --*

              - **RetainRule** *(dict) --*

                The retain rule.

                - **Count** *(integer) --* **[REQUIRED]**

                  The number of snapshots to keep for each volume, up to a maximum of 1000.

          - **Parameters** *(dict) --*

            A set of optional parameters that can be provided by the policy.

            - **ExcludeBootVolume** *(boolean) --*

              When executing an EBS Snapshot Management – Instance policy, execute all CreateSnapshots calls with the ``excludeBootVolume`` set to the supplied field. Defaults to false. Only valid for EBS Snapshot Management – Instance policies.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'PolicyId': 'string'
            }
          **Response Structure**

          - *(dict) --*

            - **PolicyId** *(string) --*

              The identifier of the lifecycle policy.

        """
        pass

    def delete_lifecycle_policy(self, PolicyId: str) -> Dict[str, Any]:
        """
        Deletes the specified lifecycle policy and halts the automated operations that the policy specified.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/dlm-2018-01-12/DeleteLifecyclePolicy>`_

        **Request Syntax**
        ::

          response = client.delete_lifecycle_policy(
              PolicyId='string'
          )
        :type PolicyId: string
        :param PolicyId: **[REQUIRED]**

          The identifier of the lifecycle policy.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {}
          **Response Structure**

          - *(dict) --*
        """
        pass

    def generate_presigned_url(
        self,
        ClientMethod: str = None,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = None,
        HttpMethod: str = None,
    ) -> None:
        """
        Generate a presigned url given a client, its method, and arguments

        :type ClientMethod: string
        :param ClientMethod: The client method to presign for

        :type Params: dict
        :param Params: The parameters normally passed to
            ``ClientMethod``.

        :type ExpiresIn: int
        :param ExpiresIn: The number of seconds the presigned url is valid
            for. By default it expires in an hour (3600 seconds)

        :type HttpMethod: string
        :param HttpMethod: The http method to use on the generated url. By
            default, the http method is whatever is used in the method's model.

        :returns: The presigned url
        """
        pass

    def get_lifecycle_policies(
        self,
        PolicyIds: List[Any] = None,
        State: str = None,
        ResourceTypes: List[Any] = None,
        TargetTags: List[Any] = None,
        TagsToAdd: List[Any] = None,
    ) -> Dict[str, Any]:
        """
        Gets summary information about all or the specified data lifecycle policies.

        To get complete information about a policy, use  GetLifecyclePolicy .

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/dlm-2018-01-12/GetLifecyclePolicies>`_

        **Request Syntax**
        ::

          response = client.get_lifecycle_policies(
              PolicyIds=[
                  'string',
              ],
              State='ENABLED'|'DISABLED'|'ERROR',
              ResourceTypes=[
                  'VOLUME'|'INSTANCE',
              ],
              TargetTags=[
                  'string',
              ],
              TagsToAdd=[
                  'string',
              ]
          )
        :type PolicyIds: list
        :param PolicyIds:

          The identifiers of the data lifecycle policies.

          - *(string) --*

        :type State: string
        :param State:

          The activation state.

        :type ResourceTypes: list
        :param ResourceTypes:

          The resource type.

          - *(string) --*

        :type TargetTags: list
        :param TargetTags:

          The target tag for a policy.

          Tags are strings in the format ``key=value`` .

          - *(string) --*

        :type TagsToAdd: list
        :param TagsToAdd:

          The tags to add to objects created by the policy.

          Tags are strings in the format ``key=value`` .

          These user-defined tags are added in addition to the AWS-added lifecycle tags.

          - *(string) --*

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'Policies': [
                    {
                        'PolicyId': 'string',
                        'Description': 'string',
                        'State': 'ENABLED'|'DISABLED'|'ERROR'
                    },
                ]
            }
          **Response Structure**

          - *(dict) --*

            - **Policies** *(list) --*

              Summary information about the lifecycle policies.

              - *(dict) --*

                Summary information about a lifecycle policy.

                - **PolicyId** *(string) --*

                  The identifier of the lifecycle policy.

                - **Description** *(string) --*

                  The description of the lifecycle policy.

                - **State** *(string) --*

                  The activation state of the lifecycle policy.

        """
        pass

    def get_lifecycle_policy(self, PolicyId: str) -> Dict[str, Any]:
        """
        Gets detailed information about the specified lifecycle policy.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/dlm-2018-01-12/GetLifecyclePolicy>`_

        **Request Syntax**
        ::

          response = client.get_lifecycle_policy(
              PolicyId='string'
          )
        :type PolicyId: string
        :param PolicyId: **[REQUIRED]**

          The identifier of the lifecycle policy.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'Policy': {
                    'PolicyId': 'string',
                    'Description': 'string',
                    'State': 'ENABLED'|'DISABLED'|'ERROR',
                    'ExecutionRoleArn': 'string',
                    'DateCreated': datetime(2015, 1, 1),
                    'DateModified': datetime(2015, 1, 1),
                    'PolicyDetails': {
                        'PolicyType': 'EBS_SNAPSHOT_MANAGEMENT',
                        'ResourceTypes': [
                            'VOLUME'|'INSTANCE',
                        ],
                        'TargetTags': [
                            {
                                'Key': 'string',
                                'Value': 'string'
                            },
                        ],
                        'Schedules': [
                            {
                                'Name': 'string',
                                'CopyTags': True|False,
                                'TagsToAdd': [
                                    {
                                        'Key': 'string',
                                        'Value': 'string'
                                    },
                                ],
                                'VariableTags': [
                                    {
                                        'Key': 'string',
                                        'Value': 'string'
                                    },
                                ],
                                'CreateRule': {
                                    'Interval': 123,
                                    'IntervalUnit': 'HOURS',
                                    'Times': [
                                        'string',
                                    ]
                                },
                                'RetainRule': {
                                    'Count': 123
                                }
                            },
                        ],
                        'Parameters': {
                            'ExcludeBootVolume': True|False
                        }
                    }
                }
            }
          **Response Structure**

          - *(dict) --*

            - **Policy** *(dict) --*

              Detailed information about the lifecycle policy.

              - **PolicyId** *(string) --*

                The identifier of the lifecycle policy.

              - **Description** *(string) --*

                The description of the lifecycle policy.

              - **State** *(string) --*

                The activation state of the lifecycle policy.

              - **ExecutionRoleArn** *(string) --*

                The Amazon Resource Name (ARN) of the IAM role used to run the operations specified by the lifecycle policy.

              - **DateCreated** *(datetime) --*

                The local date and time when the lifecycle policy was created.

              - **DateModified** *(datetime) --*

                The local date and time when the lifecycle policy was last modified.

              - **PolicyDetails** *(dict) --*

                The configuration of the lifecycle policy

                - **PolicyType** *(string) --*

                  This field determines the valid target resource types and actions a policy can manage. This field defaults to EBS_SNAPSHOT_MANAGEMENT if not present.

                - **ResourceTypes** *(list) --*

                  The resource type.

                  - *(string) --*

                - **TargetTags** *(list) --*

                  The single tag that identifies targeted resources for this policy.

                  - *(dict) --*

                    Specifies a tag for a resource.

                    - **Key** *(string) --*

                      The tag key.

                    - **Value** *(string) --*

                      The tag value.

                - **Schedules** *(list) --*

                  The schedule of policy-defined actions.

                  - *(dict) --*

                    Specifies a schedule.

                    - **Name** *(string) --*

                      The name of the schedule.

                    - **CopyTags** *(boolean) --*

                      Copy all user-defined tags on a source volume to snapshots of the volume created by this policy.

                    - **TagsToAdd** *(list) --*

                      The tags to apply to policy-created resources. These user-defined tags are in addition to the AWS-added lifecycle tags.

                      - *(dict) --*

                        Specifies a tag for a resource.

                        - **Key** *(string) --*

                          The tag key.

                        - **Value** *(string) --*

                          The tag value.

                    - **VariableTags** *(list) --*

                      A collection of key/value pairs with values determined dynamically when the policy is executed. Keys may be any valid Amazon EC2 tag key. Values must be in one of the two following formats: ``$(instance-id)`` or ``$(timestamp)`` . Variable tags are only valid for EBS Snapshot Management – Instance policies.

                      - *(dict) --*

                        Specifies a tag for a resource.

                        - **Key** *(string) --*

                          The tag key.

                        - **Value** *(string) --*

                          The tag value.

                    - **CreateRule** *(dict) --*

                      The create rule.

                      - **Interval** *(integer) --*

                        The interval between snapshots. The supported values are 2, 3, 4, 6, 8, 12, and 24.

                      - **IntervalUnit** *(string) --*

                        The interval unit.

                      - **Times** *(list) --*

                        The time, in UTC, to start the operation. The supported format is hh:mm.

                        The operation occurs within a one-hour window following the specified time.

                        - *(string) --*

                    - **RetainRule** *(dict) --*

                      The retain rule.

                      - **Count** *(integer) --*

                        The number of snapshots to keep for each volume, up to a maximum of 1000.

                - **Parameters** *(dict) --*

                  A set of optional parameters that can be provided by the policy.

                  - **ExcludeBootVolume** *(boolean) --*

                    When executing an EBS Snapshot Management – Instance policy, execute all CreateSnapshots calls with the ``excludeBootVolume`` set to the supplied field. Defaults to false. Only valid for EBS Snapshot Management – Instance policies.

        """
        pass

    def get_paginator(self, operation_name: str = None) -> Paginator:
        """
        Create a paginator for an operation.

        :type operation_name: string
        :param operation_name: The operation name.  This is the same name
            as the method name on the client.  For example, if the
            method name is ``create_foo``, and you'd normally invoke the
            operation as ``client.create_foo(**kwargs)``, if the
            ``create_foo`` operation can be paginated, you can use the
            call ``client.get_paginator("create_foo")``.

        :raise OperationNotPageableError: Raised if the operation is not
            pageable.  You can use the ``client.can_paginate`` method to
            check if an operation is pageable.

        :rtype: L{botocore.paginate.Paginator}
        :return: A paginator object.
        """
        pass

    def get_waiter(self, waiter_name: str = None) -> Waiter:
        """
        Returns an object that can wait for some condition.

        :type waiter_name: str
        :param waiter_name: The name of the waiter to get. See the waiters
            section of the service docs for a list of available waiters.

        :returns: The specified waiter object.
        :rtype: botocore.waiter.Waiter
        """
        pass

    def update_lifecycle_policy(
        self,
        PolicyId: str,
        ExecutionRoleArn: str = None,
        State: str = None,
        Description: str = None,
        PolicyDetails: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """
        Updates the specified lifecycle policy.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/dlm-2018-01-12/UpdateLifecyclePolicy>`_

        **Request Syntax**
        ::

          response = client.update_lifecycle_policy(
              PolicyId='string',
              ExecutionRoleArn='string',
              State='ENABLED'|'DISABLED',
              Description='string',
              PolicyDetails={
                  'PolicyType': 'EBS_SNAPSHOT_MANAGEMENT',
                  'ResourceTypes': [
                      'VOLUME'|'INSTANCE',
                  ],
                  'TargetTags': [
                      {
                          'Key': 'string',
                          'Value': 'string'
                      },
                  ],
                  'Schedules': [
                      {
                          'Name': 'string',
                          'CopyTags': True|False,
                          'TagsToAdd': [
                              {
                                  'Key': 'string',
                                  'Value': 'string'
                              },
                          ],
                          'VariableTags': [
                              {
                                  'Key': 'string',
                                  'Value': 'string'
                              },
                          ],
                          'CreateRule': {
                              'Interval': 123,
                              'IntervalUnit': 'HOURS',
                              'Times': [
                                  'string',
                              ]
                          },
                          'RetainRule': {
                              'Count': 123
                          }
                      },
                  ],
                  'Parameters': {
                      'ExcludeBootVolume': True|False
                  }
              }
          )
        :type PolicyId: string
        :param PolicyId: **[REQUIRED]**

          The identifier of the lifecycle policy.

        :type ExecutionRoleArn: string
        :param ExecutionRoleArn:

          The Amazon Resource Name (ARN) of the IAM role used to run the operations specified by the lifecycle policy.

        :type State: string
        :param State:

          The desired activation state of the lifecycle policy after creation.

        :type Description: string
        :param Description:

          A description of the lifecycle policy.

        :type PolicyDetails: dict
        :param PolicyDetails:

          The configuration of the lifecycle policy.

          Target tags cannot be re-used across policies.

          - **PolicyType** *(string) --*

            This field determines the valid target resource types and actions a policy can manage. This field defaults to EBS_SNAPSHOT_MANAGEMENT if not present.

          - **ResourceTypes** *(list) --*

            The resource type.

            - *(string) --*

          - **TargetTags** *(list) --*

            The single tag that identifies targeted resources for this policy.

            - *(dict) --*

              Specifies a tag for a resource.

              - **Key** *(string) --* **[REQUIRED]**

                The tag key.

              - **Value** *(string) --* **[REQUIRED]**

                The tag value.

          - **Schedules** *(list) --*

            The schedule of policy-defined actions.

            - *(dict) --*

              Specifies a schedule.

              - **Name** *(string) --*

                The name of the schedule.

              - **CopyTags** *(boolean) --*

                Copy all user-defined tags on a source volume to snapshots of the volume created by this policy.

              - **TagsToAdd** *(list) --*

                The tags to apply to policy-created resources. These user-defined tags are in addition to the AWS-added lifecycle tags.

                - *(dict) --*

                  Specifies a tag for a resource.

                  - **Key** *(string) --* **[REQUIRED]**

                    The tag key.

                  - **Value** *(string) --* **[REQUIRED]**

                    The tag value.

              - **VariableTags** *(list) --*

                A collection of key/value pairs with values determined dynamically when the policy is executed. Keys may be any valid Amazon EC2 tag key. Values must be in one of the two following formats: ``$(instance-id)`` or ``$(timestamp)`` . Variable tags are only valid for EBS Snapshot Management – Instance policies.

                - *(dict) --*

                  Specifies a tag for a resource.

                  - **Key** *(string) --* **[REQUIRED]**

                    The tag key.

                  - **Value** *(string) --* **[REQUIRED]**

                    The tag value.

              - **CreateRule** *(dict) --*

                The create rule.

                - **Interval** *(integer) --* **[REQUIRED]**

                  The interval between snapshots. The supported values are 2, 3, 4, 6, 8, 12, and 24.

                - **IntervalUnit** *(string) --* **[REQUIRED]**

                  The interval unit.

                - **Times** *(list) --*

                  The time, in UTC, to start the operation. The supported format is hh:mm.

                  The operation occurs within a one-hour window following the specified time.

                  - *(string) --*

              - **RetainRule** *(dict) --*

                The retain rule.

                - **Count** *(integer) --* **[REQUIRED]**

                  The number of snapshots to keep for each volume, up to a maximum of 1000.

          - **Parameters** *(dict) --*

            A set of optional parameters that can be provided by the policy.

            - **ExcludeBootVolume** *(boolean) --*

              When executing an EBS Snapshot Management – Instance policy, execute all CreateSnapshots calls with the ``excludeBootVolume`` set to the supplied field. Defaults to false. Only valid for EBS Snapshot Management – Instance policies.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {}
          **Response Structure**

          - *(dict) --*
        """
        pass
