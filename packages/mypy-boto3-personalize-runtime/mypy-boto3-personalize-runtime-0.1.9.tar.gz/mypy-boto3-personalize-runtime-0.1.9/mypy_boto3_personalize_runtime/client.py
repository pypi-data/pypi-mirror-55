"Main interface for personalize-runtime Client"
from __future__ import annotations

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

    def get_personalized_ranking(
        self,
        campaignArn: str,
        inputList: List[Any],
        userId: str
    ) -> Dict[str, Any]:
        """
        Re-ranks a list of recommended items for the given user. The first item in the list is deemed the most likely item to be of interest to the user.

        .. note::

          The solution backing the campaign must have been created using a recipe of type PERSONALIZED_RANKING.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/personalize-runtime-2018-05-22/GetPersonalizedRanking>`_

        **Request Syntax**
        ::

          response = client.get_personalized_ranking(
              campaignArn='string',
              inputList=[
                  'string',
              ],
              userId='string'
          )
        :type campaignArn: string
        :param campaignArn: **[REQUIRED]**

          The Amazon Resource Name (ARN) of the campaign to use for generating the personalized ranking.

        :type inputList: list
        :param inputList: **[REQUIRED]**

          A list of items (itemId's) to rank. If an item was not included in the training dataset, the item is appended to the end of the reranked list.

          - *(string) --*

        :type userId: string
        :param userId: **[REQUIRED]**

          The user for which you want the campaign to provide a personalized ranking.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'personalizedRanking': [
                    {
                        'itemId': 'string'
                    },
                ]
            }
          **Response Structure**

          - *(dict) --*

            - **personalizedRanking** *(list) --*

              A list of items in order of most likely interest to the user.

              - *(dict) --*

                An object that identifies an item.

                The and APIs return a list of ``PredictedItem`` s.

                - **itemId** *(string) --*

                  The recommended item ID.

        """
        pass

    def get_recommendations(
        self,
        campaignArn: str,
        itemId: str = None,
        userId: str = None,
        numResults: int = None
    ) -> Dict[str, Any]:
        """
        Returns a list of recommended items. The required input depends on the recipe type used to create the solution backing the campaign, as follows:

        * RELATED_ITEMS - ``itemId`` required, ``userId`` not used

        * USER_PERSONALIZATION - ``itemId`` optional, ``userId`` required

        .. note::

          Campaigns that are backed by a solution created using a recipe of type PERSONALIZED_RANKING use the API.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/personalize-runtime-2018-05-22/GetRecommendations>`_

        **Request Syntax**
        ::

          response = client.get_recommendations(
              campaignArn='string',
              itemId='string',
              userId='string',
              numResults=123
          )
        :type campaignArn: string
        :param campaignArn: **[REQUIRED]**

          The Amazon Resource Name (ARN) of the campaign to use for getting recommendations.

        :type itemId: string
        :param itemId:

          The item ID to provide recommendations for.

          Required for ``RELATED_ITEMS`` recipe type.

        :type userId: string
        :param userId:

          The user ID to provide recommendations for.

          Required for ``USER_PERSONALIZATION`` recipe type.

        :type numResults: integer
        :param numResults:

          The number of results to return. The default is 25. The maximum is 100.

        :rtype: dict
        :returns:

          **Response Syntax**

          ::

            {
                'itemList': [
                    {
                        'itemId': 'string'
                    },
                ]
            }
          **Response Structure**

          - *(dict) --*

            - **itemList** *(list) --*

              A list of recommendations.

              - *(dict) --*

                An object that identifies an item.

                The and APIs return a list of ``PredictedItem`` s.

                - **itemId** *(string) --*

                  The recommended item ID.

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