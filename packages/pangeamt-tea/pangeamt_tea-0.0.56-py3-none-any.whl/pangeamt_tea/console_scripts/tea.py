import asyncclick as click
import os
from pangeamt_tea.project.project import Project
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
@click.option("--dir", default=None, help="Directory where the project is created")
async def new(dir, customer, src_lang, tgt_lang, flavor, version):
    Project.new(customer, src_lang, tgt_lang, dir, version=version, flavor=flavor)
    click.echo(f'---> Project \n Type: $ cd {dir} ')



# Worflow group
@tea.group(invoke_without_command=True)
@click.option('--project')
@click.pass_context
async def workflow(ctx, project):
    ctx.ensure_object(dict)
    if project is None:
        project = os.getcwd()
    project = os.path.abspath(project)
    ctx.obj['project'] = project


# Clean
@workflow.command()
@click.option("--project", "-p", "project_dir", help="The project directory. Default: the current working directory")
@click.pass_context
async def clean(ctx, project_dir):
    '''
    Clean the data.
    '''
    click.echo(ctx.obj['project'])
    click.echo('---> Done')


def main():
    tea(_anyio_backend="asyncio")  # or asyncio, or curio
