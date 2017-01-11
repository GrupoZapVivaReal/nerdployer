
from nerdployer.step import BaseStep
import nerdployer.helpers.utils as utils
import time
import boto3

MAX_HEALTH_CHECK_ATTEMPTS = 20
HEALTH_CHECK_WAIT_TIME = 15


class ElbHealthyWaiterStep(BaseStep):
    def __init__(self, config):
        super().__init__('elb_healthy_waiter', config)

    def execute(self, step_name, context, params):
        region = utils.fallback([params['region'], self.config['region']])
        asg_client = boto3.client('autoscaling', region_name=region)
        elb_client = boto3.client('elb', region_name=region)

        asg = params['asg_name']
        elb = params['elb_name']

        asg_instances = asg_client.describe_auto_scaling_groups(AutoScalingGroupNames=[asg])['AutoScalingGroups'][0]['Instances']

        load_balance_instances_param = [{'InstanceId': asg_instance['InstanceId']} for asg_instance in asg_instances]

        expected_instances_health_count = len(asg_instances)
        current_attempt = 0

        while True:
            instance_states = elb_client.describe_instance_health(LoadBalancerName=elb, Instances=load_balance_instances_param)
            if expected_instances_health_count == len(instance_states['InstanceStates']):
                current_health_instances = 0
                for instance_state in instance_states['InstanceStates']:
                    if instance_state['State'] == 'InService':
                        current_health_instances += 1
                if current_health_instances == expected_instances_health_count:
                    break

            if current_attempt == MAX_HEALTH_CHECK_ATTEMPTS:
                raise Exception('attempt count exceeded for checking elb instances state')

            current_attempt += 1
            time.sleep(HEALTH_CHECK_WAIT_TIME)
