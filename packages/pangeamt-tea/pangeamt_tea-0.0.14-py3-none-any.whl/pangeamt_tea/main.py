import asyncio
import argparse
import os



def main():
    asyncio.run(run())


async def run():
    parser = argparse.ArgumentParser(description='Tea')
    parser.add_argument(
        'task',
        metavar='task',
        type=str,
        choices=['init'],
        help='The task to execute')


    args = parser.parse_args()
    task = args.task
    if task == 'init':
        await task_init()





async def task_init():
    customer = input("Customer:")
    src_lang = input("Source language:")
    tgt_lang = input("Target language:")
    flavor = input("Flavor")

    project_dir = customer + '_' + src_lang + '_' + tgt_lang
    if flavor:
        project_dir += '_' + flavor
    if os.path.isdir(project_dir):
        raise ValueError(f'Project {project_dir} already exist\'s')

    os.mkdir(project_dir)
    print(f"run `cd {project_dir}`")


if __name__ == '__main__':
    main()