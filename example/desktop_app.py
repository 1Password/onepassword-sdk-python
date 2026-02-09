# [developer-docs.sdk.python.sdk-import]-start
from onepassword import *
import asyncio
import os


async def main():
    vault_id = os.environ.get("OP_VAULT_ID")
    if vault_id is None:
        raise Exception("OP_VAULT_ID is required")

    # [developer-docs.sdk.python.client-initialization]-start
    # Connects to the 1Password desktop app.
    client = await Client.authenticate(
        auth=DesktopAuth(
            account_name="YourAccountNameAsShownInTheDesktopApp"  # Set to your 1Password account name as shown at the top left sidebar of the app, or your account UUID.
        ),
        # Set the following to your own integration name and version.
        integration_name="My 1Password Integration",
        integration_version="v1.0.0",
    )

    # [developer-docs.sdk.python.list-vaults]-start
    vaults = await client.vaults.list()
    for vault in vaults:
        print(vault)
    # [developer-docs.sdk.python.list-vaults]-end

    # [developer-docs.sdk.python.list-items]-start
    overviews = await client.items.list(vault_id)
    for overview in overviews:
        print(overview.title)
    # [developer-docs.sdk.python.list-items]-end

    # [developer-docs.sdk.python.get-vault-overview]-start
    # Get vault overview
    vaultOverview = await client.vaults.get_overview(vault_id)
    print(vaultOverview)
    # [developer-docs.sdk.python.get-vault-overview]-end

    # [developer-docs.sdk.python.get-vault-details]-start
    # Get vault details
    vault = await client.vaults.get(vaultOverview.id, VaultGetParams(accessors=False))
    print(vault)
    # [developer-docs.sdk.python.get-vault-details]-end

    # [developer-docs.sdk.python.batch-create-items]-start
    items_to_create = []
    for i in range(1, 4):
        items_to_create.append(
            ItemCreateParams(
                title="My Login Item {}".format(i),
                category=ItemCategory.LOGIN,
                vault_id=vault.id,
                fields=[
                    ItemField(
                        id="username",
                        title="username",
                        field_type=ItemFieldType.TEXT,
                        value="mynameisjeff",
                    ),
                    ItemField(
                        id="password",
                        title="password",
                        field_type=ItemFieldType.CONCEALED,
                        value="jeff",
                    ),
                    ItemField(
                        id="onetimepassword",
                        title="one-time-password",
                        field_type=ItemFieldType.TOTP,
                        section_id="totpsection",
                        value="otpauth://totp/my-example-otp?secret=jncrjgbdjnrncbjsr&issuer=1Password",
                    ),
                ],
                sections=[
                    ItemSection(id="", title=""),
                    ItemSection(id="totpsection", title=""),
                ],
                tags=["test tag 1", "test tag 2"],
                websites=[
                    Website(
                        label="my custom website",
                        url="https://example.com",
                        autofill_behavior=AutofillBehavior.NEVER,
                    )
                ],
            )
        )

    # Create all items in the same vault in a single batch
    batchCreateResponse = await client.items.create_all(vault.id, items_to_create)

    item_ids = []
    for res in batchCreateResponse.individual_responses:
        if res.content is not None:
            print('Created item "{}" ({})'.format(res.content.title, res.content.id))
            item_ids.append(res.content.id)
        elif res.error is not None:
            print("[Batch create] Something went wrong: {}".format(res.error))
    # [developer-docs.sdk.python.batch-create-items]-end

    # [developer-docs.sdk.python.batch-get-items]-start
    # Get multiple items form the same vault in a single batch
    batchGetReponse = await client.items.get_all(vault.id, item_ids)
    for res in batchGetReponse.individual_responses:
        if res.content is not None:
            print('Obtained item "{}" ({})'.format(res.content.title, res.content.id))
        elif res.error is not None:
            print("[Batch get] Something went wrong: {}".format(res.error))
    # [developer-docs.sdk.python.batch-get-items]-end

    # [developer-docs.sdk.python.batch-delete-items]-start
    # Delete multiple items from the same vault in a single batch
    batchDeleteResponse = await client.items.delete_all(vault.id, item_ids)
    for id, res in batchDeleteResponse.individual_responses.items():
        if res.error is not None:
            print("[Batch delete] Something went wrong: {}".format(res.error))
        else:
            print("Deleted item {}".format(id))
    # [developer-docs.sdk.python.batch-delete-items]-end

    group_id = os.environ.get("OP_GROUP_ID")
    if group_id is None:
        raise Exception("OP_GROUP_ID is required")

    # [developer-docs.sdk.python.get-group]-start
    # Get a group
    group = await client.groups.get(group_id, GroupGetParams(vaultPermissions=False))
    print(group)
    # [developer-docs.sdk.python.get-group]-end

    environment_id = os.environ.get("OP_ENVIRONMENT_ID")
    if environment_id is not None:
        # [developer-docs.sdk.python.get-environment-variables]-start
        # Read variables from a 1Password Environment
        environment = await client.environments.get_variables(environment_id)
        for variable in environment.variables:
            print(f"{variable.name}: {variable.value} (masked: {variable.masked})")
        # [developer-docs.sdk.python.get-environment-variables]-end


if __name__ == "__main__":
    asyncio.run(main())
