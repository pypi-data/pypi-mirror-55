"Main interface for dms Waiters"
from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List
from botocore.waiter import Waiter as Boto3Waiter


class EndpointDeleted(Boto3Waiter):
    def wait(
        self,
        Filters: List[Any] = None,
        MaxRecords: int = None,
        Marker: str = None,
        WaiterConfig: Dict[str, Any] = None
    ) -> None:
        """
        Polls :py:meth:`DatabaseMigrationService.Client.describe_endpoints` every 5 seconds until a successful state is reached. An error is returned after 60 failed checks.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/dms-2016-01-01/DescribeEndpoints>`_

        **Request Syntax**
        ::

          waiter.wait(
              Filters=[
                  {
                      'Name': 'string',
                      'Values': [
                          'string',
                      ]
                  },
              ],
              MaxRecords=123,
              Marker='string',
              WaiterConfig={
                  'Delay': 123,
                  'MaxAttempts': 123
              }
          )
        :type Filters: list
        :param Filters:

          Filters applied to the describe action.

          Valid filter names: endpoint-arn | endpoint-type | endpoint-id | engine-name

          - *(dict) --*

            - **Name** *(string) --* **[REQUIRED]**

              The name of the filter.

            - **Values** *(list) --* **[REQUIRED]**

              The filter value.

              - *(string) --*

        :type MaxRecords: integer
        :param MaxRecords:

          The maximum number of records to include in the response. If more records exist than the specified ``MaxRecords`` value, a pagination token called a marker is included in the response so that the remaining results can be retrieved.

          Default: 100

          Constraints: Minimum 20, maximum 100.

        :type Marker: string
        :param Marker:

          An optional pagination token provided by a previous request. If this parameter is specified, the response includes only records beyond the marker, up to the value specified by ``MaxRecords`` .

        :type WaiterConfig: dict
        :param WaiterConfig:

          A dictionary that provides parameters to control waiting behavior.

          - **Delay** *(integer) --*

            The amount of time in seconds to wait between attempts. Default: 5

          - **MaxAttempts** *(integer) --*

            The maximum number of attempts to be made. Default: 60

        :returns: None
        """
        pass


class ReplicationInstanceAvailable(Boto3Waiter):
    def wait(
        self,
        Filters: List[Any] = None,
        MaxRecords: int = None,
        Marker: str = None,
        WaiterConfig: Dict[str, Any] = None
    ) -> None:
        """
        Polls :py:meth:`DatabaseMigrationService.Client.describe_replication_instances` every 60 seconds until a successful state is reached. An error is returned after 60 failed checks.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/dms-2016-01-01/DescribeReplicationInstances>`_

        **Request Syntax**
        ::

          waiter.wait(
              Filters=[
                  {
                      'Name': 'string',
                      'Values': [
                          'string',
                      ]
                  },
              ],
              MaxRecords=123,
              Marker='string',
              WaiterConfig={
                  'Delay': 123,
                  'MaxAttempts': 123
              }
          )
        :type Filters: list
        :param Filters:

          Filters applied to the describe action.

          Valid filter names: replication-instance-arn | replication-instance-id | replication-instance-class | engine-version

          - *(dict) --*

            - **Name** *(string) --* **[REQUIRED]**

              The name of the filter.

            - **Values** *(list) --* **[REQUIRED]**

              The filter value.

              - *(string) --*

        :type MaxRecords: integer
        :param MaxRecords:

          The maximum number of records to include in the response. If more records exist than the specified ``MaxRecords`` value, a pagination token called a marker is included in the response so that the remaining results can be retrieved.

          Default: 100

          Constraints: Minimum 20, maximum 100.

        :type Marker: string
        :param Marker:

          An optional pagination token provided by a previous request. If this parameter is specified, the response includes only records beyond the marker, up to the value specified by ``MaxRecords`` .

        :type WaiterConfig: dict
        :param WaiterConfig:

          A dictionary that provides parameters to control waiting behavior.

          - **Delay** *(integer) --*

            The amount of time in seconds to wait between attempts. Default: 60

          - **MaxAttempts** *(integer) --*

            The maximum number of attempts to be made. Default: 60

        :returns: None
        """
        pass


class ReplicationInstanceDeleted(Boto3Waiter):
    def wait(
        self,
        Filters: List[Any] = None,
        MaxRecords: int = None,
        Marker: str = None,
        WaiterConfig: Dict[str, Any] = None
    ) -> None:
        """
        Polls :py:meth:`DatabaseMigrationService.Client.describe_replication_instances` every 15 seconds until a successful state is reached. An error is returned after 60 failed checks.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/dms-2016-01-01/DescribeReplicationInstances>`_

        **Request Syntax**
        ::

          waiter.wait(
              Filters=[
                  {
                      'Name': 'string',
                      'Values': [
                          'string',
                      ]
                  },
              ],
              MaxRecords=123,
              Marker='string',
              WaiterConfig={
                  'Delay': 123,
                  'MaxAttempts': 123
              }
          )
        :type Filters: list
        :param Filters:

          Filters applied to the describe action.

          Valid filter names: replication-instance-arn | replication-instance-id | replication-instance-class | engine-version

          - *(dict) --*

            - **Name** *(string) --* **[REQUIRED]**

              The name of the filter.

            - **Values** *(list) --* **[REQUIRED]**

              The filter value.

              - *(string) --*

        :type MaxRecords: integer
        :param MaxRecords:

          The maximum number of records to include in the response. If more records exist than the specified ``MaxRecords`` value, a pagination token called a marker is included in the response so that the remaining results can be retrieved.

          Default: 100

          Constraints: Minimum 20, maximum 100.

        :type Marker: string
        :param Marker:

          An optional pagination token provided by a previous request. If this parameter is specified, the response includes only records beyond the marker, up to the value specified by ``MaxRecords`` .

        :type WaiterConfig: dict
        :param WaiterConfig:

          A dictionary that provides parameters to control waiting behavior.

          - **Delay** *(integer) --*

            The amount of time in seconds to wait between attempts. Default: 15

          - **MaxAttempts** *(integer) --*

            The maximum number of attempts to be made. Default: 60

        :returns: None
        """
        pass


class ReplicationTaskDeleted(Boto3Waiter):
    def wait(
        self,
        Filters: List[Any] = None,
        MaxRecords: int = None,
        Marker: str = None,
        WithoutSettings: bool = None,
        WaiterConfig: Dict[str, Any] = None
    ) -> None:
        """
        Polls :py:meth:`DatabaseMigrationService.Client.describe_replication_tasks` every 15 seconds until a successful state is reached. An error is returned after 60 failed checks.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/dms-2016-01-01/DescribeReplicationTasks>`_

        **Request Syntax**
        ::

          waiter.wait(
              Filters=[
                  {
                      'Name': 'string',
                      'Values': [
                          'string',
                      ]
                  },
              ],
              MaxRecords=123,
              Marker='string',
              WithoutSettings=True|False,
              WaiterConfig={
                  'Delay': 123,
                  'MaxAttempts': 123
              }
          )
        :type Filters: list
        :param Filters:

          Filters applied to the describe action.

          Valid filter names: replication-task-arn | replication-task-id | migration-type | endpoint-arn | replication-instance-arn

          - *(dict) --*

            - **Name** *(string) --* **[REQUIRED]**

              The name of the filter.

            - **Values** *(list) --* **[REQUIRED]**

              The filter value.

              - *(string) --*

        :type MaxRecords: integer
        :param MaxRecords:

          The maximum number of records to include in the response. If more records exist than the specified ``MaxRecords`` value, a pagination token called a marker is included in the response so that the remaining results can be retrieved.

          Default: 100

          Constraints: Minimum 20, maximum 100.

        :type Marker: string
        :param Marker:

          An optional pagination token provided by a previous request. If this parameter is specified, the response includes only records beyond the marker, up to the value specified by ``MaxRecords`` .

        :type WithoutSettings: boolean
        :param WithoutSettings:

          An option to set to avoid returning information about settings. Use this to reduce overhead when setting information is too large. To use this option, choose ``true`` ; otherwise, choose ``false`` (the default).

        :type WaiterConfig: dict
        :param WaiterConfig:

          A dictionary that provides parameters to control waiting behavior.

          - **Delay** *(integer) --*

            The amount of time in seconds to wait between attempts. Default: 15

          - **MaxAttempts** *(integer) --*

            The maximum number of attempts to be made. Default: 60

        :returns: None
        """
        pass


class ReplicationTaskReady(Boto3Waiter):
    def wait(
        self,
        Filters: List[Any] = None,
        MaxRecords: int = None,
        Marker: str = None,
        WithoutSettings: bool = None,
        WaiterConfig: Dict[str, Any] = None
    ) -> None:
        """
        Polls :py:meth:`DatabaseMigrationService.Client.describe_replication_tasks` every 15 seconds until a successful state is reached. An error is returned after 60 failed checks.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/dms-2016-01-01/DescribeReplicationTasks>`_

        **Request Syntax**
        ::

          waiter.wait(
              Filters=[
                  {
                      'Name': 'string',
                      'Values': [
                          'string',
                      ]
                  },
              ],
              MaxRecords=123,
              Marker='string',
              WithoutSettings=True|False,
              WaiterConfig={
                  'Delay': 123,
                  'MaxAttempts': 123
              }
          )
        :type Filters: list
        :param Filters:

          Filters applied to the describe action.

          Valid filter names: replication-task-arn | replication-task-id | migration-type | endpoint-arn | replication-instance-arn

          - *(dict) --*

            - **Name** *(string) --* **[REQUIRED]**

              The name of the filter.

            - **Values** *(list) --* **[REQUIRED]**

              The filter value.

              - *(string) --*

        :type MaxRecords: integer
        :param MaxRecords:

          The maximum number of records to include in the response. If more records exist than the specified ``MaxRecords`` value, a pagination token called a marker is included in the response so that the remaining results can be retrieved.

          Default: 100

          Constraints: Minimum 20, maximum 100.

        :type Marker: string
        :param Marker:

          An optional pagination token provided by a previous request. If this parameter is specified, the response includes only records beyond the marker, up to the value specified by ``MaxRecords`` .

        :type WithoutSettings: boolean
        :param WithoutSettings:

          An option to set to avoid returning information about settings. Use this to reduce overhead when setting information is too large. To use this option, choose ``true`` ; otherwise, choose ``false`` (the default).

        :type WaiterConfig: dict
        :param WaiterConfig:

          A dictionary that provides parameters to control waiting behavior.

          - **Delay** *(integer) --*

            The amount of time in seconds to wait between attempts. Default: 15

          - **MaxAttempts** *(integer) --*

            The maximum number of attempts to be made. Default: 60

        :returns: None
        """
        pass


class ReplicationTaskRunning(Boto3Waiter):
    def wait(
        self,
        Filters: List[Any] = None,
        MaxRecords: int = None,
        Marker: str = None,
        WithoutSettings: bool = None,
        WaiterConfig: Dict[str, Any] = None
    ) -> None:
        """
        Polls :py:meth:`DatabaseMigrationService.Client.describe_replication_tasks` every 15 seconds until a successful state is reached. An error is returned after 60 failed checks.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/dms-2016-01-01/DescribeReplicationTasks>`_

        **Request Syntax**
        ::

          waiter.wait(
              Filters=[
                  {
                      'Name': 'string',
                      'Values': [
                          'string',
                      ]
                  },
              ],
              MaxRecords=123,
              Marker='string',
              WithoutSettings=True|False,
              WaiterConfig={
                  'Delay': 123,
                  'MaxAttempts': 123
              }
          )
        :type Filters: list
        :param Filters:

          Filters applied to the describe action.

          Valid filter names: replication-task-arn | replication-task-id | migration-type | endpoint-arn | replication-instance-arn

          - *(dict) --*

            - **Name** *(string) --* **[REQUIRED]**

              The name of the filter.

            - **Values** *(list) --* **[REQUIRED]**

              The filter value.

              - *(string) --*

        :type MaxRecords: integer
        :param MaxRecords:

          The maximum number of records to include in the response. If more records exist than the specified ``MaxRecords`` value, a pagination token called a marker is included in the response so that the remaining results can be retrieved.

          Default: 100

          Constraints: Minimum 20, maximum 100.

        :type Marker: string
        :param Marker:

          An optional pagination token provided by a previous request. If this parameter is specified, the response includes only records beyond the marker, up to the value specified by ``MaxRecords`` .

        :type WithoutSettings: boolean
        :param WithoutSettings:

          An option to set to avoid returning information about settings. Use this to reduce overhead when setting information is too large. To use this option, choose ``true`` ; otherwise, choose ``false`` (the default).

        :type WaiterConfig: dict
        :param WaiterConfig:

          A dictionary that provides parameters to control waiting behavior.

          - **Delay** *(integer) --*

            The amount of time in seconds to wait between attempts. Default: 15

          - **MaxAttempts** *(integer) --*

            The maximum number of attempts to be made. Default: 60

        :returns: None
        """
        pass


class ReplicationTaskStopped(Boto3Waiter):
    def wait(
        self,
        Filters: List[Any] = None,
        MaxRecords: int = None,
        Marker: str = None,
        WithoutSettings: bool = None,
        WaiterConfig: Dict[str, Any] = None
    ) -> None:
        """
        Polls :py:meth:`DatabaseMigrationService.Client.describe_replication_tasks` every 15 seconds until a successful state is reached. An error is returned after 60 failed checks.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/dms-2016-01-01/DescribeReplicationTasks>`_

        **Request Syntax**
        ::

          waiter.wait(
              Filters=[
                  {
                      'Name': 'string',
                      'Values': [
                          'string',
                      ]
                  },
              ],
              MaxRecords=123,
              Marker='string',
              WithoutSettings=True|False,
              WaiterConfig={
                  'Delay': 123,
                  'MaxAttempts': 123
              }
          )
        :type Filters: list
        :param Filters:

          Filters applied to the describe action.

          Valid filter names: replication-task-arn | replication-task-id | migration-type | endpoint-arn | replication-instance-arn

          - *(dict) --*

            - **Name** *(string) --* **[REQUIRED]**

              The name of the filter.

            - **Values** *(list) --* **[REQUIRED]**

              The filter value.

              - *(string) --*

        :type MaxRecords: integer
        :param MaxRecords:

          The maximum number of records to include in the response. If more records exist than the specified ``MaxRecords`` value, a pagination token called a marker is included in the response so that the remaining results can be retrieved.

          Default: 100

          Constraints: Minimum 20, maximum 100.

        :type Marker: string
        :param Marker:

          An optional pagination token provided by a previous request. If this parameter is specified, the response includes only records beyond the marker, up to the value specified by ``MaxRecords`` .

        :type WithoutSettings: boolean
        :param WithoutSettings:

          An option to set to avoid returning information about settings. Use this to reduce overhead when setting information is too large. To use this option, choose ``true`` ; otherwise, choose ``false`` (the default).

        :type WaiterConfig: dict
        :param WaiterConfig:

          A dictionary that provides parameters to control waiting behavior.

          - **Delay** *(integer) --*

            The amount of time in seconds to wait between attempts. Default: 15

          - **MaxAttempts** *(integer) --*

            The maximum number of attempts to be made. Default: 60

        :returns: None
        """
        pass


class TestConnectionSucceeds(Boto3Waiter):
    def wait(
        self,
        Filters: List[Any] = None,
        MaxRecords: int = None,
        Marker: str = None,
        WaiterConfig: Dict[str, Any] = None
    ) -> None:
        """
        Polls :py:meth:`DatabaseMigrationService.Client.describe_connections` every 5 seconds until a successful state is reached. An error is returned after 60 failed checks.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/dms-2016-01-01/DescribeConnections>`_

        **Request Syntax**
        ::

          waiter.wait(
              Filters=[
                  {
                      'Name': 'string',
                      'Values': [
                          'string',
                      ]
                  },
              ],
              MaxRecords=123,
              Marker='string',
              WaiterConfig={
                  'Delay': 123,
                  'MaxAttempts': 123
              }
          )
        :type Filters: list
        :param Filters:

          The filters applied to the connection.

          Valid filter names: endpoint-arn | replication-instance-arn

          - *(dict) --*

            - **Name** *(string) --* **[REQUIRED]**

              The name of the filter.

            - **Values** *(list) --* **[REQUIRED]**

              The filter value.

              - *(string) --*

        :type MaxRecords: integer
        :param MaxRecords:

          The maximum number of records to include in the response. If more records exist than the specified ``MaxRecords`` value, a pagination token called a marker is included in the response so that the remaining results can be retrieved.

          Default: 100

          Constraints: Minimum 20, maximum 100.

        :type Marker: string
        :param Marker:

          An optional pagination token provided by a previous request. If this parameter is specified, the response includes only records beyond the marker, up to the value specified by ``MaxRecords`` .

        :type WaiterConfig: dict
        :param WaiterConfig:

          A dictionary that provides parameters to control waiting behavior.

          - **Delay** *(integer) --*

            The amount of time in seconds to wait between attempts. Default: 5

          - **MaxAttempts** *(integer) --*

            The maximum number of attempts to be made. Default: 60

        :returns: None
        """
        pass
