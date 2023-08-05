# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class Broker(pulumi.CustomResource):
    apply_immediately: pulumi.Output[bool]
    """
    Specifies whether any broker modifications
    are applied immediately, or during the next maintenance window. Default is `false`.
    """
    arn: pulumi.Output[str]
    """
    The ARN of the broker.
    """
    auto_minor_version_upgrade: pulumi.Output[bool]
    """
    Enables automatic upgrades to new minor versions for brokers, as Apache releases the versions.
    """
    broker_name: pulumi.Output[str]
    """
    The name of the broker.
    """
    configuration: pulumi.Output[dict]
    """
    Configuration of the broker. See below.
    
      * `id` (`str`) - The Configuration ID.
      * `revision` (`float`) - Revision of the Configuration.
    """
    deployment_mode: pulumi.Output[str]
    """
    The deployment mode of the broker. Supported: `SINGLE_INSTANCE` and `ACTIVE_STANDBY_MULTI_AZ`. Defaults to `SINGLE_INSTANCE`.
    """
    encryption_options: pulumi.Output[dict]
    """
    Configuration block containing encryption options. See below.
    
      * `kms_key_id` (`str`) - Amazon Resource Name (ARN) of Key Management Service (KMS) Customer Master Key (CMK) to use for encryption at rest. Requires setting `use_aws_owned_key` to `false`. To perform drift detection when AWS managed CMKs or customer managed CMKs are in use, this value must be configured.
      * `useAwsOwnedKey` (`bool`) - Boolean to enable an AWS owned Key Management Service (KMS) Customer Master Key (CMK) that is not in your account. Defaults to `true`. Setting to `false` without configuring `kms_key_id` will create an AWS managed Customer Master Key (CMK) aliased to `aws/mq` in your account.
    """
    engine_type: pulumi.Output[str]
    """
    The type of broker engine. Currently, Amazon MQ supports only `ActiveMQ`.
    """
    engine_version: pulumi.Output[str]
    """
    The version of the broker engine. Currently, See the [AmazonMQ Broker Engine docs](https://docs.aws.amazon.com/amazon-mq/latest/developer-guide/broker-engine.html) for supported versions.
    """
    host_instance_type: pulumi.Output[str]
    """
    The broker's instance type. e.g. `mq.t2.micro` or `mq.m4.large`
    """
    instances: pulumi.Output[list]
    """
    A list of information about allocated brokers (both active & standby).
    * `instances.0.console_url` - The URL of the broker's [ActiveMQ Web Console](http://activemq.apache.org/web-console.html).
    * `instances.0.ip_address` - The IP Address of the broker.
    * `instances.0.endpoints` - The broker's wire-level protocol endpoints in the following order & format referenceable e.g. as `instances.0.endpoints.0` (SSL):
    * `ssl://broker-id.mq.us-west-2.amazonaws.com:61617`
    * `amqp+ssl://broker-id.mq.us-west-2.amazonaws.com:5671`
    * `stomp+ssl://broker-id.mq.us-west-2.amazonaws.com:61614`
    * `mqtt+ssl://broker-id.mq.us-west-2.amazonaws.com:8883`
    * `wss://broker-id.mq.us-west-2.amazonaws.com:61619`
    
      * `consoleUrl` (`str`)
      * `endpoints` (`list`)
      * `ip_address` (`str`)
    """
    logs: pulumi.Output[dict]
    """
    Logging configuration of the broker. See below.
    
      * `audit` (`bool`) - Enables audit logging. User management action made using JMX or the ActiveMQ Web Console is logged. Defaults to `false`.
      * `general` (`bool`) - Enables general logging via CloudWatch. Defaults to `false`.
    """
    maintenance_window_start_time: pulumi.Output[dict]
    """
    Maintenance window start time. See below.
    
      * `dayOfWeek` (`str`) - The day of the week. e.g. `MONDAY`, `TUESDAY`, or `WEDNESDAY`
      * `timeOfDay` (`str`) - The time, in 24-hour format. e.g. `02:00`
      * `timeZone` (`str`) - The time zone, UTC by default, in either the Country/City format, or the UTC offset format. e.g. `CET`
    """
    publicly_accessible: pulumi.Output[bool]
    """
    Whether to enable connections from applications outside of the VPC that hosts the broker's subnets.
    """
    security_groups: pulumi.Output[list]
    """
    The list of security group IDs assigned to the broker.
    """
    subnet_ids: pulumi.Output[list]
    """
    The list of subnet IDs in which to launch the broker. A `SINGLE_INSTANCE` deployment requires one subnet. An `ACTIVE_STANDBY_MULTI_AZ` deployment requires two subnets.
    """
    tags: pulumi.Output[dict]
    """
    A mapping of tags to assign to the resource.
    """
    users: pulumi.Output[list]
    """
    The list of all ActiveMQ usernames for the specified broker. See below.
    
      * `consoleAccess` (`bool`) - Whether to enable access to the [ActiveMQ Web Console](http://activemq.apache.org/web-console.html) for the user.
      * `groups` (`list`) - The list of groups (20 maximum) to which the ActiveMQ user belongs.
      * `password` (`str`) - The password of the user. It must be 12 to 250 characters long, at least 4 unique characters, and must not contain commas.
      * `username` (`str`) - The username of the user.
    """
    def __init__(__self__, resource_name, opts=None, apply_immediately=None, auto_minor_version_upgrade=None, broker_name=None, configuration=None, deployment_mode=None, encryption_options=None, engine_type=None, engine_version=None, host_instance_type=None, logs=None, maintenance_window_start_time=None, publicly_accessible=None, security_groups=None, subnet_ids=None, tags=None, users=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides an MQ Broker Resource. This resources also manages users for the broker.
        
        For more information on Amazon MQ, see [Amazon MQ documentation](https://docs.aws.amazon.com/amazon-mq/latest/developer-guide/welcome.html).
        
        Changes to an MQ Broker can occur when you change a
        parameter, such as `configuration` or `user`, and are reflected in the next maintenance
        window. Because of this, this provider may report a difference in its planning
        phase because a modification has not yet taken place. You can use the
        `apply_immediately` flag to instruct the service to apply the change immediately
        (see documentation below).
        
        > **Note:** using `apply_immediately` can result in a
        brief downtime as the broker reboots.
        
        > **Note:** All arguments including the username and password will be stored in the raw state as plain-text.
        [Read more about sensitive data in state](https://www.terraform.io/docs/state/sensitive-data.html).
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] apply_immediately: Specifies whether any broker modifications
               are applied immediately, or during the next maintenance window. Default is `false`.
        :param pulumi.Input[bool] auto_minor_version_upgrade: Enables automatic upgrades to new minor versions for brokers, as Apache releases the versions.
        :param pulumi.Input[str] broker_name: The name of the broker.
        :param pulumi.Input[dict] configuration: Configuration of the broker. See below.
        :param pulumi.Input[str] deployment_mode: The deployment mode of the broker. Supported: `SINGLE_INSTANCE` and `ACTIVE_STANDBY_MULTI_AZ`. Defaults to `SINGLE_INSTANCE`.
        :param pulumi.Input[dict] encryption_options: Configuration block containing encryption options. See below.
        :param pulumi.Input[str] engine_type: The type of broker engine. Currently, Amazon MQ supports only `ActiveMQ`.
        :param pulumi.Input[str] engine_version: The version of the broker engine. Currently, See the [AmazonMQ Broker Engine docs](https://docs.aws.amazon.com/amazon-mq/latest/developer-guide/broker-engine.html) for supported versions.
        :param pulumi.Input[str] host_instance_type: The broker's instance type. e.g. `mq.t2.micro` or `mq.m4.large`
        :param pulumi.Input[dict] logs: Logging configuration of the broker. See below.
        :param pulumi.Input[dict] maintenance_window_start_time: Maintenance window start time. See below.
        :param pulumi.Input[bool] publicly_accessible: Whether to enable connections from applications outside of the VPC that hosts the broker's subnets.
        :param pulumi.Input[list] security_groups: The list of security group IDs assigned to the broker.
        :param pulumi.Input[list] subnet_ids: The list of subnet IDs in which to launch the broker. A `SINGLE_INSTANCE` deployment requires one subnet. An `ACTIVE_STANDBY_MULTI_AZ` deployment requires two subnets.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the resource.
        :param pulumi.Input[list] users: The list of all ActiveMQ usernames for the specified broker. See below.
        
        The **configuration** object supports the following:
        
          * `id` (`pulumi.Input[str]`) - The Configuration ID.
          * `revision` (`pulumi.Input[float]`) - Revision of the Configuration.
        
        The **encryption_options** object supports the following:
        
          * `kms_key_id` (`pulumi.Input[str]`) - Amazon Resource Name (ARN) of Key Management Service (KMS) Customer Master Key (CMK) to use for encryption at rest. Requires setting `use_aws_owned_key` to `false`. To perform drift detection when AWS managed CMKs or customer managed CMKs are in use, this value must be configured.
          * `useAwsOwnedKey` (`pulumi.Input[bool]`) - Boolean to enable an AWS owned Key Management Service (KMS) Customer Master Key (CMK) that is not in your account. Defaults to `true`. Setting to `false` without configuring `kms_key_id` will create an AWS managed Customer Master Key (CMK) aliased to `aws/mq` in your account.
        
        The **logs** object supports the following:
        
          * `audit` (`pulumi.Input[bool]`) - Enables audit logging. User management action made using JMX or the ActiveMQ Web Console is logged. Defaults to `false`.
          * `general` (`pulumi.Input[bool]`) - Enables general logging via CloudWatch. Defaults to `false`.
        
        The **maintenance_window_start_time** object supports the following:
        
          * `dayOfWeek` (`pulumi.Input[str]`) - The day of the week. e.g. `MONDAY`, `TUESDAY`, or `WEDNESDAY`
          * `timeOfDay` (`pulumi.Input[str]`) - The time, in 24-hour format. e.g. `02:00`
          * `timeZone` (`pulumi.Input[str]`) - The time zone, UTC by default, in either the Country/City format, or the UTC offset format. e.g. `CET`
        
        The **users** object supports the following:
        
          * `consoleAccess` (`pulumi.Input[bool]`) - Whether to enable access to the [ActiveMQ Web Console](http://activemq.apache.org/web-console.html) for the user.
          * `groups` (`pulumi.Input[list]`) - The list of groups (20 maximum) to which the ActiveMQ user belongs.
          * `password` (`pulumi.Input[str]`) - The password of the user. It must be 12 to 250 characters long, at least 4 unique characters, and must not contain commas.
          * `username` (`pulumi.Input[str]`) - The username of the user.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/mq_broker.html.markdown.
        """
        if __name__ is not None:
            warnings.warn("explicit use of __name__ is deprecated", DeprecationWarning)
            resource_name = __name__
        if __opts__ is not None:
            warnings.warn("explicit use of __opts__ is deprecated, use 'opts' instead", DeprecationWarning)
            opts = __opts__
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = dict()

            __props__['apply_immediately'] = apply_immediately
            __props__['auto_minor_version_upgrade'] = auto_minor_version_upgrade
            if broker_name is None:
                raise TypeError("Missing required property 'broker_name'")
            __props__['broker_name'] = broker_name
            __props__['configuration'] = configuration
            __props__['deployment_mode'] = deployment_mode
            __props__['encryption_options'] = encryption_options
            if engine_type is None:
                raise TypeError("Missing required property 'engine_type'")
            __props__['engine_type'] = engine_type
            if engine_version is None:
                raise TypeError("Missing required property 'engine_version'")
            __props__['engine_version'] = engine_version
            if host_instance_type is None:
                raise TypeError("Missing required property 'host_instance_type'")
            __props__['host_instance_type'] = host_instance_type
            __props__['logs'] = logs
            __props__['maintenance_window_start_time'] = maintenance_window_start_time
            __props__['publicly_accessible'] = publicly_accessible
            if security_groups is None:
                raise TypeError("Missing required property 'security_groups'")
            __props__['security_groups'] = security_groups
            __props__['subnet_ids'] = subnet_ids
            __props__['tags'] = tags
            if users is None:
                raise TypeError("Missing required property 'users'")
            __props__['users'] = users
            __props__['arn'] = None
            __props__['instances'] = None
        super(Broker, __self__).__init__(
            'aws:mq/broker:Broker',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, apply_immediately=None, arn=None, auto_minor_version_upgrade=None, broker_name=None, configuration=None, deployment_mode=None, encryption_options=None, engine_type=None, engine_version=None, host_instance_type=None, instances=None, logs=None, maintenance_window_start_time=None, publicly_accessible=None, security_groups=None, subnet_ids=None, tags=None, users=None):
        """
        Get an existing Broker resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.
        
        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] apply_immediately: Specifies whether any broker modifications
               are applied immediately, or during the next maintenance window. Default is `false`.
        :param pulumi.Input[str] arn: The ARN of the broker.
        :param pulumi.Input[bool] auto_minor_version_upgrade: Enables automatic upgrades to new minor versions for brokers, as Apache releases the versions.
        :param pulumi.Input[str] broker_name: The name of the broker.
        :param pulumi.Input[dict] configuration: Configuration of the broker. See below.
        :param pulumi.Input[str] deployment_mode: The deployment mode of the broker. Supported: `SINGLE_INSTANCE` and `ACTIVE_STANDBY_MULTI_AZ`. Defaults to `SINGLE_INSTANCE`.
        :param pulumi.Input[dict] encryption_options: Configuration block containing encryption options. See below.
        :param pulumi.Input[str] engine_type: The type of broker engine. Currently, Amazon MQ supports only `ActiveMQ`.
        :param pulumi.Input[str] engine_version: The version of the broker engine. Currently, See the [AmazonMQ Broker Engine docs](https://docs.aws.amazon.com/amazon-mq/latest/developer-guide/broker-engine.html) for supported versions.
        :param pulumi.Input[str] host_instance_type: The broker's instance type. e.g. `mq.t2.micro` or `mq.m4.large`
        :param pulumi.Input[list] instances: A list of information about allocated brokers (both active & standby).
               * `instances.0.console_url` - The URL of the broker's [ActiveMQ Web Console](http://activemq.apache.org/web-console.html).
               * `instances.0.ip_address` - The IP Address of the broker.
               * `instances.0.endpoints` - The broker's wire-level protocol endpoints in the following order & format referenceable e.g. as `instances.0.endpoints.0` (SSL):
               * `ssl://broker-id.mq.us-west-2.amazonaws.com:61617`
               * `amqp+ssl://broker-id.mq.us-west-2.amazonaws.com:5671`
               * `stomp+ssl://broker-id.mq.us-west-2.amazonaws.com:61614`
               * `mqtt+ssl://broker-id.mq.us-west-2.amazonaws.com:8883`
               * `wss://broker-id.mq.us-west-2.amazonaws.com:61619`
        :param pulumi.Input[dict] logs: Logging configuration of the broker. See below.
        :param pulumi.Input[dict] maintenance_window_start_time: Maintenance window start time. See below.
        :param pulumi.Input[bool] publicly_accessible: Whether to enable connections from applications outside of the VPC that hosts the broker's subnets.
        :param pulumi.Input[list] security_groups: The list of security group IDs assigned to the broker.
        :param pulumi.Input[list] subnet_ids: The list of subnet IDs in which to launch the broker. A `SINGLE_INSTANCE` deployment requires one subnet. An `ACTIVE_STANDBY_MULTI_AZ` deployment requires two subnets.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the resource.
        :param pulumi.Input[list] users: The list of all ActiveMQ usernames for the specified broker. See below.
        
        The **configuration** object supports the following:
        
          * `id` (`pulumi.Input[str]`) - The Configuration ID.
          * `revision` (`pulumi.Input[float]`) - Revision of the Configuration.
        
        The **encryption_options** object supports the following:
        
          * `kms_key_id` (`pulumi.Input[str]`) - Amazon Resource Name (ARN) of Key Management Service (KMS) Customer Master Key (CMK) to use for encryption at rest. Requires setting `use_aws_owned_key` to `false`. To perform drift detection when AWS managed CMKs or customer managed CMKs are in use, this value must be configured.
          * `useAwsOwnedKey` (`pulumi.Input[bool]`) - Boolean to enable an AWS owned Key Management Service (KMS) Customer Master Key (CMK) that is not in your account. Defaults to `true`. Setting to `false` without configuring `kms_key_id` will create an AWS managed Customer Master Key (CMK) aliased to `aws/mq` in your account.
        
        The **instances** object supports the following:
        
          * `consoleUrl` (`pulumi.Input[str]`)
          * `endpoints` (`pulumi.Input[list]`)
          * `ip_address` (`pulumi.Input[str]`)
        
        The **logs** object supports the following:
        
          * `audit` (`pulumi.Input[bool]`) - Enables audit logging. User management action made using JMX or the ActiveMQ Web Console is logged. Defaults to `false`.
          * `general` (`pulumi.Input[bool]`) - Enables general logging via CloudWatch. Defaults to `false`.
        
        The **maintenance_window_start_time** object supports the following:
        
          * `dayOfWeek` (`pulumi.Input[str]`) - The day of the week. e.g. `MONDAY`, `TUESDAY`, or `WEDNESDAY`
          * `timeOfDay` (`pulumi.Input[str]`) - The time, in 24-hour format. e.g. `02:00`
          * `timeZone` (`pulumi.Input[str]`) - The time zone, UTC by default, in either the Country/City format, or the UTC offset format. e.g. `CET`
        
        The **users** object supports the following:
        
          * `consoleAccess` (`pulumi.Input[bool]`) - Whether to enable access to the [ActiveMQ Web Console](http://activemq.apache.org/web-console.html) for the user.
          * `groups` (`pulumi.Input[list]`) - The list of groups (20 maximum) to which the ActiveMQ user belongs.
          * `password` (`pulumi.Input[str]`) - The password of the user. It must be 12 to 250 characters long, at least 4 unique characters, and must not contain commas.
          * `username` (`pulumi.Input[str]`) - The username of the user.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/mq_broker.html.markdown.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()
        __props__["apply_immediately"] = apply_immediately
        __props__["arn"] = arn
        __props__["auto_minor_version_upgrade"] = auto_minor_version_upgrade
        __props__["broker_name"] = broker_name
        __props__["configuration"] = configuration
        __props__["deployment_mode"] = deployment_mode
        __props__["encryption_options"] = encryption_options
        __props__["engine_type"] = engine_type
        __props__["engine_version"] = engine_version
        __props__["host_instance_type"] = host_instance_type
        __props__["instances"] = instances
        __props__["logs"] = logs
        __props__["maintenance_window_start_time"] = maintenance_window_start_time
        __props__["publicly_accessible"] = publicly_accessible
        __props__["security_groups"] = security_groups
        __props__["subnet_ids"] = subnet_ids
        __props__["tags"] = tags
        __props__["users"] = users
        return Broker(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

