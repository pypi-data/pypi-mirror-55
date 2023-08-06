"Main interface for cloudformation Waiters"
from __future__ import annotations

from typing import Any
from typing import Dict
from botocore.waiter import Waiter as Boto3Waiter


class ChangeSetCreateComplete(Boto3Waiter):
    def wait(
        self,
        ChangeSetName: str,
        StackName: str = None,
        NextToken: str = None,
        WaiterConfig: Dict[str, Any] = None,
    ) -> None:
        """
        Polls :py:meth:`CloudFormation.Client.describe_change_set` every 30 seconds until a successful state is reached. An error is returned after 120 failed checks.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/cloudformation-2010-05-15/DescribeChangeSet>`_

        **Request Syntax**
        ::

          waiter.wait(
              ChangeSetName='string',
              StackName='string',
              NextToken='string',
              WaiterConfig={
                  'Delay': 123,
                  'MaxAttempts': 123
              }
          )
        :type ChangeSetName: string
        :param ChangeSetName: **[REQUIRED]**

          The name or Amazon Resource Name (ARN) of the change set that you want to describe.

        :type StackName: string
        :param StackName:

          If you specified the name of a change set, specify the stack name or ID (ARN) of the change set you want to describe.

        :type NextToken: string
        :param NextToken:

          A string (provided by the  DescribeChangeSet response output) that identifies the next page of information that you want to retrieve.

        :type WaiterConfig: dict
        :param WaiterConfig:

          A dictionary that provides parameters to control waiting behavior.

          - **Delay** *(integer) --*

            The amount of time in seconds to wait between attempts. Default: 30

          - **MaxAttempts** *(integer) --*

            The maximum number of attempts to be made. Default: 120

        :returns: None
        """
        pass


class StackCreateComplete(Boto3Waiter):
    def wait(
        self,
        StackName: str = None,
        NextToken: str = None,
        WaiterConfig: Dict[str, Any] = None,
    ) -> None:
        """
        Polls :py:meth:`CloudFormation.Client.describe_stacks` every 30 seconds until a successful state is reached. An error is returned after 120 failed checks.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/cloudformation-2010-05-15/DescribeStacks>`_

        **Request Syntax**
        ::

          waiter.wait(
              StackName='string',
              NextToken='string',
              WaiterConfig={
                  'Delay': 123,
                  'MaxAttempts': 123
              }
          )
        :type StackName: string
        :param StackName:

          The name or the unique stack ID that is associated with the stack, which are not always interchangeable:

          * Running stacks: You can specify either the stack's name or its unique stack ID.

          * Deleted stacks: You must specify the unique stack ID.

          Default: There is no default value.

        :type NextToken: string
        :param NextToken:

          A string that identifies the next page of stacks that you want to retrieve.

        :type WaiterConfig: dict
        :param WaiterConfig:

          A dictionary that provides parameters to control waiting behavior.

          - **Delay** *(integer) --*

            The amount of time in seconds to wait between attempts. Default: 30

          - **MaxAttempts** *(integer) --*

            The maximum number of attempts to be made. Default: 120

        :returns: None
        """
        pass


class StackDeleteComplete(Boto3Waiter):
    def wait(
        self,
        StackName: str = None,
        NextToken: str = None,
        WaiterConfig: Dict[str, Any] = None,
    ) -> None:
        """
        Polls :py:meth:`CloudFormation.Client.describe_stacks` every 30 seconds until a successful state is reached. An error is returned after 120 failed checks.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/cloudformation-2010-05-15/DescribeStacks>`_

        **Request Syntax**
        ::

          waiter.wait(
              StackName='string',
              NextToken='string',
              WaiterConfig={
                  'Delay': 123,
                  'MaxAttempts': 123
              }
          )
        :type StackName: string
        :param StackName:

          The name or the unique stack ID that is associated with the stack, which are not always interchangeable:

          * Running stacks: You can specify either the stack's name or its unique stack ID.

          * Deleted stacks: You must specify the unique stack ID.

          Default: There is no default value.

        :type NextToken: string
        :param NextToken:

          A string that identifies the next page of stacks that you want to retrieve.

        :type WaiterConfig: dict
        :param WaiterConfig:

          A dictionary that provides parameters to control waiting behavior.

          - **Delay** *(integer) --*

            The amount of time in seconds to wait between attempts. Default: 30

          - **MaxAttempts** *(integer) --*

            The maximum number of attempts to be made. Default: 120

        :returns: None
        """
        pass


class StackExists(Boto3Waiter):
    def wait(
        self,
        StackName: str = None,
        NextToken: str = None,
        WaiterConfig: Dict[str, Any] = None,
    ) -> None:
        """
        Polls :py:meth:`CloudFormation.Client.describe_stacks` every 5 seconds until a successful state is reached. An error is returned after 20 failed checks.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/cloudformation-2010-05-15/DescribeStacks>`_

        **Request Syntax**
        ::

          waiter.wait(
              StackName='string',
              NextToken='string',
              WaiterConfig={
                  'Delay': 123,
                  'MaxAttempts': 123
              }
          )
        :type StackName: string
        :param StackName:

          The name or the unique stack ID that is associated with the stack, which are not always interchangeable:

          * Running stacks: You can specify either the stack's name or its unique stack ID.

          * Deleted stacks: You must specify the unique stack ID.

          Default: There is no default value.

        :type NextToken: string
        :param NextToken:

          A string that identifies the next page of stacks that you want to retrieve.

        :type WaiterConfig: dict
        :param WaiterConfig:

          A dictionary that provides parameters to control waiting behavior.

          - **Delay** *(integer) --*

            The amount of time in seconds to wait between attempts. Default: 5

          - **MaxAttempts** *(integer) --*

            The maximum number of attempts to be made. Default: 20

        :returns: None
        """
        pass


class StackUpdateComplete(Boto3Waiter):
    def wait(
        self,
        StackName: str = None,
        NextToken: str = None,
        WaiterConfig: Dict[str, Any] = None,
    ) -> None:
        """
        Polls :py:meth:`CloudFormation.Client.describe_stacks` every 30 seconds until a successful state is reached. An error is returned after 120 failed checks.

        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/cloudformation-2010-05-15/DescribeStacks>`_

        **Request Syntax**
        ::

          waiter.wait(
              StackName='string',
              NextToken='string',
              WaiterConfig={
                  'Delay': 123,
                  'MaxAttempts': 123
              }
          )
        :type StackName: string
        :param StackName:

          The name or the unique stack ID that is associated with the stack, which are not always interchangeable:

          * Running stacks: You can specify either the stack's name or its unique stack ID.

          * Deleted stacks: You must specify the unique stack ID.

          Default: There is no default value.

        :type NextToken: string
        :param NextToken:

          A string that identifies the next page of stacks that you want to retrieve.

        :type WaiterConfig: dict
        :param WaiterConfig:

          A dictionary that provides parameters to control waiting behavior.

          - **Delay** *(integer) --*

            The amount of time in seconds to wait between attempts. Default: 30

          - **MaxAttempts** *(integer) --*

            The maximum number of attempts to be made. Default: 120

        :returns: None
        """
        pass
