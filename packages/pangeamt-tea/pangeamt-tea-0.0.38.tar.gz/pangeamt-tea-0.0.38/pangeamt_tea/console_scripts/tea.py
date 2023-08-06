import asyncclick as click


@click.group(invoke_without_command=True)
@click.pass_context
async def cli(ctx):
    if ctx.invoked_subcommand is None:
        click.echo('I was invoked without subcommand')
    else:
        click.echo('I am about to invoke %s' % ctx.invoked_subcommand)


@cli.command()
@click.option("--dir", default=None, help="Directory where the project is created")
@click.option("--customer", "-c", help="Customer name", required=True)
@click.option("--src_lang", "-s", help="Source language", required=True)
@click.option("--tgt_lang", "-t", help="Target language", required=True)
@click.option("--flavor", "-f",default=None, help="Flavor")
@click.option("--version", "-v",default=1, type=int, help="Version")
async def new(dir, customer, src_lang, tgt_lang, flavor, version):
    '''
    Create a new project
    '''
    print(dir, customer, src_lang, tgt_lang, flavor, version)
    click.echo('The subcommand')

@cli.command()
@click.option("--project", "-p", type="", help="The project directory. Default: the current working directory")
async def clean(dir):
    '''
    Clean the data.
    '''
    click.echo('---> Done')


def main():
    cli(_anyio_backend="asyncio")  # or asyncio, or curio
