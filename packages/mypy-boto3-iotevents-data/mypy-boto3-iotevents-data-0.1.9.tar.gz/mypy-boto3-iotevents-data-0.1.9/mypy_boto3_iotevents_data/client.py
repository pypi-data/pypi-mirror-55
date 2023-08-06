"Main interface for iotevents-data Client"
from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List
from botocore.client import BaseClient
from botocore.paginate import Paginator
from botocore.waiter import Waiter


class Client(BaseClient):
    def batch_put_message(
        self,
        messages: List[Any]
    ) -> Dict[str, Any]:
        """
        Sends a set of messages to the AWS IoT Events system. Each message payload is transformed into the input you specify (``"inputName"`` ) and ingested into any detectors that monitor that input. If multiple messages are sent, the order in which the messages are processed isn't guaranteed. To guarantee ordering, you must send messages one at a time and wait for a successful response.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iotevents-data-2018-10-23/BatchPutMessage>`_

        **Request Syntax**
        ::

          response = client.batch_put_message(
              messages=[
                  {
                      'messageId': 'string',
                      'inputName': 'string',
                      'payload': b'bytes'
                  },
              ]
          )
        :type messages: list
        :param messages: **[REQUIRED]**

          The list of messages to send. Each message has the following format: ``'{ "messageId": "string", "inputName": "string", "payload": "string"}'``

          - *(dict) --*

            Information about a message.

            - **messageId** *(string) --* **[REQUIRED]**

              The ID to assign to the message. Within each batch sent, each ``"messageId"`` must be unique.

            - **inputName** *(string) --* **[REQUIRED]**

              The name of the input into which the message payload is transformed.

            - **payload** *(bytes) --* **[REQUIRED]**

              The payload of the message. This can be a JSON string or a Base-64-encoded string representing binary data (in which case you must decode it).

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'BatchPutMessageErrorEntries': [
                    {
                        'messageId': 'string',
                        'errorCode': 'ResourceNotFoundException'|'InvalidRequestException'|'InternalFailureException'|'ServiceUnavailableException'|'ThrottlingException',
                        'errorMessage': 'string'
                    },
                ]
            }
          **Response Structure**

          - *(dict) --*

            - **BatchPutMessageErrorEntries** *(list) --*

              A list of any errors encountered when sending the messages.

              - *(dict) --*

                Contains information about the errors encountered.

                - **messageId** *(string) --*

                  The ID of the message that caused the error. (See the value corresponding to the ``"messageId"`` key in the ``"message"`` object.)

                - **errorCode** *(string) --*

                  The code associated with the error.

                - **errorMessage** *(string) --*

                  More information about the error.

        """
        pass

    def batch_update_detector(
        self,
        detectors: List[Any]
    ) -> Dict[str, Any]:
        """
        Updates the state, variable values, and timer settings of one or more detectors (instances) of a specified detector model.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iotevents-data-2018-10-23/BatchUpdateDetector>`_

        **Request Syntax**
        ::

          response = client.batch_update_detector(
              detectors=[
                  {
                      'messageId': 'string',
                      'detectorModelName': 'string',
                      'keyValue': 'string',
                      'state': {
                          'stateName': 'string',
                          'variables': [
                              {
                                  'name': 'string',
                                  'value': 'string'
                              },
                          ],
                          'timers': [
                              {
                                  'name': 'string',
                                  'seconds': 123
                              },
                          ]
                      }
                  },
              ]
          )
        :type detectors: list
        :param detectors: **[REQUIRED]**

          The list of detectors (instances) to update, along with the values to update.

          - *(dict) --*

            Information used to update the detector (instance).

            - **messageId** *(string) --* **[REQUIRED]**

              The ID to assign to the detector update ``"message"`` . Each ``"messageId"`` must be unique within each batch sent.

            - **detectorModelName** *(string) --* **[REQUIRED]**

              The name of the detector model that created the detectors (instances).

            - **keyValue** *(string) --*

              The value of the input key attribute (identifying the device or system) that caused the creation of this detector (instance).

            - **state** *(dict) --* **[REQUIRED]**

              The new state, variable values, and timer settings of the detector (instance).

              - **stateName** *(string) --* **[REQUIRED]**

                The name of the new state of the detector (instance).

              - **variables** *(list) --* **[REQUIRED]**

                The new values of the detector's variables. Any variable whose value isn't specified is cleared.

                - *(dict) --*

                  The new value of the variable.

                  - **name** *(string) --* **[REQUIRED]**

                    The name of the variable.

                  - **value** *(string) --* **[REQUIRED]**

                    The new value of the variable.

              - **timers** *(list) --* **[REQUIRED]**

                The new values of the detector's timers. Any timer whose value isn't specified is cleared, and its timeout event won't occur.

                - *(dict) --*

                  The new setting of a timer.

                  - **name** *(string) --* **[REQUIRED]**

                    The name of the timer.

                  - **seconds** *(integer) --* **[REQUIRED]**

                    The new setting of the timer (the number of seconds before the timer elapses).

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'batchUpdateDetectorErrorEntries': [
                    {
                        'messageId': 'string',
                        'errorCode': 'ResourceNotFoundException'|'InvalidRequestException'|'InternalFailureException'|'ServiceUnavailableException'|'ThrottlingException',
                        'errorMessage': 'string'
                    },
                ]
            }
          **Response Structure**

          - *(dict) --*

            - **batchUpdateDetectorErrorEntries** *(list) --*

              A list of those detector updates that resulted in errors. (If an error is listed here, the specific update did not occur.)

              - *(dict) --*

                Information about the error that occured when attempting to update a detector.

                - **messageId** *(string) --*

                  The ``"messageId"`` of the update request that caused the error. (The value of the ``"messageId"`` in the update request ``"Detector"`` object.)

                - **errorCode** *(string) --*

                  The code of the error.

                - **errorMessage** *(string) --*

                  A message describing the error.

        """
        pass

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

    def describe_detector(
        self,
        detectorModelName: str,
        keyValue: str = None
    ) -> Dict[str, Any]:
        """
        Returns information about the specified detector (instance).

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iotevents-data-2018-10-23/DescribeDetector>`_

        **Request Syntax**
        ::

          response = client.describe_detector(
              detectorModelName='string',
              keyValue='string'
          )
        :type detectorModelName: string
        :param detectorModelName: **[REQUIRED]**

          The name of the detector model whose detectors (instances) you want information about.

        :type keyValue: string
        :param keyValue:

          A filter used to limit results to detectors (instances) created because of the given key ID.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'detector': {
                    'detectorModelName': 'string',
                    'keyValue': 'string',
                    'detectorModelVersion': 'string',
                    'state': {
                        'stateName': 'string',
                        'variables': [
                            {
                                'name': 'string',
                                'value': 'string'
                            },
                        ],
                        'timers': [
                            {
                                'name': 'string',
                                'timestamp': datetime(2015, 1, 1)
                            },
                        ]
                    },
                    'creationTime': datetime(2015, 1, 1),
                    'lastUpdateTime': datetime(2015, 1, 1)
                }
            }
          **Response Structure**

          - *(dict) --*

            - **detector** *(dict) --*

              Information about the detector (instance).

              - **detectorModelName** *(string) --*

                The name of the detector model that created this detector (instance).

              - **keyValue** *(string) --*

                The value of the key (identifying the device or system) that caused the creation of this detector (instance).

              - **detectorModelVersion** *(string) --*

                The version of the detector model that created this detector (instance).

              - **state** *(dict) --*

                The current state of the detector (instance).

                - **stateName** *(string) --*

                  The name of the state.

                - **variables** *(list) --*

                  The current values of the detector's variables.

                  - *(dict) --*

                    The current state of the variable.

                    - **name** *(string) --*

                      The name of the variable.

                    - **value** *(string) --*

                      The current value of the variable.

                - **timers** *(list) --*

                  The current state of the detector's timers.

                  - *(dict) --*

                    The current state of a timer.

                    - **name** *(string) --*

                      The name of the timer.

                    - **timestamp** *(datetime) --*

                      The number of seconds which have elapsed on the timer.

              - **creationTime** *(datetime) --*

                The time the detector (instance) was created.

              - **lastUpdateTime** *(datetime) --*

                The time the detector (instance) was last updated.

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

    def list_detectors(
        self,
        detectorModelName: str,
        stateName: str = None,
        nextToken: str = None,
        maxResults: int = None
    ) -> Dict[str, Any]:
        """
        Lists detectors (the instances of a detector model).

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iotevents-data-2018-10-23/ListDetectors>`_

        **Request Syntax**
        ::

          response = client.list_detectors(
              detectorModelName='string',
              stateName='string',
              nextToken='string',
              maxResults=123
          )
        :type detectorModelName: string
        :param detectorModelName: **[REQUIRED]**

          The name of the detector model whose detectors (instances) are listed.

        :type stateName: string
        :param stateName:

          A filter that limits results to those detectors (instances) in the given state.

        :type nextToken: string
        :param nextToken:

          The token for the next set of results.

        :type maxResults: integer
        :param maxResults:

          The maximum number of results to return at one time.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'detectorSummaries': [
                    {
                        'detectorModelName': 'string',
                        'keyValue': 'string',
                        'detectorModelVersion': 'string',
                        'state': {
                            'stateName': 'string'
                        },
                        'creationTime': datetime(2015, 1, 1),
                        'lastUpdateTime': datetime(2015, 1, 1)
                    },
                ],
                'nextToken': 'string'
            }
          **Response Structure**

          - *(dict) --*

            - **detectorSummaries** *(list) --*

              A list of summary information about the detectors (instances).

              - *(dict) --*

                Information about the detector (instance).

                - **detectorModelName** *(string) --*

                  The name of the detector model that created this detector (instance).

                - **keyValue** *(string) --*

                  The value of the key (identifying the device or system) that caused the creation of this detector (instance).

                - **detectorModelVersion** *(string) --*

                  The version of the detector model that created this detector (instance).

                - **state** *(dict) --*

                  The current state of the detector (instance).

                  - **stateName** *(string) --*

                    The name of the state.

                - **creationTime** *(datetime) --*

                  The time the detector (instance) was created.

                - **lastUpdateTime** *(datetime) --*

                  The time the detector (instance) was last updated.

            - **nextToken** *(string) --*

              A token to retrieve the next set of results, or ``null`` if there are no additional results.

        """
        pass