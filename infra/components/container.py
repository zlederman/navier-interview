# Create a container instance
import pulumi
from pulumi_azure_native import containerinstance


from components.storage import mount, storage_account, storage_key
from components.registry import acr, acr_cred
from components.resource_group import resource_group

aci_conf = pulumi.Config("aci")
image_registry = containerinstance.ImageRegistryCredentialArgs(
            server=acr.login_server,
            username=acr_cred.username,
            password=pulumi.Output.secret(acr_cred.passwords[0].value)
)

volume = containerinstance.VolumeArgs(
        name=aci_conf.require("volume-name"),
        azure_file=containerinstance.AzureFileVolumeArgs(
            share_name=mount.name,
            storage_account_name=storage_account.name,
            storage_account_key=storage_key
        )
)

container = containerinstance.ContainerArgs(
        name=aci_conf.require("name"),
        image=aci_conf.require("image"),
        resources=containerinstance.ResourceRequirementsArgs(
            requests=containerinstance.ResourceRequestsArgs(
                cpu=int(aci_conf.require("cpu-cores")),
                memory_in_gb=int(aci_conf.require("memory-gb")),
            )
        ),
        ports=[containerinstance.ContainerPortArgs(port=80)],
        volume_mounts=[containerinstance.VolumeMountArgs(
            name=aci_conf.require("volume-name"),
            mount_path=aci_conf.require("volume-mnt-path"),

        )]
)

container_instance = containerinstance.ContainerGroup(
    resource_name=aci_conf.require("group-name"),
    resource_group_name=resource_group.name,
    os_type=containerinstance.OperatingSystemTypes.LINUX,
    restart_policy=containerinstance.ContainerGroupRestartPolicy.ALWAYS,
    ip_address=containerinstance.IpAddressArgs(
        type=containerinstance.ContainerGroupIpAddressType.PUBLIC,
        ports=[containerinstance.PortArgs(
            port=80,
            protocol=containerinstance.ContainerGroupNetworkProtocol.TCP
        )]
    ),
    image_registry_credentials=[image_registry],
    volumes=[volume],
    containers=[container]
)