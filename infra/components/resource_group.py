import pulumi
from pulumi_azure_native import resources

rg_conf = pulumi.Config("rg")
resource_group = resources.ResourceGroup(rg_conf.require("name"))