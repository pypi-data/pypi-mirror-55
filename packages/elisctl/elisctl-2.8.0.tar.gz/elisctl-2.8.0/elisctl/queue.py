from typing import Optional, Dict, Any, List, Tuple

import click
from tabulate import tabulate

from elisctl import argument, option
from elisctl.lib import INBOXES, WORKSPACES, SCHEMAS, USERS, WEBHOOKS, generate_secret
from elisctl.lib.api_client import ELISClient, get_json

locale_option = click.option(
    "--locale",
    type=str,
    help="Document locale - passed to the Data Extractor, may influence e.g. date parsing.",
)


@click.group("queue")
def cli() -> None:
    pass


@cli.command(name="create", help="Create queue.")
@click.argument("name")
@option.schema_content(required=True)
@option.email_prefix
@option.bounce_email
@option.workspace_id
@option.connector_id
@locale_option
@option.webhook_id
@click.pass_context
def create_command(
    ctx: click.Context,
    name: str,
    schema_content: List[dict],
    email_prefix: Optional[str],
    bounce_email: Optional[str],
    workspace_id: Optional[int],
    connector_id: Optional[int],
    webhook_id: Optional[Tuple[int, ...]],
    locale: Optional[str],
) -> None:
    if email_prefix is not None and bounce_email is None:
        raise click.ClickException("Inbox cannot be created without specified bounce email.")

    with ELISClient(context=ctx.obj) as elis:
        workspace_url = elis.get_workspace(workspace_id)["url"]
        connector_url = (
            get_json(elis.get(f"connectors/{connector_id}"))["url"]
            if connector_id is not None
            else None
        )

        webhooks_urls = []
        if webhook_id:
            for webhook in webhook_id:
                webhook_url = get_json(elis.get(f"webhooks/{webhook}"))["url"]
                webhooks_urls.append(webhook_url)

        schema_dict = elis.create_schema(f"{name} schema", schema_content)
        queue_dict = elis.create_queue(
            name, workspace_url, schema_dict["url"], connector_url, webhooks_urls, locale
        )

        inbox_dict = {"email": "no email-prefix specified"}
        if email_prefix is not None:
            inbox_dict = elis.create_inbox(
                f"{name} inbox", email_prefix, bounce_email, queue_dict["url"]
            )
    click.echo(f"{queue_dict['id']}, {inbox_dict['email']}")


@cli.command(name="list", help="List all queues.")
@click.pass_context
def list_command(ctx: click.Context,) -> None:
    with ELISClient(context=ctx.obj) as elis:
        queues = elis.get_queues((WORKSPACES, INBOXES, SCHEMAS, USERS, WEBHOOKS))

    table = [
        [
            queue["id"],
            queue["name"],
            str(queue["workspace"].get("id", "")),
            queue["inbox"].get("email", ""),
            str(queue["schema"].get("id", "")),
            ", ".join(str(q.get("id", "")) for q in queue["users"]),
            queue["connector"],
            ", ".join(str(q.get("id", "")) for q in queue["webhooks"]),
        ]
        for queue in queues
    ]

    click.echo(
        tabulate(
            table,
            headers=[
                "id",
                "name",
                "workspace",
                "inbox",
                "schema",
                "users",
                "connector",
                "webhooks",
            ],
        )
    )


@cli.command(name="delete", help="Delete a queue.")
@argument.id_
@click.confirmation_option(
    prompt="This will delete ALL DOCUMENTS in the queue. Do you want to continue?"
)
@click.pass_context
def delete_command(ctx: click.Context, id_: int) -> None:
    with ELISClient(context=ctx.obj) as elis:
        queue = elis.get_queue(id_)
        elis.delete({queue["id"]: queue["url"]})


@cli.command(name="change", help="Change a queue.")
@argument.id_
@option.name
@option.schema_content
@option.connector_id
@option.email_prefix
@option.bounce_email
@option.webhook_id
@locale_option
@click.pass_context
def change_command(
    ctx: click.Context,
    id_: int,
    name: Optional[str],
    schema_content: Optional[List[dict]],
    email_prefix: Optional[str],
    bounce_email: Optional[str],
    connector_id: Optional[int],
    webhook_id: Optional[Tuple[int, ...]],
    locale: Optional[str],
) -> None:

    if (email_prefix or bounce_email) and not (email_prefix and bounce_email):
        raise click.ClickException(
            "Inbox cannot be created or updated without both bounce email and email prefix specified."
        )

    if not any(
        [name, schema_content, email_prefix, bounce_email, connector_id, locale, webhook_id]
    ):
        return

    data: Dict[str, Any] = {}

    if name is not None:
        data["name"] = name

    if locale is not None:
        data["locale"] = locale

    with ELISClient(context=ctx.obj) as elis:
        if email_prefix and bounce_email:
            queue_dict = elis.get_queue(id_)
            if not queue_dict["inbox"]:
                inbox_dict = elis.create_inbox(
                    f"{name or queue_dict['name']} inbox",
                    email_prefix,
                    bounce_email,
                    queue_dict["url"],
                )
                click.echo(
                    f"{inbox_dict['id']}, {inbox_dict['email']}, {inbox_dict['bounce_email_to']}"
                )
            else:
                email = f"{email_prefix}-{generate_secret(6)}@elis.rossum.ai"
                inbox_data = {"email": email, "bounce_email_to": bounce_email}
                _, inbox_id = queue_dict["inbox"].rsplit("/", 1)
                elis.patch(f"inboxes/{inbox_id}", inbox_data)

        if connector_id is not None:
            data["connector"] = get_json(elis.get(f"connectors/{connector_id}"))["url"]

        if webhook_id:
            webhooks_urls = []
            for webhook in webhook_id:
                webhook_url = get_json(elis.get(f"webhooks/{webhook}"))["url"]
                webhooks_urls.append(webhook_url)
                data["webhooks"] = webhooks_urls

        if schema_content is not None:
            name = name or elis.get_queue(id_)["name"]
            schema_dict = elis.create_schema(f"{name} schema", schema_content)
            data["schema"] = schema_dict["url"]

        if data:
            elis.patch(f"queues/{id_}", data)
