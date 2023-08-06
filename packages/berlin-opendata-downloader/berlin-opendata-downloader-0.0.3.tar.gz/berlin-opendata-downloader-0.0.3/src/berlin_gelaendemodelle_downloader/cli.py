import os
import click

from tqdm import tqdm

from .download import get_subset_links, download_zip
from .file import fix_file_names, write_file_content
from .utils import file_content_2_data_frame, create_directories, compress_data_frame, data_frame_2_file_content


@click.group()
def cli():
    """
    Entrypoint of CLI implementation.
    """


@cli.command()
@click.argument("download_path", type=click.Path(exists=True, dir_okay=True, writable=True))
@click.option("--keep_original", is_flag=True, type=bool, help="Keeps the original files.")
@click.option("--compress", default=0, type=int, help="Indicates how many tiles should be compressed to one.\n\t<= 0 means no compression and automatically keeps the original ones.\n\t2000 have to be divisible by this without remainder.")
def download(download_path: str, keep_original: bool, compress: int):

    # creats all necessary directories
    original_path, compressed_path = create_directories(download_path, keep_original)
    links = get_subset_links()

    if compress <= 0:
        keep_original = True
        
        for link in tqdm(links):

            file_name, file_content = download_zip(link)

            if keep_original:
                write_file_content(original_path, file_name, file_content)

        fix_file_names(download_path)


    elif 2000 % compress == 0:
        for link in tqdm(links):

            file_name, file_content = download_zip(link)

            if keep_original:
                write_file_content(original_path, file_name, file_content)

            data_frame = file_content_2_data_frame(file_content)
            compressed_data_frame = compress_data_frame(data_frame, compress)

            file_content_compressed = data_frame_2_file_content(compressed_data_frame)
            write_file_content(compressed_path, file_name, file_content_compressed)

        fix_file_names(download_path)


    else:
        raise click.BadParameter("Argument 'compress' have to divide 2000 without remainder.")
