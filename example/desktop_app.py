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

    await showcase_vault_operations(client)

    await showcase_batch_item_operations(client, vault_id)

    group_id = os.environ.get("OP_GROUP_ID")
    if group_id is None:
        raise Exception("OP_GROUP_ID is required")
    
    await showcase_group_permission_operations(client, vault_id, group_id)

async def showcase_vault_operations(client: Client):
    # [developer-docs.sdk.python.create-vault]-start
    # Create Vault
    vault_create_params = VaultCreateParams(
    title="Python SDK Vault",
    description="A description",
    allow_admins_access=False,
    )
    created_vault = await client.vaults.create(vault_create_params)
    print(f"Created vault: {created_vault.id} - {created_vault.title}")
    # [developer-docs.sdk.python.create-vault]-end

    # [developer-docs.sdk.python.vault-overview]-start
    vault_overview = await client.vaults.get_overview(created_vault.id)
    print(vault_overview)
    # [developer-docs.sdk.python.vault-overview]-end

    # [developer-docs.sdk.python.update-vault]-start
    # Update Vault
    update_params = VaultUpdateParams(
        title="Python SDK Updated Name",
        description="Updated description",
    )
    
    await client.vaults.update(created_vault.id, update_params)
    # [developer-docs.sdk.python.update-vault]-end

    # [developer-docs.sdk.python.get-vault-details]-start
    # Get Vault
    get_params = VaultGetParams(
        accessors=True,
    )

    updated_vault = await client.vaults.get(created_vault.id, get_params)
    print(f"Updated vault: {updated_vault.id} - {updated_vault.title}")
    # [developer-docs.sdk.python.get-vault-details]-end

    # [developer-docs.sdk.python.delete-vault]-start
    # Delete Vault
    await client.vaults.delete(created_vault.id)
    # [developer-docs.sdk.python.delete-vault]-end

    # [developer-docs.sdk.python.list-vault]-start
    # List Vaults
    vaults = await client.vaults.list()
    for vault in vaults:
        print(vault.title)
    # [developer-docs.sdk.python.list-vault]-end

async def showcase_group_permission_operations(client: Client, vault_id: str, group_id: str):

    # [developer-docs.sdk.python.grant-group-permissions]-start
    # Grant Group Permissions
    await client.vaults.grant_group_permissions(
        vault_id=vault_id,
        group_permissions_list=[
            GroupAccess(
                group_id=group_id,
                permissions=READ_ITEMS,
            )
        ],
    )
    print(f"Granted group {group_id} permissions to vault {vault_id}")
    # [developer-docs.sdk.python.grant-group-permissions]-end

    # [developer-docs.sdk.python.update-group-permissions]-start
    # Update Group Permissions
    await client.vaults.update_group_permissions(
        group_permissions_list=[
            GroupVaultAccess(
                vault_id=vault_id,
                group_id=group_id,
                permissions= READ_ITEMS | CREATE_ITEMS | UPDATE_ITEMS,
            )
        ],
    )
    print(f"Updated group {group_id} permissions to vault {vault_id}")
    # [developer-docs.sdk.python.update-group-permissions]-start

    # [developer-docs.sdk.python.revoke-group-permissions]-start
    # Revoke Group Permissions
    await client.vaults.revoke_group_permissions(
        vault_id=vault_id,
        group_id=group_id,
    )
    # [developer-docs.sdk.python.update-group-permissions]-end
    
    # [developer-docs.sdk.python.get-group]-start
    # Get a group
    group = await client.groups.get(group_id, GroupGetParams(vaultPermissions=False))
    print(group)
    # [developer-docs.sdk.python.get-group]-end

async def showcase_batch_item_operations(client: Client, vault_id: str):
    # [developer-docs.sdk.python.batch-create-items]-start
    items_to_create = []
    for i in range(1, 4):
        items_to_create.append(
            ItemCreateParams(
                title="My Login Item {}".format(i),
                category=ItemCategory.LOGIN,
                vault_id=vault_id,
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
    batchCreateResponse = await client.items.create_all(vault_id, items_to_create)

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
    batchGetReponse = await client.items.get_all(vault_id, item_ids)
    for res in batchGetReponse.individual_responses:
        if res.content is not None:
            print('Obtained item "{}" ({})'.format(res.content.title, res.content.id))
        elif res.error is not None:
            print("[Batch get] Something went wrong: {}".format(res.error))
    # [developer-docs.sdk.python.batch-get-items]-end

    # [developer-docs.sdk.python.batch-delete-items]-start
    # Delete multiple items from the same vault in a single batch
    batchDeleteResponse = await client.items.delete_all(vault_id, item_ids)
    for id, res in batchDeleteResponse.individual_responses.items():
        if res.error is not None:
            print("[Batch delete] Something went wrong: {}".format(res.error))
        else:
            print("Deleted item {}".format(id))
    # [developer-docs.sdk.python.batch-delete-items]-end


if __name__ == "__main__":
    asyncio.run(main())
