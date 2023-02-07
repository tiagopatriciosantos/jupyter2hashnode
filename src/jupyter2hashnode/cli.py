from typing import Optional
import typer
from dotenv import load_dotenv
from jupyter2hashnode import __app_name__, __version__, __author__, __email__, __homepage__
from .jupyter2hashnode import Jupyter2Hashnode
import os

load_dotenv()

app = typer.Typer()


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} {__version__}")
        raise typer.Exit()


@app.command()
def main(notebook_path: str = typer.Argument(..., help="notebook file name or complete path"),
         output_path: Optional[str] = typer.Argument(None, help="output folder name or complete output path where the files will be written to, if none creates output folder with the same name as the notebook file name"),
         jwt: str = typer.Option(None, "--jwt", "-j",
                                   help="JWT token for authentication at https://hashnode.com/api/upload-image."),
         token: str = typer.Option(None, "--token", "-t",
                                     help="Token for authentication at https://api.hashnode.com  mutation createPublicationStory endpoint"),
         publication_id: str = typer.Option(None, "--publication", "-p",
                                              help="ID of the Hashnode publication e.g. https://hashnode.com/<id>/dashboard"),
         title: str = typer.Option(..., help="Article title", prompt="Article title"),
         hide_from_feed:bool=typer.Option(True, help="Hide this article from Hashnode and display it only on your blog"),
         delete_files:bool=typer.Option(True, help="Delete all files after creating the publication story"),
         upload:bool=typer.Option(True, help="Upload the publication story to the Hashnode server"),
         version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
)
) -> None:
    """
    jupyter2hashnode converts the specified Jupyter Notebook to a Hashnode publication story, 
    compressing images, uploading images to the Hashnode server, and replacing image URLs 
    in the markdown file, then published.

    If jwt, token, publication_id arguments not passed then will use environment variables HASHNODE_JWT, HASHNODE_TOKEN, HASHNODE_PUBLICATION_ID. 

    Notes:

    To obtain JWT: Open https://hashnode.com, account must be logged in, open DevTools of chrome browser (F12), go to Application tab, go to Cookies, find and copy value of "jwt" cookie (245 characters)

    To obtain Hashnode API token: Open https://hashnode.com/settings/developer, click on "Generate New Token" button or use the existing one

    To obtain Publication ID: Go to https://hashnode.com/settings/blogs, click "Dashboard" of the blog you want to upload to, copy the ID, e.g. https://hashnode.com/<id>/dashboard
    """

    if len(title)<12:
        typer.echo(f"Title is too short, must be greater than 12 chars!")
        raise typer.Exit()


    if not jwt:
        jwt = os.environ.get("HASHNODE_JWT")
    if not token:
        token= os.environ.get("HASHNODE_TOKEN")
    if not publication_id:
        publication_id = os.environ.get("HASHNODE_PUBLICATION_ID")
        
    
    j2h = Jupyter2Hashnode(jwt, token, publication_id)
    j2h.create_publication_story(title, notebook_path, hide_from_feed, output_path, delete_files, upload)


