import asyncio
import argparse
import os



def main():
    asyncio.run(run())


async def run():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(description='Tea', dest="cmd")

    parser_init = subparser.add_parser("init")
    parser_init.add_argument('-parent_dir', type=str, default=None)
    parser_init.add_argument('-customer', type=str, default=None)
    parser_init.add_argument('-src_lang', type=str, default=None)
    parser_init.add_argument('-tgt_lang', type=str, default=None)
    parser_init.add_argument('-flavor', type=str, default=None)
    parser_init.add_argument('-version', type=str, default=None)

    parser_clean = subparser.add_parser("clean")
    args = parser.parse_args()
    print(vars(args))

    if args.cmd == 'init':
        await cmd_init(

        )




async def cmd_init():
    pass
    # customer = input("Customer: ")
    # src_lang = input("Source language: ")
    # tgt_lang = input("Target language: ")
    # flavor = input("Flavor ")
    #
    # project_dir = customer + '_' + src_lang + '_' + tgt_lang
    # if flavor:
    #     project_dir += '_' + flavor
    # if os.path.isdir(project_dir):
    #     raise ValueError(f'Project {project_dir} already exist\'s')
    #
    # os.mkdir(project_dir)
    # print(f"run `cd {project_dir}`")


if __name__ == '__main__':
    main()