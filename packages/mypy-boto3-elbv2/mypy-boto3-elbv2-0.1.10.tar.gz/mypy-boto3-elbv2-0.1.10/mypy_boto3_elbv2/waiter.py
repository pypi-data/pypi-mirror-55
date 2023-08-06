"Main interface for elbv2 Waiters"
from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List
from botocore.waiter import Waiter as Boto3Waiter


class LoadBalancerAvailable(Boto3Waiter):
    def wait(
        self,
        LoadBalancerArns: List[Any] = None,
        Names: List[Any] = None,
        Marker: str = None,
        PageSize: int = None,
        WaiterConfig: Dict[str, Any] = None,
    ) -> None:
        """
        Polls :py:meth:`ElasticLoadBalancingv2.Client.describe_load_balancers` every 15 seconds until a successful state is reached. An error is returned after 40 failed checks.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/elasticloadbalancingv2-2015-12-01/DescribeLoadBalancers>`_

        **Request Syntax**
        ::

          waiter.wait(
              LoadBalancerArns=[
                  'string',
              ],
              Names=[
                  'string',
              ],
              Marker='string',
              PageSize=123,
              WaiterConfig={
                  'Delay': 123,
                  'MaxAttempts': 123
              }
          )
        :type LoadBalancerArns: list
        :param LoadBalancerArns:

          The Amazon Resource Names (ARN) of the load balancers. You can specify up to 20 load balancers in a single call.

          - *(string) --*

        :type Names: list
        :param Names:

          The names of the load balancers.

          - *(string) --*

        :type Marker: string
        :param Marker:

          The marker for the next set of results. (You received this marker from a previous call.)

        :type PageSize: integer
        :param PageSize:

          The maximum number of results to return with this call.

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


class LoadBalancerExists(Boto3Waiter):
    def wait(
        self,
        LoadBalancerArns: List[Any] = None,
        Names: List[Any] = None,
        Marker: str = None,
        PageSize: int = None,
        WaiterConfig: Dict[str, Any] = None,
    ) -> None:
        """
        Polls :py:meth:`ElasticLoadBalancingv2.Client.describe_load_balancers` every 15 seconds until a successful state is reached. An error is returned after 40 failed checks.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/elasticloadbalancingv2-2015-12-01/DescribeLoadBalancers>`_

        **Request Syntax**
        ::

          waiter.wait(
              LoadBalancerArns=[
                  'string',
              ],
              Names=[
                  'string',
              ],
              Marker='string',
              PageSize=123,
              WaiterConfig={
                  'Delay': 123,
                  'MaxAttempts': 123
              }
          )
        :type LoadBalancerArns: list
        :param LoadBalancerArns:

          The Amazon Resource Names (ARN) of the load balancers. You can specify up to 20 load balancers in a single call.

          - *(string) --*

        :type Names: list
        :param Names:

          The names of the load balancers.

          - *(string) --*

        :type Marker: string
        :param Marker:

          The marker for the next set of results. (You received this marker from a previous call.)

        :type PageSize: integer
        :param PageSize:

          The maximum number of results to return with this call.

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


class LoadBalancersDeleted(Boto3Waiter):
    def wait(
        self,
        LoadBalancerArns: List[Any] = None,
        Names: List[Any] = None,
        Marker: str = None,
        PageSize: int = None,
        WaiterConfig: Dict[str, Any] = None,
    ) -> None:
        """
        Polls :py:meth:`ElasticLoadBalancingv2.Client.describe_load_balancers` every 15 seconds until a successful state is reached. An error is returned after 40 failed checks.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/elasticloadbalancingv2-2015-12-01/DescribeLoadBalancers>`_

        **Request Syntax**
        ::

          waiter.wait(
              LoadBalancerArns=[
                  'string',
              ],
              Names=[
                  'string',
              ],
              Marker='string',
              PageSize=123,
              WaiterConfig={
                  'Delay': 123,
                  'MaxAttempts': 123
              }
          )
        :type LoadBalancerArns: list
        :param LoadBalancerArns:

          The Amazon Resource Names (ARN) of the load balancers. You can specify up to 20 load balancers in a single call.

          - *(string) --*

        :type Names: list
        :param Names:

          The names of the load balancers.

          - *(string) --*

        :type Marker: string
        :param Marker:

          The marker for the next set of results. (You received this marker from a previous call.)

        :type PageSize: integer
        :param PageSize:

          The maximum number of results to return with this call.

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


class TargetDeregistered(Boto3Waiter):
    def wait(
        self,
        TargetGroupArn: str,
        Targets: List[Any] = None,
        WaiterConfig: Dict[str, Any] = None,
    ) -> None:
        """
        Polls :py:meth:`ElasticLoadBalancingv2.Client.describe_target_health` every 15 seconds until a successful state is reached. An error is returned after 40 failed checks.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/elasticloadbalancingv2-2015-12-01/DescribeTargetHealth>`_

        **Request Syntax**
        ::

          waiter.wait(
              TargetGroupArn='string',
              Targets=[
                  {
                      'Id': 'string',
                      'Port': 123,
                      'AvailabilityZone': 'string'
                  },
              ],
              WaiterConfig={
                  'Delay': 123,
                  'MaxAttempts': 123
              }
          )
        :type TargetGroupArn: string
        :param TargetGroupArn: **[REQUIRED]**

          The Amazon Resource Name (ARN) of the target group.

        :type Targets: list
        :param Targets:

          The targets.

          - *(dict) --*

            Information about a target.

            - **Id** *(string) --* **[REQUIRED]**

              The ID of the target. If the target type of the target group is ``instance`` , specify an instance ID. If the target type is ``ip`` , specify an IP address. If the target type is ``lambda`` , specify the ARN of the Lambda function.

            - **Port** *(integer) --*

              The port on which the target is listening.

            - **AvailabilityZone** *(string) --*

              An Availability Zone or ``all`` . This determines whether the target receives traffic from the load balancer nodes in the specified Availability Zone or from all enabled Availability Zones for the load balancer.

              This parameter is not supported if the target type of the target group is ``instance`` .

              If the target type is ``ip`` and the IP address is in a subnet of the VPC for the target group, the Availability Zone is automatically detected and this parameter is optional. If the IP address is outside the VPC, this parameter is required.

              With an Application Load Balancer, if the target type is ``ip`` and the IP address is outside the VPC for the target group, the only supported value is ``all`` .

              If the target type is ``lambda`` , this parameter is optional and the only supported value is ``all`` .

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


class TargetInService(Boto3Waiter):
    def wait(
        self,
        TargetGroupArn: str,
        Targets: List[Any] = None,
        WaiterConfig: Dict[str, Any] = None,
    ) -> None:
        """
        Polls :py:meth:`ElasticLoadBalancingv2.Client.describe_target_health` every 15 seconds until a successful state is reached. An error is returned after 40 failed checks.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/elasticloadbalancingv2-2015-12-01/DescribeTargetHealth>`_

        **Request Syntax**
        ::

          waiter.wait(
              TargetGroupArn='string',
              Targets=[
                  {
                      'Id': 'string',
                      'Port': 123,
                      'AvailabilityZone': 'string'
                  },
              ],
              WaiterConfig={
                  'Delay': 123,
                  'MaxAttempts': 123
              }
          )
        :type TargetGroupArn: string
        :param TargetGroupArn: **[REQUIRED]**

          The Amazon Resource Name (ARN) of the target group.

        :type Targets: list
        :param Targets:

          The targets.

          - *(dict) --*

            Information about a target.

            - **Id** *(string) --* **[REQUIRED]**

              The ID of the target. If the target type of the target group is ``instance`` , specify an instance ID. If the target type is ``ip`` , specify an IP address. If the target type is ``lambda`` , specify the ARN of the Lambda function.

            - **Port** *(integer) --*

              The port on which the target is listening.

            - **AvailabilityZone** *(string) --*

              An Availability Zone or ``all`` . This determines whether the target receives traffic from the load balancer nodes in the specified Availability Zone or from all enabled Availability Zones for the load balancer.

              This parameter is not supported if the target type of the target group is ``instance`` .

              If the target type is ``ip`` and the IP address is in a subnet of the VPC for the target group, the Availability Zone is automatically detected and this parameter is optional. If the IP address is outside the VPC, this parameter is required.

              With an Application Load Balancer, if the target type is ``ip`` and the IP address is outside the VPC for the target group, the only supported value is ``all`` .

              If the target type is ``lambda`` , this parameter is optional and the only supported value is ``all`` .

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
