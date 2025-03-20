import asyncio
import os
from pathlib import Path

# [developer-docs.sdk.python.sdk-import]-start
from onepassword import *

# [developer-docs.sdk.python.sdk-import]-end
from cryptography.hazmat.primitives.asymmetric import rsa, ed25519
from cryptography.hazmat.primitives import serialization


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
    await resolve_all_secrets(client,created_item.vault_id, created_item.id, "username", "password")
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

    await share_item(client, created_item.vault_id, updated_item.id)

    await create_ssh_key_item(client)

    await create_and_replace_document_item(client)

    await create_attach_and_delete_file_field_item(client)

    # [developer-docs.sdk.python.delete-item]-start
    # Delete a item from your vault.
    await client.items.delete(created_item.vault_id, updated_item.id)
    # [developer-docs.sdk.python.delete-item]-end


## NOTE: this is in a separate function to avoid creating a new item
## NOTE: just for the sake of archiving it. This is because the SDK
## NOTE: only works with active items, so archiving and then deleting
## NOTE: is not yet possible.
async def archive_item(client: Client, vault_id: str, item_id: str):
    # [developer-docs.sdk.python.archive-item]-start
    # Archive a item from your vault.
    await client.items.archive(vault_id, item_id)
    # [developer-docs.sdk.python.archive-item]-end


async def share_item(client: Client, vault_id: str, item_id: str):
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
            recipients=valid_recipients,
            expireAfter=ItemShareDuration.ONEHOUR,
            oneTimeOnly=False,
        ),
    )

    print(share_link)
    # [developer-docs.sdk.python.item-share-create-share]-end


async def create_ssh_key_item(client: Client):
    # Generate a 2048-bit RSA private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
    )

    # Serialize the private key in PKCS8 format (PEM)
    ssh_key_pkcs8_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    # [developer-docs.sdk.python.create-sshkey-item]-start
    # Create an Item containing SSH Key and add it to your vault.
    to_create = ItemCreateParams(
        title="SSH Key Item Created With Python SDK",
        category=ItemCategory.SSHKEY,
        vault_id="7turaasywpymt3jecxoxk5roli",
        fields=[
            ItemField(
                id="private_key",
                title="private key",
                field_type=ItemFieldType.SSHKEY,
                value=ssh_key_pkcs8_pem,
                sectionId="",
            ),
        ],
        sections=[
            ItemSection(id="", title=""),
        ],
    )
    created_item = await client.items.create(to_create)

    print(created_item.fields[0].value)
    print(created_item.fields[0].details.content.public_key)
    print(created_item.fields[0].details.content.fingerprint)
    print(created_item.fields[0].details.content.key_type)
    # [developer-docs.sdk.python.create-sshkey-item]-end
    await client.items.delete(created_item.vault_id, created_item.id)


async def create_and_replace_document_item(client: Client):
    # [developer-docs.sdk.python.create-document-item]-start
    # Create a Document Item
    to_create = ItemCreateParams(
        title="Document Item Created with Python SDK",
        category=ItemCategory.DOCUMENT,
        vault_id="7turaasywpymt3jecxoxk5roli",
        sections=[
            ItemSection(id="", title=""),
        ],
        document=DocumentCreateParams(
            name="file.txt", content=Path("./example/file.txt").read_bytes()
        ),
    )
    created_item = await client.items.create(to_create)
    # [developer-docs.sdk.python.create-document-item]-end

    # [developer-docs.sdk.python.replace-document-item]-start
    # Replace the document in the item
    replaced_item = await client.items.files.replace_document(
        created_item,
        DocumentCreateParams(
            name="file2.txt", content=Path("./example/file2.txt").read_bytes()
        ),
    )
    # [developer-docs.sdk.python.replace-document-item]-end

    # [developer-docs.sdk.python.read-document-item]-start
    # Read the document in the item
    content = await client.items.files.read(
        replaced_item.vault_id, replaced_item.id, replaced_item.document
    )
    # [developer-docs.sdk.python.read-document-item]-end

    print(content.decode())

    await client.items.delete(replaced_item.vault_id, replaced_item.id)


async def create_attach_and_delete_file_field_item(client: Client):
    # [developer-docs.sdk.python.create-item-with-file-field]-start
    # Create a File Field Item
    to_create = ItemCreateParams(
        title="FileField Item created with Python SDK",
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
        ],
        sections=[
            ItemSection(id="", title=""),
        ],
        files=[
            FileCreateParams(
                name="file.txt",
                content=Path("./example/file.txt").read_bytes(),
                sectionId="",
                fieldId="file_field",
            )
        ],
    )

    created_item = await client.items.create(to_create)
    # [developer-docs.sdk.python.create-item-with-file-field]-end

    # [developer-docs.sdk.python.read-file-field]-start
    # Read the file field from an item
    content = await client.items.files.read(
        created_item.vault_id, created_item.id, created_item.files[0].attributes
    )
    # [developer-docs.sdk.python.read-file-field]-end
    print(content.decode())

    # [developer-docs.sdk.python.attach-file-field-item]-start
    # Attach a file field to the item
    attached_item = await client.items.files.attach(
        created_item,
        FileCreateParams(
            name="file2.txt",
            content=Path("./example/file2.txt").read_bytes(),
            sectionId="",
            fieldId="new_file_field",
        ),
    )
    # [developer-docs.sdk.python.attach-file-field-item]-end

    # [developer-docs.sdk.python.delete-file-field-item]-start
    # Delete a file field from an item
    deleted_file_item = await client.items.files.delete(
        attached_item,
        attached_item.files[1].section_id,
        attached_item.files[1].field_id,
    )
    # [developer-docs.sdk.python.delete-file-field-item]-end

    print(len(deleted_file_item.files))

    await client.items.delete(deleted_file_item.vault_id, deleted_file_item.id)


async def resolve_all_secrets(client: Client, vault_id: str, item_id: str, field_id: str, field_id2: str):
    # [developer-docs.sdk.python.resolve-bulk-secret]-start
    # Retrieves multiple secret from 1Password.
    secrets = await client.secrets.resolve_all([f"op://{vault_id}//{item_id}/{field_id}", f"op://{vault_id}/{item_id}/{field_id2}"])
    for secret in secrets.individual_responses.values():
        if secret.error is not None:
            print(str(secret.error))
        else:
            print(secret.content.secret)
    # [developer-docs.sdk.python.resolve-bulk-secret]-end

if __name__ == "__main__":
    asyncio.run(main())

def generate_special_item_fields():

    # Generate an Ed25519 private key
    private_key = ed25519.Ed25519PrivateKey.generate()

    # Encode the private key into a PEM encoded string. This will be assigned to the item field
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    fields=[
        # Address
        ItemField(
            id="address",
            title="Address",
            field_type=ItemFieldType.ADDRESS,
            value="",
            details=ItemFieldDetailsAddress(type="Address", content=AddressFieldDetails(street="1234 Main St", city="San Francisco", state="CA", zip="94111", country="USA")),
            sectionId="",
        ),
        # Date
        ItemField(
            id="date",
            title="Date",
            field_type=ItemFieldType.DATE,
            section_id="mysection",
            value="1998-03-15",
	    ),
        # MonthYear
        ItemField(
            id="month_year",
            title="Month Year",
            field_type=ItemFieldType.MONTHYEAR,
            section_id="mysection",
            value="03/1998",
	    ),
        # Reference
        ItemField(
            id="Reference",
            title="Reference",
            field_type=ItemFieldType.REFERENCE,
            value="f43hnkatjllm5fsfsmgaqdhv7a",
            sectionId="references"
	    ),
        # TOTP from URL
        ItemField(
            id="onetimepassword",
            title="one-time-password",
            field_type=ItemFieldType.TOTP,
            section_id="totpsection",
            value="otpauth://totp/my-example-otp?secret=jncrjgbdjnrncbjsr&issuer=1Password",
	    ),
        # TOTP from Secret
        ItemField(
            id="onetimepassword",
            title="one-time-password",
            field_type=ItemFieldType.TOTP,
            section_id="totpsection",
            value="jncrjgbdjnrncbjsr",
	    ),
        # SSH key
        # id and title must be "private_key" and "private key", respectively
        ItemField(
            id="private_key",
            title="private key",
            field_type=ItemFieldType.SSHKEY,
            value=private_pem,
            sectionId="",
        ),
    ],