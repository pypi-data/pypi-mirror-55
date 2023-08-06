import unittest
from unittest.mock import MagicMock

from botocore.exceptions import ClientError
from placebo.utils import placebo_session

from aws_gate.query import _query_aws_api, query_instance, AWSConnectionError


class TestQuery(unittest.TestCase):
    @placebo_session
    def setUp(self, session):
        self.ec2 = session.resource("ec2", region_name="eu-west-1")

        self.instance_id = "i-0c32153096cd68a6d"

    def test_query_aws_api_exception(self):
        ec2_mock = MagicMock()

        # https://github.com/surbas/pg2kinesis/blob/master/tests/test_stream.py#L20
        error_response = {"Error": {"Code": "ResourceInUseException"}}
        ec2_mock.configure_mock(
            **{
                "instances.filter.side_effect": ClientError(
                    error_response, "random_ec2_op"
                )
            }
        )

        filters = [{"Name": "ip-address", "Values": ["10.1.1.1"]}]
        with self.assertRaises(AWSConnectionError):
            _query_aws_api(filters=filters, ec2=ec2_mock)

    def test_query_instance_by_private_ip_address(self):
        self.assertEqual(self.instance_id, query_instance("10.69.104.49", ec2=self.ec2))

    def test_query_instance_by_dns_name(self):
        self.assertEqual(
            self.instance_id,
            query_instance(
                "ec2-18-202-215-108.eu-west-1.compute.amazonaws.com", ec2=self.ec2
            ),
        )

    def test_query_instance_by_private_dns_name(self):
        self.assertEqual(
            self.instance_id,
            query_instance("ip-10-69-104-49.eu-west-1.compute.internal", ec2=self.ec2),
        )

    def test_query_instance_by_ip_address(self):
        self.assertEqual(
            self.instance_id, query_instance("18.202.215.108", ec2=self.ec2)
        )

    def test_query_instance_by_id(self):
        self.assertEqual(
            self.instance_id, query_instance(self.instance_id, ec2=self.ec2)
        )

    def test_query_instance_by_tag(self):
        self.assertEqual(
            self.instance_id, query_instance("Name:dummy-instance", ec2=self.ec2)
        )

    def test_query_instance_by_name(self):
        self.assertEqual(
            self.instance_id, query_instance("dummy-instance", ec2=self.ec2)
        )

    def test_query_instance_ec2_unitialized(self):
        with self.assertRaises(ValueError):
            query_instance("18.205.215.108")
