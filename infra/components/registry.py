
import pulumi
from pulumi_azure_native import authorization, containerregistry
from pulumi_azuread import Application, ServicePrincipal, ServicePrincipalPassword
from components.resource_group import resource_group


acr_conf = pulumi.Config("acr")
current = authorization.get_client_config()
# Create an Azure Container Registry
acr = containerregistry.Registry(
    acr_conf.require("name"),
    resource_group_name=resource_group.name,
    sku={
        "name": containerregistry.SkuName.BASIC
    },
    zone_redundancy= containerregistry.ZoneRedundancy.DISABLED,
    admin_user_enabled=True
)

acr_cred = pulumi.Output.all(resource_group.name, acr.name).apply(
    lambda args: containerregistry.list_registry_credentials(
        resource_group_name=args[0],
        registry_name=args[1]
    )
)


# Create a password for the Service Principal
app = Application("github-actions-app",
    display_name="github-actions-app")

gh_service_principal = ServicePrincipal("github-actions-sp", client_id=app.client_id)
sp_password = ServicePrincipalPassword("github-actions-sp-pwd",
    service_principal_id=gh_service_principal.id,
    end_date="2025-01-01T01:02:03Z")

gh_push_role = authorization.RoleAssignment("sp-acr-push-role",
    scope=acr.id,  # Reference to your ACR resource
    role_definition_id=acr_conf.require("push-role-id"),
    principal_type=authorization.PrincipalType.SERVICE_PRINCIPAL,
    principal_id=gh_service_principal.object_id
)

