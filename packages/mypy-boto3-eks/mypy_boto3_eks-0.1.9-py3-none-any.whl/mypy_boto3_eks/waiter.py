"Main interface for eks Waiters"
from __future__ import annotations

from typing import Any
from typing import Dict
from botocore.waiter import Waiter as Boto3Waiter


class ClusterActive(Boto3Waiter):
    def wait(
        self,
        name: str,
        WaiterConfig: Dict[str, Any] = None
    ) -> None:
        """
        Polls :py:meth:`EKS.Client.describe_cluster` every 30 seconds until a successful state is reached. An error is returned after 40 failed checks.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/eks-2017-11-01/DescribeCluster>`_

        **Request Syntax**
        ::

          waiter.wait(
              name='string',
              WaiterConfig={
                  'Delay': 123,
                  'MaxAttempts': 123
              }
          )
        :type name: string
        :param name: **[REQUIRED]**

          The name of the cluster to describe.

        :type WaiterConfig: dict
        :param WaiterConfig:

          A dictionary that provides parameters to control waiting behavior.

          - **Delay** *(integer) --*

            The amount of time in seconds to wait between attempts. Default: 30

          - **MaxAttempts** *(integer) --*

            The maximum number of attempts to be made. Default: 40

        :returns: None
        """
        pass


class ClusterDeleted(Boto3Waiter):
    def wait(
        self,
        name: str,
        WaiterConfig: Dict[str, Any] = None
    ) -> None:
        """
        Polls :py:meth:`EKS.Client.describe_cluster` every 30 seconds until a successful state is reached. An error is returned after 40 failed checks.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/eks-2017-11-01/DescribeCluster>`_

        **Request Syntax**
        ::

          waiter.wait(
              name='string',
              WaiterConfig={
                  'Delay': 123,
                  'MaxAttempts': 123
              }
          )
        :type name: string
        :param name: **[REQUIRED]**

          The name of the cluster to describe.

        :type WaiterConfig: dict
        :param WaiterConfig:

          A dictionary that provides parameters to control waiting behavior.

          - **Delay** *(integer) --*

            The amount of time in seconds to wait between attempts. Default: 30

          - **MaxAttempts** *(integer) --*

            The maximum number of attempts to be made. Default: 40

        :returns: None
        """
        pass
