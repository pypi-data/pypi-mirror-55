"Main interface for elb Waiters"
from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List
from botocore.waiter import Waiter as Boto3Waiter


class AnyInstanceInService(Boto3Waiter):
    def wait(
        self,
        LoadBalancerName: str,
        Instances: List[Any] = None,
        WaiterConfig: Dict[str, Any] = None
    ) -> None:
        """
        Polls :py:meth:`ElasticLoadBalancing.Client.describe_instance_health` every 15 seconds until a successful state is reached. An error is returned after 40 failed checks.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/elasticloadbalancing-2012-06-01/DescribeInstanceHealth>`_

        **Request Syntax**
        ::

          waiter.wait(
              LoadBalancerName='string',
              Instances=[
                  {
                      'InstanceId': 'string'
                  },
              ],
              WaiterConfig={
                  'Delay': 123,
                  'MaxAttempts': 123
              }
          )
        :type LoadBalancerName: string
        :param LoadBalancerName: **[REQUIRED]**

          The name of the load balancer.

        :type Instances: list
        :param Instances:

          The IDs of the instances.

          - *(dict) --*

            The ID of an EC2 instance.

            - **InstanceId** *(string) --*

              The instance ID.

        :type WaiterConfig: dict
        :param WaiterConfig:

          A dictionary that provides parameters to control waiting behavior.

          - **Delay** *(integer) --*

            The amount of time in seconds to wait between attempts. Default: 15

          - **MaxAttempts** *(integer) --*

            The maximum number of attempts to be made. Default: 40

        :returns: None
        """
        pass


class InstanceDeregistered(Boto3Waiter):
    def wait(
        self,
        LoadBalancerName: str,
        Instances: List[Any] = None,
        WaiterConfig: Dict[str, Any] = None
    ) -> None:
        """
        Polls :py:meth:`ElasticLoadBalancing.Client.describe_instance_health` every 15 seconds until a successful state is reached. An error is returned after 40 failed checks.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/elasticloadbalancing-2012-06-01/DescribeInstanceHealth>`_

        **Request Syntax**
        ::

          waiter.wait(
              LoadBalancerName='string',
              Instances=[
                  {
                      'InstanceId': 'string'
                  },
              ],
              WaiterConfig={
                  'Delay': 123,
                  'MaxAttempts': 123
              }
          )
        :type LoadBalancerName: string
        :param LoadBalancerName: **[REQUIRED]**

          The name of the load balancer.

        :type Instances: list
        :param Instances:

          The IDs of the instances.

          - *(dict) --*

            The ID of an EC2 instance.

            - **InstanceId** *(string) --*

              The instance ID.

        :type WaiterConfig: dict
        :param WaiterConfig:

          A dictionary that provides parameters to control waiting behavior.

          - **Delay** *(integer) --*

            The amount of time in seconds to wait between attempts. Default: 15

          - **MaxAttempts** *(integer) --*

            The maximum number of attempts to be made. Default: 40

        :returns: None
        """
        pass


class InstanceInService(Boto3Waiter):
    def wait(
        self,
        LoadBalancerName: str,
        Instances: List[Any] = None,
        WaiterConfig: Dict[str, Any] = None
    ) -> None:
        """
        Polls :py:meth:`ElasticLoadBalancing.Client.describe_instance_health` every 15 seconds until a successful state is reached. An error is returned after 40 failed checks.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/elasticloadbalancing-2012-06-01/DescribeInstanceHealth>`_

        **Request Syntax**
        ::

          waiter.wait(
              LoadBalancerName='string',
              Instances=[
                  {
                      'InstanceId': 'string'
                  },
              ],
              WaiterConfig={
                  'Delay': 123,
                  'MaxAttempts': 123
              }
          )
        :type LoadBalancerName: string
        :param LoadBalancerName: **[REQUIRED]**

          The name of the load balancer.

        :type Instances: list
        :param Instances:

          The IDs of the instances.

          - *(dict) --*

            The ID of an EC2 instance.

            - **InstanceId** *(string) --*

              The instance ID.

        :type WaiterConfig: dict
        :param WaiterConfig:

          A dictionary that provides parameters to control waiting behavior.

          - **Delay** *(integer) --*

            The amount of time in seconds to wait between attempts. Default: 15

          - **MaxAttempts** *(integer) --*

            The maximum number of attempts to be made. Default: 40

        :returns: None
        """
        pass
