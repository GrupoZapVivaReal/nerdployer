import boto3
from botocore.exceptions import ClientError


class Cloudformation(object):

    def __init__(self, region='us-east-1'):
        self._client = boto3.client('cloudformation', region_name=region)

    def create_stack(self, stack, template, parameters, tags=[]):
        create_result = self._client.create_stack(StackName=stack, TemplateBody=template, Parameters=parameters, Tags=tags, Capabilities=['CAPABILITY_AUTO_EXPAND'], OnFailure='DELETE')
        self._wait_for(create_result['StackId'], 'stack_create_complete')
        return self.get_stack(create_result['StackId'])

    def update_stack(self, stack, template, parameters, tags=[]):
        try:
            update_result = self._client.update_stack(StackName=stack, TemplateBody=template, Parameters=parameters, Tags=tags, Capabilities=['CAPABILITY_AUTO_EXPAND'])
            self._wait_for(update_result['StackId'], 'stack_update_complete')
        except ClientError as e:
            if not (e.response['Error']['Code'] == 'ValidationError' and 'No updates are to be performed' in e.response['Error']['Message']):
                raise(e)
        return self.get_stack(stack)

    def get_stack(self, stack):
        try:
            describe_results = self._client.describe_stacks(StackName=stack)
            return describe_results['Stacks'][0]
        except ClientError as e:
            if not (e.response['Error']['Code'] == 'ValidationError' and 'does not exist' in e.response['Error']['Message']):
                raise(e)

    def list_stacks(self, tags=None):
        stack_list = []
        paginator = self._client.get_paginator('describe_stacks')
        for page in paginator.paginate():
            stack_list += [stack for stack in page['Stacks'] if not tags or all(tag in stack['Tags'] for tag in tags)]
        return stack_list

    def get_stack_resources(self, stack):
        return self._client.describe_stack_resources(StackName=stack, LogicalResourceId=resource)['StackResources']

    def get_stack_resource(self, stack, resource):
        return self._client.describe_stack_resources(StackName=stack, LogicalResourceId=resource)['StackResources'][0]

    def delete_stack(self, stack):
        self._client.delete_stack(StackName=stack)
        self._wait_for(stack, 'stack_delete_complete')

    def _wait_for(self, stack, event):
        waiter = self._client.get_waiter(event)
        waiter.wait(StackName=stack)
