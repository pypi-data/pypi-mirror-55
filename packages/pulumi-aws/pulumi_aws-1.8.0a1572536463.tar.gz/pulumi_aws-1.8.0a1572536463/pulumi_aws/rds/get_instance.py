# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class GetInstanceResult:
    """
    A collection of values returned by getInstance.
    """
    def __init__(__self__, address=None, allocated_storage=None, auto_minor_version_upgrade=None, availability_zone=None, backup_retention_period=None, ca_cert_identifier=None, db_cluster_identifier=None, db_instance_arn=None, db_instance_class=None, db_instance_identifier=None, db_instance_port=None, db_name=None, db_parameter_groups=None, db_security_groups=None, db_subnet_group=None, enabled_cloudwatch_logs_exports=None, endpoint=None, engine=None, engine_version=None, hosted_zone_id=None, iops=None, kms_key_id=None, license_model=None, master_username=None, monitoring_interval=None, monitoring_role_arn=None, multi_az=None, option_group_memberships=None, port=None, preferred_backup_window=None, preferred_maintenance_window=None, publicly_accessible=None, replicate_source_db=None, resource_id=None, storage_encrypted=None, storage_type=None, timezone=None, vpc_security_groups=None, id=None):
        if address and not isinstance(address, str):
            raise TypeError("Expected argument 'address' to be a str")
        __self__.address = address
        """
        The hostname of the RDS instance. See also `endpoint` and `port`.
        """
        if allocated_storage and not isinstance(allocated_storage, float):
            raise TypeError("Expected argument 'allocated_storage' to be a float")
        __self__.allocated_storage = allocated_storage
        """
        Specifies the allocated storage size specified in gigabytes.
        """
        if auto_minor_version_upgrade and not isinstance(auto_minor_version_upgrade, bool):
            raise TypeError("Expected argument 'auto_minor_version_upgrade' to be a bool")
        __self__.auto_minor_version_upgrade = auto_minor_version_upgrade
        """
        Indicates that minor version patches are applied automatically.
        """
        if availability_zone and not isinstance(availability_zone, str):
            raise TypeError("Expected argument 'availability_zone' to be a str")
        __self__.availability_zone = availability_zone
        """
        Specifies the name of the Availability Zone the DB instance is located in.
        """
        if backup_retention_period and not isinstance(backup_retention_period, float):
            raise TypeError("Expected argument 'backup_retention_period' to be a float")
        __self__.backup_retention_period = backup_retention_period
        """
        Specifies the number of days for which automatic DB snapshots are retained.
        """
        if ca_cert_identifier and not isinstance(ca_cert_identifier, str):
            raise TypeError("Expected argument 'ca_cert_identifier' to be a str")
        __self__.ca_cert_identifier = ca_cert_identifier
        """
        Specifies the identifier of the CA certificate for the DB instance.
        """
        if db_cluster_identifier and not isinstance(db_cluster_identifier, str):
            raise TypeError("Expected argument 'db_cluster_identifier' to be a str")
        __self__.db_cluster_identifier = db_cluster_identifier
        """
        If the DB instance is a member of a DB cluster, contains the name of the DB cluster that the DB instance is a member of.
        """
        if db_instance_arn and not isinstance(db_instance_arn, str):
            raise TypeError("Expected argument 'db_instance_arn' to be a str")
        __self__.db_instance_arn = db_instance_arn
        """
        The Amazon Resource Name (ARN) for the DB instance.
        """
        if db_instance_class and not isinstance(db_instance_class, str):
            raise TypeError("Expected argument 'db_instance_class' to be a str")
        __self__.db_instance_class = db_instance_class
        """
        Contains the name of the compute and memory capacity class of the DB instance.
        """
        if db_instance_identifier and not isinstance(db_instance_identifier, str):
            raise TypeError("Expected argument 'db_instance_identifier' to be a str")
        __self__.db_instance_identifier = db_instance_identifier
        if db_instance_port and not isinstance(db_instance_port, float):
            raise TypeError("Expected argument 'db_instance_port' to be a float")
        __self__.db_instance_port = db_instance_port
        """
        Specifies the port that the DB instance listens on.
        """
        if db_name and not isinstance(db_name, str):
            raise TypeError("Expected argument 'db_name' to be a str")
        __self__.db_name = db_name
        """
        Contains the name of the initial database of this instance that was provided at create time, if one was specified when the DB instance was created. This same name is returned for the life of the DB instance.
        """
        if db_parameter_groups and not isinstance(db_parameter_groups, list):
            raise TypeError("Expected argument 'db_parameter_groups' to be a list")
        __self__.db_parameter_groups = db_parameter_groups
        """
        Provides the list of DB parameter groups applied to this DB instance.
        """
        if db_security_groups and not isinstance(db_security_groups, list):
            raise TypeError("Expected argument 'db_security_groups' to be a list")
        __self__.db_security_groups = db_security_groups
        """
        Provides List of DB security groups associated to this DB instance.
        """
        if db_subnet_group and not isinstance(db_subnet_group, str):
            raise TypeError("Expected argument 'db_subnet_group' to be a str")
        __self__.db_subnet_group = db_subnet_group
        """
        Specifies the name of the subnet group associated with the DB instance.
        """
        if enabled_cloudwatch_logs_exports and not isinstance(enabled_cloudwatch_logs_exports, list):
            raise TypeError("Expected argument 'enabled_cloudwatch_logs_exports' to be a list")
        __self__.enabled_cloudwatch_logs_exports = enabled_cloudwatch_logs_exports
        """
        List of log types to export to cloudwatch.
        """
        if endpoint and not isinstance(endpoint, str):
            raise TypeError("Expected argument 'endpoint' to be a str")
        __self__.endpoint = endpoint
        """
        The connection endpoint in `address:port` format.
        """
        if engine and not isinstance(engine, str):
            raise TypeError("Expected argument 'engine' to be a str")
        __self__.engine = engine
        """
        Provides the name of the database engine to be used for this DB instance.
        """
        if engine_version and not isinstance(engine_version, str):
            raise TypeError("Expected argument 'engine_version' to be a str")
        __self__.engine_version = engine_version
        """
        Indicates the database engine version.
        """
        if hosted_zone_id and not isinstance(hosted_zone_id, str):
            raise TypeError("Expected argument 'hosted_zone_id' to be a str")
        __self__.hosted_zone_id = hosted_zone_id
        """
        The canonical hosted zone ID of the DB instance (to be used in a Route 53 Alias record).
        """
        if iops and not isinstance(iops, float):
            raise TypeError("Expected argument 'iops' to be a float")
        __self__.iops = iops
        """
        Specifies the Provisioned IOPS (I/O operations per second) value.
        """
        if kms_key_id and not isinstance(kms_key_id, str):
            raise TypeError("Expected argument 'kms_key_id' to be a str")
        __self__.kms_key_id = kms_key_id
        """
        If StorageEncrypted is true, the KMS key identifier for the encrypted DB instance.
        """
        if license_model and not isinstance(license_model, str):
            raise TypeError("Expected argument 'license_model' to be a str")
        __self__.license_model = license_model
        """
        License model information for this DB instance.
        """
        if master_username and not isinstance(master_username, str):
            raise TypeError("Expected argument 'master_username' to be a str")
        __self__.master_username = master_username
        """
        Contains the master username for the DB instance.
        """
        if monitoring_interval and not isinstance(monitoring_interval, float):
            raise TypeError("Expected argument 'monitoring_interval' to be a float")
        __self__.monitoring_interval = monitoring_interval
        """
        The interval, in seconds, between points when Enhanced Monitoring metrics are collected for the DB instance.
        """
        if monitoring_role_arn and not isinstance(monitoring_role_arn, str):
            raise TypeError("Expected argument 'monitoring_role_arn' to be a str")
        __self__.monitoring_role_arn = monitoring_role_arn
        """
        The ARN for the IAM role that permits RDS to send Enhanced Monitoring metrics to CloudWatch Logs.
        """
        if multi_az and not isinstance(multi_az, bool):
            raise TypeError("Expected argument 'multi_az' to be a bool")
        __self__.multi_az = multi_az
        """
        Specifies if the DB instance is a Multi-AZ deployment.
        """
        if option_group_memberships and not isinstance(option_group_memberships, list):
            raise TypeError("Expected argument 'option_group_memberships' to be a list")
        __self__.option_group_memberships = option_group_memberships
        """
        Provides the list of option group memberships for this DB instance.
        """
        if port and not isinstance(port, float):
            raise TypeError("Expected argument 'port' to be a float")
        __self__.port = port
        """
        The database port.
        """
        if preferred_backup_window and not isinstance(preferred_backup_window, str):
            raise TypeError("Expected argument 'preferred_backup_window' to be a str")
        __self__.preferred_backup_window = preferred_backup_window
        """
        Specifies the daily time range during which automated backups are created.
        """
        if preferred_maintenance_window and not isinstance(preferred_maintenance_window, str):
            raise TypeError("Expected argument 'preferred_maintenance_window' to be a str")
        __self__.preferred_maintenance_window = preferred_maintenance_window
        """
        Specifies the weekly time range during which system maintenance can occur in UTC.
        """
        if publicly_accessible and not isinstance(publicly_accessible, bool):
            raise TypeError("Expected argument 'publicly_accessible' to be a bool")
        __self__.publicly_accessible = publicly_accessible
        """
        Specifies the accessibility options for the DB instance.
        """
        if replicate_source_db and not isinstance(replicate_source_db, str):
            raise TypeError("Expected argument 'replicate_source_db' to be a str")
        __self__.replicate_source_db = replicate_source_db
        """
        The identifier of the source DB that this is a replica of.
        """
        if resource_id and not isinstance(resource_id, str):
            raise TypeError("Expected argument 'resource_id' to be a str")
        __self__.resource_id = resource_id
        """
        The RDS Resource ID of this instance.
        """
        if storage_encrypted and not isinstance(storage_encrypted, bool):
            raise TypeError("Expected argument 'storage_encrypted' to be a bool")
        __self__.storage_encrypted = storage_encrypted
        """
        Specifies whether the DB instance is encrypted.
        """
        if storage_type and not isinstance(storage_type, str):
            raise TypeError("Expected argument 'storage_type' to be a str")
        __self__.storage_type = storage_type
        """
        Specifies the storage type associated with DB instance.
        """
        if timezone and not isinstance(timezone, str):
            raise TypeError("Expected argument 'timezone' to be a str")
        __self__.timezone = timezone
        """
        The time zone of the DB instance.
        """
        if vpc_security_groups and not isinstance(vpc_security_groups, list):
            raise TypeError("Expected argument 'vpc_security_groups' to be a list")
        __self__.vpc_security_groups = vpc_security_groups
        """
        Provides a list of VPC security group elements that the DB instance belongs to.
        """
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        id is the provider-assigned unique ID for this managed resource.
        """
class AwaitableGetInstanceResult(GetInstanceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetInstanceResult(
            address=self.address,
            allocated_storage=self.allocated_storage,
            auto_minor_version_upgrade=self.auto_minor_version_upgrade,
            availability_zone=self.availability_zone,
            backup_retention_period=self.backup_retention_period,
            ca_cert_identifier=self.ca_cert_identifier,
            db_cluster_identifier=self.db_cluster_identifier,
            db_instance_arn=self.db_instance_arn,
            db_instance_class=self.db_instance_class,
            db_instance_identifier=self.db_instance_identifier,
            db_instance_port=self.db_instance_port,
            db_name=self.db_name,
            db_parameter_groups=self.db_parameter_groups,
            db_security_groups=self.db_security_groups,
            db_subnet_group=self.db_subnet_group,
            enabled_cloudwatch_logs_exports=self.enabled_cloudwatch_logs_exports,
            endpoint=self.endpoint,
            engine=self.engine,
            engine_version=self.engine_version,
            hosted_zone_id=self.hosted_zone_id,
            iops=self.iops,
            kms_key_id=self.kms_key_id,
            license_model=self.license_model,
            master_username=self.master_username,
            monitoring_interval=self.monitoring_interval,
            monitoring_role_arn=self.monitoring_role_arn,
            multi_az=self.multi_az,
            option_group_memberships=self.option_group_memberships,
            port=self.port,
            preferred_backup_window=self.preferred_backup_window,
            preferred_maintenance_window=self.preferred_maintenance_window,
            publicly_accessible=self.publicly_accessible,
            replicate_source_db=self.replicate_source_db,
            resource_id=self.resource_id,
            storage_encrypted=self.storage_encrypted,
            storage_type=self.storage_type,
            timezone=self.timezone,
            vpc_security_groups=self.vpc_security_groups,
            id=self.id)

def get_instance(db_instance_identifier=None,opts=None):
    """
    Use this data source to get information about an RDS instance
    
    :param str db_instance_identifier: The name of the RDS instance

    > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/d/db_instance.html.markdown.
    """
    __args__ = dict()

    __args__['dbInstanceIdentifier'] = db_instance_identifier
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('aws:rds/getInstance:getInstance', __args__, opts=opts).value

    return AwaitableGetInstanceResult(
        address=__ret__.get('address'),
        allocated_storage=__ret__.get('allocatedStorage'),
        auto_minor_version_upgrade=__ret__.get('autoMinorVersionUpgrade'),
        availability_zone=__ret__.get('availabilityZone'),
        backup_retention_period=__ret__.get('backupRetentionPeriod'),
        ca_cert_identifier=__ret__.get('caCertIdentifier'),
        db_cluster_identifier=__ret__.get('dbClusterIdentifier'),
        db_instance_arn=__ret__.get('dbInstanceArn'),
        db_instance_class=__ret__.get('dbInstanceClass'),
        db_instance_identifier=__ret__.get('dbInstanceIdentifier'),
        db_instance_port=__ret__.get('dbInstancePort'),
        db_name=__ret__.get('dbName'),
        db_parameter_groups=__ret__.get('dbParameterGroups'),
        db_security_groups=__ret__.get('dbSecurityGroups'),
        db_subnet_group=__ret__.get('dbSubnetGroup'),
        enabled_cloudwatch_logs_exports=__ret__.get('enabledCloudwatchLogsExports'),
        endpoint=__ret__.get('endpoint'),
        engine=__ret__.get('engine'),
        engine_version=__ret__.get('engineVersion'),
        hosted_zone_id=__ret__.get('hostedZoneId'),
        iops=__ret__.get('iops'),
        kms_key_id=__ret__.get('kmsKeyId'),
        license_model=__ret__.get('licenseModel'),
        master_username=__ret__.get('masterUsername'),
        monitoring_interval=__ret__.get('monitoringInterval'),
        monitoring_role_arn=__ret__.get('monitoringRoleArn'),
        multi_az=__ret__.get('multiAz'),
        option_group_memberships=__ret__.get('optionGroupMemberships'),
        port=__ret__.get('port'),
        preferred_backup_window=__ret__.get('preferredBackupWindow'),
        preferred_maintenance_window=__ret__.get('preferredMaintenanceWindow'),
        publicly_accessible=__ret__.get('publiclyAccessible'),
        replicate_source_db=__ret__.get('replicateSourceDb'),
        resource_id=__ret__.get('resourceId'),
        storage_encrypted=__ret__.get('storageEncrypted'),
        storage_type=__ret__.get('storageType'),
        timezone=__ret__.get('timezone'),
        vpc_security_groups=__ret__.get('vpcSecurityGroups'),
        id=__ret__.get('id'))
