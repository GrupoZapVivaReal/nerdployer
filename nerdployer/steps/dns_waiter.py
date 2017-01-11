
from nerdployer.step import BaseStep
import nerdployer.helpers.utils as utils
import time
import dns.resolver as resolver

MAX_HEALTH_CHECK_ATTEMPTS = 20
HEALTH_CHECK_WAIT_TIME = 15
DEFAULT_DNS_TYPE = 'CNAME'


class DnsWaiterStep(BaseStep):
    def __init__(self, config):
        super().__init__('dns_waiter', config)

    def execute(self, context, params):
        dns = params['dns']
        target = params['target']
        dns_type = utils.fallback([params['dns_type'], DEFAULT_DNS_TYPE])

        current_attempt = 0
        done = False
        while True:
            answers = dns.resolver.query(dns, dns_type)

            for answer in answers:
                if str(answer.target)[:-1] == target:
                    done = True

            if done:
                break

            if current_attempt == MAX_HEALTH_CHECK_ATTEMPTS:
                raise Exception('attempt count exceeded for checking the dns change')

            resolver.Cache().flush()
            current_attempt += 1
            time.sleep(HEALTH_CHECK_WAIT_TIME)
