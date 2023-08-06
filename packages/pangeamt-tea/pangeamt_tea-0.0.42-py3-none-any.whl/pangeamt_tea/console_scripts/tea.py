import asyncclick as click


@click.group(invoke_without_command=True)
@click.pass_context
async def tea(ctx):
    if ctx.invoked_subcommand is None:
        click.echo('I was invoked without subcommand')
    else:
        click.echo('I am about to invoke %s' % ctx.invoked_subcommand)

# New Project
@tea.command()
@click.option("--customer", "-c", help="Customer name", required=True)
@click.option("--src_lang", "-s", help="Source language", required=True)
@click.option("--tgt_lang", "-t", help="Target language", required=True)
@click.option("--flavor", "-f", default=None, help="Flavor")
@click.option("--version", "-v", default=1, type=click.INT, help="Version")
@click.option("--dir", default=None, help="Directory where the project is created. Default: the current working directory")

# New
async def new(dir, customer, src_lang, tgt_lang, flavor, version):
    '''
    Create a new project
    '''
    click.echo(f'---> Project \n Type: $ cd {dir} ')


# Clean
@tea.workflow.command()
@click.option("--project", "-p", "project_dir", help="The project directory. Default: the current working directory")
async def clean(project_dir):
    '''
    Clean the data.
    '''
    click.echo('---> Done')


def main():
    tea(_anyio_backend="asyncio")  # or asyncio, or curio
