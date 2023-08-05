# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class GetEncryptionByDefaultResult:
    """
    A collection of values returned by getEncryptionByDefault.
    """
    def __init__(__self__, enabled=None, id=None):
        if enabled and not isinstance(enabled, bool):
            raise TypeError("Expected argument 'enabled' to be a bool")
        __self__.enabled = enabled
        """
        Whether or not default EBS encryption is enabled. Returns as `true` or `false`.
        """
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        id is the provider-assigned unique ID for this managed resource.
        """
class AwaitableGetEncryptionByDefaultResult(GetEncryptionByDefaultResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetEncryptionByDefaultResult(
            enabled=self.enabled,
            id=self.id)

def get_encryption_by_default(opts=None):
    """
    Provides a way to check whether default EBS encryption is enabled for your AWS account in the current AWS region.

    > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/d/ebs_encryption_by_default.html.markdown.
    """
    __args__ = dict()

    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('aws:ebs/getEncryptionByDefault:getEncryptionByDefault', __args__, opts=opts).value

    return AwaitableGetEncryptionByDefaultResult(
        enabled=__ret__.get('enabled'),
        id=__ret__.get('id'))
