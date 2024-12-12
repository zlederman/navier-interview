"""An Azure RM Python Pulumi program"""
import pulumi
from pulumi_azure_native import storage

from components.resource_group import resource_group

sa_conf = pulumi.Config("sa")
storage_account = storage.StorageAccount(
    sa_conf.require("name"),
    resource_group_name=resource_group.name,
    sku={
        "name": storage.SkuName.STANDARD_LRS,
    },
    kind=storage.Kind.STORAGE_V2,
)

mount = storage.FileShare(sa_conf.require("file-share-name"),
    resource_group_name=resource_group.name,
    account_name=storage_account.name,
    share_quota=20
) 

storage_key = (
    pulumi.Output.all(resource_group.name, storage_account.name)
    .apply(
        lambda args: storage.list_storage_account_keys(
            resource_group_name=args[0], account_name=args[1]
        )
    )
    .apply(lambda accountKeys: accountKeys.keys[0].value)
)

