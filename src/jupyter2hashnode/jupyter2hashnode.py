import os
import requests
from nbconvert import MarkdownExporter
from traitlets.config import Config
from nbconvert.writers import FilesWriter
import shutil
from typing import Optional
import json
from PIL import Image
from .hashnode import HashnodePoster


class Jupyter2Hashnode():
    """
    class Jupyter2Hashnode

    The Jupyter2Hashnode class is used to convert Jupyter Notebooks to Hashnode publication stories by compressing images, uploading images to the Hashnode server, and replacing image URLs in the markdown file.

    Notes:
    - To obtain JWT
        1. Open https://hashnode.com
        2. Open DevTools of chrome browser (F12)
        3. Go to Application tab
        4. Go to Cookies
        5. Find and copy value of "jwt" cookie (245 characters)
    - To obtain Hashnode API token
        1. Open https://hashnode.com/settings/developer
        2. Click on "Generate New Token" button or use the existing one
    - To obtain Publication ID
        1. Go to https://hashnode.com/settings/blogs
        2. Click on "Dashboard" button of the blog you want to upload to
        3. Copy ID from the URL, e.g. https://hashnode.com/<id>/dashboard
    - 

    Attributes:
    HASHNODE_JWT (str): JWT token for authentication with the Hashnode image uploader, https://hashnode.com/api/upload-image.
    HASHNODE_TOKEN (str): Token for authentication with the Hashnode server, to use https://api.hashnode.com  mutation createPublicationStory endpoint
    HASHNODE_PUBLICATION_ID (str): ID of the Hashnode publication e.g. https://hashnode.com/<id>/dashboard
    Methods:
    create_publication_story(title:str, notebook_path: str, output_path:Optional[str]=None, delete_files:bool=True, upload:bool=True):
    Creates a publication story on the Hashnode blog platform by converting a Jupyter Notebook to a markdown file, compressing images, uploading images to the Hashnode server, and replacing image URLs in the markdown file.
    """
    def __init__(self, HASHNODE_JWT:str, HASHNODE_TOKEN:str, HASHNODE_PUBLICATION_ID:str):
        self.JWT = HASHNODE_JWT
        self.HASHNODE_TOKEN = HASHNODE_TOKEN
        self.HASHNODE_PUBLICATION_ID = HASHNODE_PUBLICATION_ID


    def create_publication_story(self, title:str, notebook_path: str, hide_from_feed:bool=True, output_path:Optional[str]=None, delete_files:bool=True , upload:bool=True):
        """
        create_publication_story(title:str, notebook_path: str, output_path:Optional[str]=None, delete_files:bool=True, upload:bool=True)

        This function is used to create a publication story on the Hashnode blog platform by converting a Jupyter Notebook to a markdown file, compressing images, uploading images to the Hashnode server, and replacing image URLs in the markdown file.

        Parameters:
        title (str): Title of the publication story.
        notebook_path (str): Path to the Jupyter Notebook file.
        hide_from_feed (bool): Hide this article from Hashnode and display it only on your blog, Default is True.
        output_path (str, optional): Path to the output directory. Default is None.
        delete_files (bool, optional): Boolean value indicating whether to delete all files after creating the publication story. Default is True.
        upload (bool, optional): Boolean value indicating whether to upload the publication story to the Hashnode server. Default is True.

        Returns:
        None
        """
        path = None
        try:
            print("Starting the publication...")
            doc_basename = os.path.splitext(os.path.basename(notebook_path))[0]
            if not output_path and len(str(output_path))>0:
                output_path= "md_"+doc_basename
            print("Creating markdown file at", output_path,"...")
            path, md_file = self._create_markdown_files(notebook_path,doc_basename, output_path)
            print("Compressing and uploading images from ", path,"...")
            images_filenames = self._get_images_filename(path)
            self._compress_images(path, images_filenames)
            image_url_dict = self._upload_images(path, images_filenames)
            file_path =os.path.join(path, md_file)
            self._replace_image_url(file_path, image_url_dict )
            if upload:
                print("Story publication from file", file_path, f" with the title '{title}'...")
                self._create_publication_story(file_path, title, hide_from_feed)
        finally:
            # when finished deletes all files
            if delete_files and path:
                self._delete_path(path)


    def _create_publication_story(self, file_path, title, hide_from_feed=True):

        with open(file_path, "r") as file:
            content = file.read()

        tags = ["python", "linearprogramming", "tutorial", "datascience"]

        hasnode = HashnodePoster(self.HASHNODE_TOKEN)

        response = hasnode.create_post_hashnode(
            title,
            content,
            self.HASHNODE_PUBLICATION_ID,
            tags,
            hide_from_feed=hide_from_feed
        )
        code = response["data"]["code"]
        message = response["data"]["message"]
        cuid = response["data"]["createPublicationStory"]["post"]["cuid"]

        print(f"{code}: {message}")
        print(f"Hashnode Post URL: https://hashnode.com/edit/{hashnode_url}")
        



    def _get_images_filename(self, path):
        files = os.listdir(path)
        extensions = {".jpg", ".png", ".gif"}
        # stores the filename and extension of files thar contains specific extensions
        images = {file: os.path.splitext(file)[1][1:] for file in files if os.path.splitext(file)[1] in  extensions}
        return images


    def _replace_image_url(self, file_path, image_url_dict):
        with open(file_path, 'r') as file:
            content = file.read()
        for k, v in image_url_dict.items():
            content = content.replace(k, v)
        with open(file_path, 'w') as file:
            file.write(content)
    

    def _compress_images(self, path, images_filename):
        for filename, extension in images_filename.items():
            image_full_path = os.path.join(path, filename)
            with Image.open(image_full_path) as image:
                a=image.convert("P")
                a.save(image_full_path,optimize=True)

    def _upload_images(self, path, images_filename):
        image_url_dict = {}
        for filename, extension in images_filename.items():
            image_full_path = os.path.join(path, filename)

            meta_res = requests.get(f"https://hashnode.com/api/upload-image?imageType={extension}", headers={"cookie": f"jwt={self.JWT}"})
            if meta_res.status_code != 200:
                raise Exception("Failed to get metadata")

            meta = json.loads(meta_res.text)
            url = meta["url"]
            fields = meta["fields"]

            files = {"file": open(image_full_path, "rb")}
            upload_res = requests.post(url, data=fields, files=files)
            if upload_res.status_code != 204:
                raise Exception(f"Upload failed for file {filename}")

            image_cdn_url = f"https://cdn.hashnode.com/{fields['key']}"
            image_url_dict[filename]=image_cdn_url
        return image_url_dict



    def _create_markdown_files(self, notebook_path, doc_basename, output_path):
        c = Config()
        base_template = "hashnode"
        dirname, _ = os.path.split(os.path.abspath(__file__))
        template_path =os.path.join(dirname, "nbconvert", "templates", base_template)

        c.TemplateExporter.extra_template_basedirs.append(template_path)
        c.TemplateExporter.template_name=template_path
        # Load notebook from path
        exporter = MarkdownExporter(config=c)
        (output, resources) = exporter.from_filename(notebook_path)

        # Employ nbconvert.writers.FilesWriter to write the markdown file 
        c.FilesWriter.build_directory = output_path
        fw = FilesWriter(config=c)
        
        fw.write(output, resources, notebook_name=doc_basename)

        return output_path, doc_basename+".md"


    def _delete_path(self, path):
        # Check Folder is exists or Not
        if os.path.exists(path):
            # Delete Folder code
            shutil.rmtree(path)
