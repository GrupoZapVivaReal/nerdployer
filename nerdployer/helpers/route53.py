import boto3


class Route53(object):

    def __init__(self):
        self._client = boto3.client('route53')

    def create_record(self, hosted_zone_id, record, target, record_type='CNAME', ttl=300):
        change_batch = {}
        change = {
            'Action': 'UPSERT',
            'ResourceRecordSet': {
                'Name': record,
                'Type': record_type,
                'TTL': ttl,
                'ResourceRecords': [
                    {'Value': target}
                ]
            }
        }
        change_batch['Changes'] = [change]
        self._client.change_resource_record_sets(HostedZoneId=hosted_zone_id, ChangeBatch=change_batch)
