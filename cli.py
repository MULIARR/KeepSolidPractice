import typer
import asyncio

from database import db
from constants import Role

app = typer.Typer()


@app.command("set_role")
def set_role(a,  user_id: int, role_name: str):
    """
   update user role via console

    example:
        python cli.py set_role 123 admin
        py -3.11 cli.py set_role 123 admin
    """

    async def run():
        user = await db.user.get_user_by_id(user_id)
        if not user:
            typer.echo(f"User with ID {user_id} not found.")
            raise typer.Exit(code=1)

        valid_roles = [r for r in Role]
        if role_name not in valid_roles:
            typer.echo(f"Invalid role {role_name}. Choose from {valid_roles}")
            raise typer.Exit(code=1)

        await db.user.update_user_role(user_id, Role(role_name))
        typer.echo(f"Updated role for user {user_id} to '{role_name}'")

    asyncio.run(run())


if __name__ == "__main__":
    app()
