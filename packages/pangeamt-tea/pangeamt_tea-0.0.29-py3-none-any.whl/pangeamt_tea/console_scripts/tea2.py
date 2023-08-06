import anyio
import asyncclick as click

@click.group(invoke_without_command=True)
@click.pass_context

async def cli(ctx):
    if ctx.invoked_subcommand is None:
        click.echo('I was invoked without subcommand')
    else:
        click.echo('I am about to invoke %s' % ctx.invoked_subcommand)

@cli.command()
async def new(dir, customer, src_lang, tgt_lang, flavor, version):
    '''
    Create a new project
    '''
    click.echo('The subcommand')



def main():
    cli(_anyio_backend="asyncio")  # or asyncio, or curio