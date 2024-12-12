"""An Azure RM Python Pulumi program"""
import pulumi
from pulumi_azure_native import authorization

from components.registry import acr, acr_cred, sp_password, app
from components.storage import storage_key
from components.container import container_instance
#live azure client
current = authorization.get_client_config()


def create_credentials(app_id, password, tenant_id, subscription_id):
    return {
        "clientId": app_id,
        "clientSecret": password,
        "subscriptionId": subscription_id,
        "tenantId": tenant_id
    }

pulumi.export(
    "github_service_principal",
        pulumi.Output.all(
            app.client_id,
            sp_password.value,
            current.tenant_id,
            current.subscription_id
        ).apply(lambda args: create_credentials(args[0], args[1], args[2], args[3]))
)

pulumi.export("primary_storage_key", pulumi.Output.secret(storage_key))
pulumi.export("registry_login_server", acr.login_server)
pulumi.export("registry_username", acr_cred.apply(lambda creds: creds.username))
pulumi.export("registry_password", pulumi.Output.secret(acr_cred.apply(lambda creds: creds.passwords[0].value)))
pulumi.export("container_ip", container_instance.ip_address.apply(lambda ip: ip.ip))