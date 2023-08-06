"Main interface for iot1click-devices Client"
from __future__ import annotations

from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from botocore.client import BaseClient
from botocore.paginate import Paginator
from botocore.waiter import Waiter


class Client(BaseClient):
    def can_paginate(
        self,
        operation_name: str = None
    ) -> None:
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

    def claim_devices_by_claim_code(
        self,
        ClaimCode: str
    ) -> Dict[str, Any]:
        """
        Adds device(s) to your account (i.e., claim one or more devices) if and only if you received a claim code with the device(s).

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/devices-2018-05-14/ClaimDevicesByClaimCode>`_

        **Request Syntax**
        ::

          response = client.claim_devices_by_claim_code(
              ClaimCode='string'
          )
        :type ClaimCode: string
        :param ClaimCode: **[REQUIRED]**

          The claim code, starting with "C-", as provided by the device manufacturer.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'ClaimCode': 'string',
                'Total': 123
            }
          **Response Structure**

          - *(dict) --*

            200 response

            - **ClaimCode** *(string) --*

              The claim code provided by the device manufacturer.

            - **Total** *(integer) --*

              The total number of devices associated with the claim code that has been processed in the claim request.

        """
        pass

    def describe_device(
        self,
        DeviceId: str
    ) -> Dict[str, Any]:
        """
        Given a device ID, returns a DescribeDeviceResponse object describing the details of the device.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/devices-2018-05-14/DescribeDevice>`_

        **Request Syntax**
        ::

          response = client.describe_device(
              DeviceId='string'
          )
        :type DeviceId: string
        :param DeviceId: **[REQUIRED]**

          The unique identifier of the device.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'DeviceDescription': {
                    'Arn': 'string',
                    'Attributes': {
                        'string': 'string'
                    },
                    'DeviceId': 'string',
                    'Enabled': True|False,
                    'RemainingLife': 123.0,
                    'Type': 'string',
                    'Tags': {
                        'string': 'string'
                    }
                }
            }
          **Response Structure**

          - *(dict) --*

            200 response

            - **DeviceDescription** *(dict) --*

              Device details.

              - **Arn** *(string) --*

                The ARN of the device.

              - **Attributes** *(dict) --*

                An array of zero or more elements of DeviceAttribute objects providing user specified device attributes.

                - *(string) --*

                  - *(string) --*

              - **DeviceId** *(string) --*

                The unique identifier of the device.

              - **Enabled** *(boolean) --*

                A Boolean value indicating whether or not the device is enabled.

              - **RemainingLife** *(float) --*

                A value between 0 and 1 inclusive, representing the fraction of life remaining for the device.

              - **Type** *(string) --*

                The type of the device, such as "button".

              - **Tags** *(dict) --*

                The tags currently associated with the AWS IoT 1-Click device.

                - *(string) --*

                  - *(string) --*

        """
        pass

    def finalize_device_claim(
        self,
        DeviceId: str,
        Tags: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Given a device ID, finalizes the claim request for the associated device.

        .. note::

          Claiming a device consists of initiating a claim, then publishing a device event, and finalizing the claim. For a device of type button, a device event can be published by simply clicking the device.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/devices-2018-05-14/FinalizeDeviceClaim>`_

        **Request Syntax**
        ::

          response = client.finalize_device_claim(
              DeviceId='string',
              Tags={
                  'string': 'string'
              }
          )
        :type DeviceId: string
        :param DeviceId: **[REQUIRED]**

          The unique identifier of the device.

        :type Tags: dict
        :param Tags:

          A collection of key/value pairs defining the resource tags. For example, { "tags": {"key1": "value1", "key2": "value2"} }. For more information, see `AWS Tagging Strategies <https://aws.amazon.com/answers/account-management/aws-tagging-strategies/>`__ .

          - *(string) --*

            - *(string) --*

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'State': 'string'
            }
          **Response Structure**

          - *(dict) --*

            200 response

            - **State** *(string) --*

              The device's final claim state.

        """
        pass

    def generate_presigned_url(
        self,
        ClientMethod: str = None,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = None,
        HttpMethod: str = None
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

    def get_device_methods(
        self,
        DeviceId: str
    ) -> Dict[str, Any]:
        """
        Given a device ID, returns the invokable methods associated with the device.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/devices-2018-05-14/GetDeviceMethods>`_

        **Request Syntax**
        ::

          response = client.get_device_methods(
              DeviceId='string'
          )
        :type DeviceId: string
        :param DeviceId: **[REQUIRED]**

          The unique identifier of the device.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'DeviceMethods': [
                    {
                        'DeviceType': 'string',
                        'MethodName': 'string'
                    },
                ]
            }
          **Response Structure**

          - *(dict) --*

            200 response

            - **DeviceMethods** *(list) --*

              List of available device APIs.

              - *(dict) --*

                - **DeviceType** *(string) --*

                  The type of the device, such as "button".

                - **MethodName** *(string) --*

                  The name of the method applicable to the deviceType.

        """
        pass

    def get_paginator(
        self,
        operation_name: str = None
    ) -> Paginator:
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

    def get_waiter(
        self,
        waiter_name: str = None
    ) -> Waiter:
        """
        Returns an object that can wait for some condition.

        :type waiter_name: str
        :param waiter_name: The name of the waiter to get. See the waiters
            section of the service docs for a list of available waiters.

        :returns: The specified waiter object.
        :rtype: botocore.waiter.Waiter
        """
        pass

    def initiate_device_claim(
        self,
        DeviceId: str
    ) -> Dict[str, Any]:
        """
        Given a device ID, initiates a claim request for the associated device.

        .. note::

          Claiming a device consists of initiating a claim, then publishing a device event, and finalizing the claim. For a device of type button, a device event can be published by simply clicking the device.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/devices-2018-05-14/InitiateDeviceClaim>`_

        **Request Syntax**
        ::

          response = client.initiate_device_claim(
              DeviceId='string'
          )
        :type DeviceId: string
        :param DeviceId: **[REQUIRED]**

          The unique identifier of the device.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'State': 'string'
            }
          **Response Structure**

          - *(dict) --*

            200 response

            - **State** *(string) --*

              The device's final claim state.

        """
        pass

    def invoke_device_method(
        self,
        DeviceId: str,
        DeviceMethod: Dict[str, Any] = None,
        DeviceMethodParameters: str = None
    ) -> Dict[str, Any]:
        """
        Given a device ID, issues a request to invoke a named device method (with possible parameters). See the "Example POST" code snippet below.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/devices-2018-05-14/InvokeDeviceMethod>`_

        **Request Syntax**
        ::

          response = client.invoke_device_method(
              DeviceId='string',
              DeviceMethod={
                  'DeviceType': 'string',
                  'MethodName': 'string'
              },
              DeviceMethodParameters='string'
          )
        :type DeviceId: string
        :param DeviceId: **[REQUIRED]**

          The unique identifier of the device.

        :type DeviceMethod: dict
        :param DeviceMethod:

          The device method to invoke.

          - **DeviceType** *(string) --*

            The type of the device, such as "button".

          - **MethodName** *(string) --*

            The name of the method applicable to the deviceType.

        :type DeviceMethodParameters: string
        :param DeviceMethodParameters:

          A JSON encoded string containing the device method request parameters.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'DeviceMethodResponse': 'string'
            }
          **Response Structure**

          - *(dict) --*

            200 response

            - **DeviceMethodResponse** *(string) --*

              A JSON encoded string containing the device method response.

        """
        pass

    def list_device_events(
        self,
        DeviceId: str,
        FromTimeStamp: datetime,
        ToTimeStamp: datetime,
        MaxResults: int = None,
        NextToken: str = None
    ) -> Dict[str, Any]:
        """
        Using a device ID, returns a DeviceEventsResponse object containing an array of events for the device.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/devices-2018-05-14/ListDeviceEvents>`_

        **Request Syntax**
        ::

          response = client.list_device_events(
              DeviceId='string',
              FromTimeStamp=datetime(2015, 1, 1),
              MaxResults=123,
              NextToken='string',
              ToTimeStamp=datetime(2015, 1, 1)
          )
        :type DeviceId: string
        :param DeviceId: **[REQUIRED]**

          The unique identifier of the device.

        :type FromTimeStamp: datetime
        :param FromTimeStamp: **[REQUIRED]**

          The start date for the device event query, in ISO8061 format. For example, 2018-03-28T15:45:12.880Z

        :type MaxResults: integer
        :param MaxResults:

          The maximum number of results to return per request. If not set, a default value of 100 is used.

        :type NextToken: string
        :param NextToken:

          The token to retrieve the next set of results.

        :type ToTimeStamp: datetime
        :param ToTimeStamp: **[REQUIRED]**

          The end date for the device event query, in ISO8061 format. For example, 2018-03-28T15:45:12.880Z

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'Events': [
                    {
                        'Device': {
                            'Attributes': {},
                            'DeviceId': 'string',
                            'Type': 'string'
                        },
                        'StdEvent': 'string'
                    },
                ],
                'NextToken': 'string'
            }
          **Response Structure**

          - *(dict) --*

            200 response

            - **Events** *(list) --*

              An array of zero or more elements describing the event(s) associated with the device.

              - *(dict) --*

                - **Device** *(dict) --*

                  An object representing the device associated with the event.

                  - **Attributes** *(dict) --*

                    The user specified attributes associated with the device for an event.

                  - **DeviceId** *(string) --*

                    The unique identifier of the device.

                  - **Type** *(string) --*

                    The device type, such as "button".

                - **StdEvent** *(string) --*

                  A serialized JSON object representing the device-type specific event.

            - **NextToken** *(string) --*

              The token to retrieve the next set of results.

        """
        pass

    def list_devices(
        self,
        DeviceType: str = None,
        MaxResults: int = None,
        NextToken: str = None
    ) -> Dict[str, Any]:
        """
        Lists the 1-Click compatible devices associated with your AWS account.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/devices-2018-05-14/ListDevices>`_

        **Request Syntax**
        ::

          response = client.list_devices(
              DeviceType='string',
              MaxResults=123,
              NextToken='string'
          )
        :type DeviceType: string
        :param DeviceType:

          The type of the device, such as "button".

        :type MaxResults: integer
        :param MaxResults:

          The maximum number of results to return per request. If not set, a default value of 100 is used.

        :type NextToken: string
        :param NextToken:

          The token to retrieve the next set of results.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'Devices': [
                    {
                        'Arn': 'string',
                        'Attributes': {
                            'string': 'string'
                        },
                        'DeviceId': 'string',
                        'Enabled': True|False,
                        'RemainingLife': 123.0,
                        'Type': 'string',
                        'Tags': {
                            'string': 'string'
                        }
                    },
                ],
                'NextToken': 'string'
            }
          **Response Structure**

          - *(dict) --*

            200 response

            - **Devices** *(list) --*

              A list of devices.

              - *(dict) --*

                - **Arn** *(string) --*

                  The ARN of the device.

                - **Attributes** *(dict) --*

                  An array of zero or more elements of DeviceAttribute objects providing user specified device attributes.

                  - *(string) --*

                    - *(string) --*

                - **DeviceId** *(string) --*

                  The unique identifier of the device.

                - **Enabled** *(boolean) --*

                  A Boolean value indicating whether or not the device is enabled.

                - **RemainingLife** *(float) --*

                  A value between 0 and 1 inclusive, representing the fraction of life remaining for the device.

                - **Type** *(string) --*

                  The type of the device, such as "button".

                - **Tags** *(dict) --*

                  The tags currently associated with the AWS IoT 1-Click device.

                  - *(string) --*

                    - *(string) --*

            - **NextToken** *(string) --*

              The token to retrieve the next set of results.

        """
        pass

    def list_tags_for_resource(
        self,
        ResourceArn: str
    ) -> Dict[str, Any]:
        """
        Lists the tags associated with the specified resource ARN.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/devices-2018-05-14/ListTagsForResource>`_

        **Request Syntax**
        ::

          response = client.list_tags_for_resource(
              ResourceArn='string'
          )
        :type ResourceArn: string
        :param ResourceArn: **[REQUIRED]**

          The ARN of the resource.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'Tags': {
                    'string': 'string'
                }
            }
          **Response Structure**

          - *(dict) --*

            - **Tags** *(dict) --*

              A collection of key/value pairs defining the resource tags. For example, { "tags": {"key1": "value1", "key2": "value2"} }. For more information, see `AWS Tagging Strategies <https://aws.amazon.com/answers/account-management/aws-tagging-strategies/>`__ .

              - *(string) --*

                - *(string) --*

        """
        pass

    def tag_resource(
        self,
        ResourceArn: str,
        Tags: Dict[str, Any]
    ) -> None:
        """
        Adds or updates the tags associated with the resource ARN. See `AWS IoT 1-Click Service Limits <https://docs.aws.amazon.com/iot-1-click/latest/developerguide/1click-appendix.html#1click-limits>`__ for the maximum number of tags allowed per resource.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/devices-2018-05-14/TagResource>`_

        **Request Syntax**
        ::

          response = client.tag_resource(
              ResourceArn='string',
              Tags={
                  'string': 'string'
              }
          )
        :type ResourceArn: string
        :param ResourceArn: **[REQUIRED]**

          The ARN of the resource.

        :type Tags: dict
        :param Tags: **[REQUIRED]**

          A collection of key/value pairs defining the resource tags. For example, { "tags": {"key1": "value1", "key2": "value2"} }. For more information, see `AWS Tagging Strategies <https://aws.amazon.com/answers/account-management/aws-tagging-strategies/>`__ .

          - *(string) --*

            - *(string) --*

        :returns: None
        """
        pass

    def unclaim_device(
        self,
        DeviceId: str
    ) -> Dict[str, Any]:
        """
        Disassociates a device from your AWS account using its device ID.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/devices-2018-05-14/UnclaimDevice>`_

        **Request Syntax**
        ::

          response = client.unclaim_device(
              DeviceId='string'
          )
        :type DeviceId: string
        :param DeviceId: **[REQUIRED]**

          The unique identifier of the device.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'State': 'string'
            }
          **Response Structure**

          - *(dict) --*

            200 response

            - **State** *(string) --*

              The device's final claim state.

        """
        pass

    def untag_resource(
        self,
        ResourceArn: str,
        TagKeys: List[Any]
    ) -> None:
        """
        Using tag keys, deletes the tags (key/value pairs) associated with the specified resource ARN.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/devices-2018-05-14/UntagResource>`_

        **Request Syntax**
        ::

          response = client.untag_resource(
              ResourceArn='string',
              TagKeys=[
                  'string',
              ]
          )
        :type ResourceArn: string
        :param ResourceArn: **[REQUIRED]**

          The ARN of the resource.

        :type TagKeys: list
        :param TagKeys: **[REQUIRED]**

          A collections of tag keys. For example, {"key1","key2"}

          - *(string) --*

        :returns: None
        """
        pass

    def update_device_state(
        self,
        DeviceId: str,
        Enabled: bool = None
    ) -> Dict[str, Any]:
        """
        Using a Boolean value (true or false), this operation enables or disables the device given a device ID.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/devices-2018-05-14/UpdateDeviceState>`_

        **Request Syntax**
        ::

          response = client.update_device_state(
              DeviceId='string',
              Enabled=True|False
          )
        :type DeviceId: string
        :param DeviceId: **[REQUIRED]**

          The unique identifier of the device.

        :type Enabled: boolean
        :param Enabled:

          If true, the device is enabled. If false, the device is disabled.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {}
          **Response Structure**

          - *(dict) --*

            200 response

        """
        pass