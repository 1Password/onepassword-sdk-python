import asyncio
import os

# [developer-docs.sdk.python.sdk-import]-start
from onepassword import *
# [developer-docs.sdk.python.sdk-import]-end


async def main():
    # [developer-docs.sdk.python.client-initialization]-start
    # Gets your service account token from the OP_SERVICE_ACCOUNT_TOKEN environment variable.
    token = os.getenv("OP_SERVICE_ACCOUNT_TOKEN")

    # Connects to 1Password.
    client = await Client.authenticate(
        auth=token,
        # Set the following to your own integration name and version.
        integration_name="My 1Password Integration",
        integration_version="v1.0.0",
    )
    # [developer-docs.sdk.python.client-initialization]-end

    # [developer-docs.sdk.python.list-vaults]-start
    vaults = await client.vaults.list_all()
    async for vault in vaults:
        print(vault.title)
    # [developer-docs.sdk.python.list-vaults]-end

    # [developer-docs.sdk.python.list-items]-start
    items = await client.items.list_all(vault.id)
    async for item in items:
        print(item.title)
    # [developer-docs.sdk.python.list-items]-end

    # [developer-docs.sdk.python.validate-secret-reference]-start
    # Validate secret reference to ensure no syntax errors
    try:
        Secrets.validate_secret_reference("op://vault/item/field")
    except Exception as error:
        print(error)
    # [developer-docs.sdk.python.validate-secret-reference]-end

    # [developer-docs.sdk.python.resolve-secret]-start
    # Retrieves a secret from 1Password. Takes a secret reference as input and returns the secret to which it points.
    value = await client.secrets.resolve("op://vault/item/field")
    print(value)
    # [developer-docs.sdk.python.resolve-secret]-end

    # [developer-docs.sdk.python.create-item]-start
    # Create an Item and add it to your vault.
    to_create = ItemCreateParams(
        title="MyName",
        category=ItemCategory.LOGIN,
        vault_id="7turaasywpymt3jecxoxk5roli",
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
    created_item = await client.items.create(to_create)
    # [developer-docs.sdk.python.create-item]-end

    print(dict(created_item))

    # [developer-docs.sdk.python.resolve-totp-code]-start
    # Retrieves a secret from 1Password. Takes a secret reference as input and returns the secret to which it points.
    code = await client.secrets.resolve(
        f"op://{created_item.vault_id}/{created_item.id}/TOTP_onetimepassword?attribute=totp"
    )
    print(code)
    # [developer-docs.sdk.python.resolve-totp-code]-end

    # [developer-docs.sdk.python.get-totp-item-crud]-start
    # Fetch a totp code from the item
    for f in created_item.fields:
        if f.field_type == "Totp":
            if f.details.content.error_message is not None:
                print(f.details.content.error_message)
            else:
                print(f.details.content.code)
    # [developer-docs.sdk.python.get-totp-item-crud]-end

    # [developer-docs.sdk.python.get-item]-start
    # Retrieve an item from your vault.
    item = await client.items.get(created_item.vault_id, created_item.id)
    # [developer-docs.sdk.python.get-item]-end

    print(dict(item))

    # [developer-docs.sdk.python.update-item]-start
    # Update a field in your item
    item.fields[0].value = "new_value"
    item.websites.append(
        Website(
            label="my custom website 2",
            url="https://example2.com",
            autofill_behavior=AutofillBehavior.NEVER,
        ),
    )
    updated_item = await client.items.put(item)
    # [developer-docs.sdk.python.update-item]-end

    print(dict(updated_item))

    # [developer-docs.sdk.python.generate-pin-password]-start
    pin_password = Secrets.generate_password(
        PasswordRecipePin(parameters=PasswordRecipePinInner(length=8))
    )
    print(pin_password)
    # [developer-docs.sdk.python.generate-pin-password]-end

    # [developer-docs.sdk.python.generate-memorable-password]-start
    memorable_password = Secrets.generate_password(
        PasswordRecipeMemorable(
            parameters=PasswordRecipeMemorableInner(
                separatorType=SeparatorType.UNDERSCORES,
                wordListType=WordListType.SYLLABLES,
                capitalize=False,
                wordCount=3,
            )
        ),
    )
    print(memorable_password)
    # [developer-docs.sdk.python.generate-memorable-password]-end

    # [developer-docs.sdk.python.generate-random-password]-start
    random_password = Secrets.generate_password(
        PasswordRecipeRandom(
            parameters=PasswordRecipeRandomInner(
                length=10,
                includeDigits=False,
                includeSymbols=False,
            )
        ),
    )
    print(random_password)
    # [developer-docs.sdk.python.generate-random-password]-end

    await share_item(created_item.vault_id, updated_item.id, client)

    # [developer-docs.sdk.python.delete-item]-start
    # Delete / archive a item from your vault.
    await client.items.delete(created_item.vault_id, updated_item.id)
    # or to archive: await client.items.archive(created_item.vault_id, updated_item.id)
    # [developer-docs.sdk.python.delete-item]-end

async def share_item(vault_id: str, item_id: str, client: Client):
    # [developer-docs.sdk.python.item-share-get-item]-start
    item = await client.items.get(vault_id, item_id)
    print(item)
    # [developer-docs.sdk.python.item-share-get-item]-end

    # [developer-docs.sdk.python.item-share-get-account-policy]-start
    policy = await client.items.shares.get_account_policy(item.vault_id, item.id)
    print(policy)
    # [developer-docs.sdk.python.item-share-get-account-policy]-end

    # [developer-docs.sdk.python.item-share-validate-recipients]-start
    valid_recipients = await client.items.shares.validate_recipients(
        policy, ["agilebits.com"]
    )

    print(valid_recipients)
    # [developer-docs.sdk.python.item-share-validate-recipients]-end

    # [developer-docs.sdk.python.item-share-create-share]-start
    share_link = await client.items.shares.create(
        item,
        policy,
        ItemShareParams(
            recipients = valid_recipients,
            expireAfter= ItemShareDuration.ONEHOUR,
            oneTimeOnly= False,
        ),
    )

    print(share_link)
    # [developer-docs.sdk.python.item-share-create-share]-end

if __name__ == "__main__":
    asyncio.run(main())
