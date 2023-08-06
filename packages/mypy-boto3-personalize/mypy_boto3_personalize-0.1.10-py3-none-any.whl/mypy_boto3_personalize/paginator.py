"Main interface for personalize Paginators"
from __future__ import annotations

from typing import Any
from typing import Dict
from botocore.paginate import Paginator as Boto3Paginator


class ListCampaigns(Boto3Paginator):
    def paginate(
        self, solutionArn: str = None, PaginationConfig: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Creates an iterator that will paginate through responses from :py:meth:`Personalize.Client.list_campaigns`.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/personalize-2018-05-22/ListCampaigns>`_

        **Request Syntax**
        ::

          response_iterator = paginator.paginate(
              solutionArn='string',
              PaginationConfig={
                  'MaxItems': 123,
                  'PageSize': 123,
                  'StartingToken': 'string'
              }
          )
        :type solutionArn: string
        :param solutionArn:

          The Amazon Resource Name (ARN) of the solution to list the campaigns for. When a solution is not specified, all the campaigns associated with the account are listed.

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
                'campaigns': [
                    {
                        'name': 'string',
                        'campaignArn': 'string',
                        'status': 'string',
                        'creationDateTime': datetime(2015, 1, 1),
                        'lastUpdatedDateTime': datetime(2015, 1, 1),
                        'failureReason': 'string'
                    },
                ],
                'NextToken': 'string'
            }
          **Response Structure**

          - *(dict) --*

            - **campaigns** *(list) --*

              A list of the campaigns.

              - *(dict) --*

                Provides a summary of the properties of a campaign. For a complete listing, call the  DescribeCampaign API.

                - **name** *(string) --*

                  The name of the campaign.

                - **campaignArn** *(string) --*

                  The Amazon Resource Name (ARN) of the campaign.

                - **status** *(string) --*

                  The status of the campaign.

                  A campaign can be in one of the following states:

                  * CREATE PENDING > CREATE IN_PROGRESS > ACTIVE -or- CREATE FAILED

                  * DELETE PENDING > DELETE IN_PROGRESS

                - **creationDateTime** *(datetime) --*

                  The date and time (in Unix time) that the campaign was created.

                - **lastUpdatedDateTime** *(datetime) --*

                  The date and time (in Unix time) that the campaign was last updated.

                - **failureReason** *(string) --*

                  If a campaign fails, the reason behind the failure.

            - **NextToken** *(string) --*

              A token to resume pagination.

        """
        pass


class ListDatasetGroups(Boto3Paginator):
    def paginate(self, PaginationConfig: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Creates an iterator that will paginate through responses from :py:meth:`Personalize.Client.list_dataset_groups`.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/personalize-2018-05-22/ListDatasetGroups>`_

        **Request Syntax**
        ::

          response_iterator = paginator.paginate(
              PaginationConfig={
                  'MaxItems': 123,
                  'PageSize': 123,
                  'StartingToken': 'string'
              }
          )
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
                'datasetGroups': [
                    {
                        'name': 'string',
                        'datasetGroupArn': 'string',
                        'status': 'string',
                        'creationDateTime': datetime(2015, 1, 1),
                        'lastUpdatedDateTime': datetime(2015, 1, 1),
                        'failureReason': 'string'
                    },
                ],
                'NextToken': 'string'
            }
          **Response Structure**

          - *(dict) --*

            - **datasetGroups** *(list) --*

              The list of your dataset groups.

              - *(dict) --*

                Provides a summary of the properties of a dataset group. For a complete listing, call the  DescribeDatasetGroup API.

                - **name** *(string) --*

                  The name of the dataset group.

                - **datasetGroupArn** *(string) --*

                  The Amazon Resource Name (ARN) of the dataset group.

                - **status** *(string) --*

                  The status of the dataset group.

                  A dataset group can be in one of the following states:

                  * CREATE PENDING > CREATE IN_PROGRESS > ACTIVE -or- CREATE FAILED

                  * DELETE PENDING

                - **creationDateTime** *(datetime) --*

                  The date and time (in Unix time) that the dataset group was created.

                - **lastUpdatedDateTime** *(datetime) --*

                  The date and time (in Unix time) that the dataset group was last updated.

                - **failureReason** *(string) --*

                  If creating a dataset group fails, the reason behind the failure.

            - **NextToken** *(string) --*

              A token to resume pagination.

        """
        pass


class ListDatasetImportJobs(Boto3Paginator):
    def paginate(
        self, datasetArn: str = None, PaginationConfig: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Creates an iterator that will paginate through responses from :py:meth:`Personalize.Client.list_dataset_import_jobs`.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/personalize-2018-05-22/ListDatasetImportJobs>`_

        **Request Syntax**
        ::

          response_iterator = paginator.paginate(
              datasetArn='string',
              PaginationConfig={
                  'MaxItems': 123,
                  'PageSize': 123,
                  'StartingToken': 'string'
              }
          )
        :type datasetArn: string
        :param datasetArn:

          The Amazon Resource Name (ARN) of the dataset to list the dataset import jobs for.

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
                'datasetImportJobs': [
                    {
                        'datasetImportJobArn': 'string',
                        'jobName': 'string',
                        'status': 'string',
                        'creationDateTime': datetime(2015, 1, 1),
                        'lastUpdatedDateTime': datetime(2015, 1, 1),
                        'failureReason': 'string'
                    },
                ],
                'NextToken': 'string'
            }
          **Response Structure**

          - *(dict) --*

            - **datasetImportJobs** *(list) --*

              The list of dataset import jobs.

              - *(dict) --*

                Provides a summary of the properties of a dataset import job. For a complete listing, call the  DescribeDatasetImportJob API.

                - **datasetImportJobArn** *(string) --*

                  The Amazon Resource Name (ARN) of the dataset import job.

                - **jobName** *(string) --*

                  The name of the dataset import job.

                - **status** *(string) --*

                  The status of the dataset import job.

                  A dataset import job can be in one of the following states:

                  * CREATE PENDING > CREATE IN_PROGRESS > ACTIVE -or- CREATE FAILED

                - **creationDateTime** *(datetime) --*

                  The date and time (in Unix time) that the dataset import job was created.

                - **lastUpdatedDateTime** *(datetime) --*

                  The date and time (in Unix time) that the dataset was last updated.

                - **failureReason** *(string) --*

                  If a dataset import job fails, the reason behind the failure.

            - **NextToken** *(string) --*

              A token to resume pagination.

        """
        pass


class ListDatasets(Boto3Paginator):
    def paginate(
        self, datasetGroupArn: str = None, PaginationConfig: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Creates an iterator that will paginate through responses from :py:meth:`Personalize.Client.list_datasets`.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/personalize-2018-05-22/ListDatasets>`_

        **Request Syntax**
        ::

          response_iterator = paginator.paginate(
              datasetGroupArn='string',
              PaginationConfig={
                  'MaxItems': 123,
                  'PageSize': 123,
                  'StartingToken': 'string'
              }
          )
        :type datasetGroupArn: string
        :param datasetGroupArn:

          The Amazon Resource Name (ARN) of the dataset group that contains the datasets to list.

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
                'datasets': [
                    {
                        'name': 'string',
                        'datasetArn': 'string',
                        'datasetType': 'string',
                        'status': 'string',
                        'creationDateTime': datetime(2015, 1, 1),
                        'lastUpdatedDateTime': datetime(2015, 1, 1)
                    },
                ],
                'NextToken': 'string'
            }
          **Response Structure**

          - *(dict) --*

            - **datasets** *(list) --*

              An array of ``Dataset`` objects. Each object provides metadata information.

              - *(dict) --*

                Provides a summary of the properties of a dataset. For a complete listing, call the  DescribeDataset API.

                - **name** *(string) --*

                  The name of the dataset.

                - **datasetArn** *(string) --*

                  The Amazon Resource Name (ARN) of the dataset.

                - **datasetType** *(string) --*

                  The dataset type. One of the following values:

                  * Interactions

                  * Items

                  * Users

                  * Event-Interactions

                - **status** *(string) --*

                  The status of the dataset.

                  A dataset can be in one of the following states:

                  * CREATE PENDING > CREATE IN_PROGRESS > ACTIVE -or- CREATE FAILED

                  * DELETE PENDING > DELETE IN_PROGRESS

                - **creationDateTime** *(datetime) --*

                  The date and time (in Unix time) that the dataset was created.

                - **lastUpdatedDateTime** *(datetime) --*

                  The date and time (in Unix time) that the dataset was last updated.

            - **NextToken** *(string) --*

              A token to resume pagination.

        """
        pass


class ListEventTrackers(Boto3Paginator):
    def paginate(
        self, datasetGroupArn: str = None, PaginationConfig: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Creates an iterator that will paginate through responses from :py:meth:`Personalize.Client.list_event_trackers`.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/personalize-2018-05-22/ListEventTrackers>`_

        **Request Syntax**
        ::

          response_iterator = paginator.paginate(
              datasetGroupArn='string',
              PaginationConfig={
                  'MaxItems': 123,
                  'PageSize': 123,
                  'StartingToken': 'string'
              }
          )
        :type datasetGroupArn: string
        :param datasetGroupArn:

          The ARN of a dataset group used to filter the response.

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
                'eventTrackers': [
                    {
                        'name': 'string',
                        'eventTrackerArn': 'string',
                        'status': 'string',
                        'creationDateTime': datetime(2015, 1, 1),
                        'lastUpdatedDateTime': datetime(2015, 1, 1)
                    },
                ],
                'NextToken': 'string'
            }
          **Response Structure**

          - *(dict) --*

            - **eventTrackers** *(list) --*

              A list of event trackers.

              - *(dict) --*

                Provides a summary of the properties of an event tracker. For a complete listing, call the  DescribeEventTracker API.

                - **name** *(string) --*

                  The name of the event tracker.

                - **eventTrackerArn** *(string) --*

                  The Amazon Resource Name (ARN) of the event tracker.

                - **status** *(string) --*

                  The status of the event tracker.

                  An event tracker can be in one of the following states:

                  * CREATE PENDING > CREATE IN_PROGRESS > ACTIVE -or- CREATE FAILED

                  * DELETE PENDING > DELETE IN_PROGRESS

                - **creationDateTime** *(datetime) --*

                  The date and time (in Unix time) that the event tracker was created.

                - **lastUpdatedDateTime** *(datetime) --*

                  The date and time (in Unix time) that the event tracker was last updated.

            - **NextToken** *(string) --*

              A token to resume pagination.

        """
        pass


class ListRecipes(Boto3Paginator):
    def paginate(
        self, recipeProvider: str = None, PaginationConfig: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Creates an iterator that will paginate through responses from :py:meth:`Personalize.Client.list_recipes`.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/personalize-2018-05-22/ListRecipes>`_

        **Request Syntax**
        ::

          response_iterator = paginator.paginate(
              recipeProvider='SERVICE',
              PaginationConfig={
                  'MaxItems': 123,
                  'PageSize': 123,
                  'StartingToken': 'string'
              }
          )
        :type recipeProvider: string
        :param recipeProvider:

          The default is ``SERVICE`` .

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
                'recipes': [
                    {
                        'name': 'string',
                        'recipeArn': 'string',
                        'status': 'string',
                        'creationDateTime': datetime(2015, 1, 1),
                        'lastUpdatedDateTime': datetime(2015, 1, 1)
                    },
                ],
                'NextToken': 'string'
            }
          **Response Structure**

          - *(dict) --*

            - **recipes** *(list) --*

              The list of available recipes.

              - *(dict) --*

                Provides a summary of the properties of a recipe. For a complete listing, call the  DescribeRecipe API.

                - **name** *(string) --*

                  The name of the recipe.

                - **recipeArn** *(string) --*

                  The Amazon Resource Name (ARN) of the recipe.

                - **status** *(string) --*

                  The status of the recipe.

                - **creationDateTime** *(datetime) --*

                  The date and time (in Unix time) that the recipe was created.

                - **lastUpdatedDateTime** *(datetime) --*

                  The date and time (in Unix time) that the recipe was last updated.

            - **NextToken** *(string) --*

              A token to resume pagination.

        """
        pass


class ListSchemas(Boto3Paginator):
    def paginate(self, PaginationConfig: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Creates an iterator that will paginate through responses from :py:meth:`Personalize.Client.list_schemas`.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/personalize-2018-05-22/ListSchemas>`_

        **Request Syntax**
        ::

          response_iterator = paginator.paginate(
              PaginationConfig={
                  'MaxItems': 123,
                  'PageSize': 123,
                  'StartingToken': 'string'
              }
          )
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
                'schemas': [
                    {
                        'name': 'string',
                        'schemaArn': 'string',
                        'creationDateTime': datetime(2015, 1, 1),
                        'lastUpdatedDateTime': datetime(2015, 1, 1)
                    },
                ],
                'NextToken': 'string'
            }
          **Response Structure**

          - *(dict) --*

            - **schemas** *(list) --*

              A list of schemas.

              - *(dict) --*

                Provides a summary of the properties of a dataset schema. For a complete listing, call the  DescribeSchema API.

                - **name** *(string) --*

                  The name of the schema.

                - **schemaArn** *(string) --*

                  The Amazon Resource Name (ARN) of the schema.

                - **creationDateTime** *(datetime) --*

                  The date and time (in Unix time) that the schema was created.

                - **lastUpdatedDateTime** *(datetime) --*

                  The date and time (in Unix time) that the schema was last updated.

            - **NextToken** *(string) --*

              A token to resume pagination.

        """
        pass


class ListSolutionVersions(Boto3Paginator):
    def paginate(
        self, solutionArn: str = None, PaginationConfig: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Creates an iterator that will paginate through responses from :py:meth:`Personalize.Client.list_solution_versions`.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/personalize-2018-05-22/ListSolutionVersions>`_

        **Request Syntax**
        ::

          response_iterator = paginator.paginate(
              solutionArn='string',
              PaginationConfig={
                  'MaxItems': 123,
                  'PageSize': 123,
                  'StartingToken': 'string'
              }
          )
        :type solutionArn: string
        :param solutionArn:

          The Amazon Resource Name (ARN) of the solution.

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
                'solutionVersions': [
                    {
                        'solutionVersionArn': 'string',
                        'status': 'string',
                        'creationDateTime': datetime(2015, 1, 1),
                        'lastUpdatedDateTime': datetime(2015, 1, 1),
                        'failureReason': 'string'
                    },
                ],
                'NextToken': 'string'
            }
          **Response Structure**

          - *(dict) --*

            - **solutionVersions** *(list) --*

              A list of solution versions describing the version properties.

              - *(dict) --*

                Provides a summary of the properties of a solution version. For a complete listing, call the  DescribeSolutionVersion API.

                - **solutionVersionArn** *(string) --*

                  The Amazon Resource Name (ARN) of the solution version.

                - **status** *(string) --*

                  The status of the solution version.

                  A solution version can be in one of the following states:

                  * CREATE PENDING > CREATE IN_PROGRESS > ACTIVE -or- CREATE FAILED

                - **creationDateTime** *(datetime) --*

                  The date and time (in Unix time) that this version of a solution was created.

                - **lastUpdatedDateTime** *(datetime) --*

                  The date and time (in Unix time) that the solution version was last updated.

                - **failureReason** *(string) --*

                  If a solution version fails, the reason behind the failure.

            - **NextToken** *(string) --*

              A token to resume pagination.

        """
        pass


class ListSolutions(Boto3Paginator):
    def paginate(
        self, datasetGroupArn: str = None, PaginationConfig: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Creates an iterator that will paginate through responses from :py:meth:`Personalize.Client.list_solutions`.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/personalize-2018-05-22/ListSolutions>`_

        **Request Syntax**
        ::

          response_iterator = paginator.paginate(
              datasetGroupArn='string',
              PaginationConfig={
                  'MaxItems': 123,
                  'PageSize': 123,
                  'StartingToken': 'string'
              }
          )
        :type datasetGroupArn: string
        :param datasetGroupArn:

          The Amazon Resource Name (ARN) of the dataset group.

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
                'solutions': [
                    {
                        'name': 'string',
                        'solutionArn': 'string',
                        'status': 'string',
                        'creationDateTime': datetime(2015, 1, 1),
                        'lastUpdatedDateTime': datetime(2015, 1, 1)
                    },
                ],
                'NextToken': 'string'
            }
          **Response Structure**

          - *(dict) --*

            - **solutions** *(list) --*

              A list of the current solutions.

              - *(dict) --*

                Provides a summary of the properties of a solution. For a complete listing, call the  DescribeSolution API.

                - **name** *(string) --*

                  The name of the solution.

                - **solutionArn** *(string) --*

                  The Amazon Resource Name (ARN) of the solution.

                - **status** *(string) --*

                  The status of the solution.

                  A solution can be in one of the following states:

                  * CREATE PENDING > CREATE IN_PROGRESS > ACTIVE -or- CREATE FAILED

                  * DELETE PENDING > DELETE IN_PROGRESS

                - **creationDateTime** *(datetime) --*

                  The date and time (in Unix time) that the solution was created.

                - **lastUpdatedDateTime** *(datetime) --*

                  The date and time (in Unix time) that the solution was last updated.

            - **NextToken** *(string) --*

              A token to resume pagination.

        """
        pass
