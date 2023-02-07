# Using `jupyter2hashnode` as a command line tool

jupyter2hashnode converts the specified Jupyter Notebook to a Hashnode publication story, 
compressing images, uploading images to the Hashnode server, and replacing image URLs 
in the markdown file, then published.

If jwt, token, publication_id arguments not passed then will use environment variables HASHNODE_JWT, HASHNODE_TOKEN, HASHNODE_PUBLICATION_ID. 

Notes:

To obtain JWT: Open https://hashnode.com, account must be logged in, open DevTools of chrome browser (F12), go to Application tab, go to Cookies, find and copy value of "jwt" cookie (245 characters)

To obtain Hashnode API token: Open https://hashnode.com/settings/developer, click on "Generate New Token" button or use the existing one

To obtain Publication ID: Go to https://hashnode.com/settings/blogs, click "Dashboard" of the blog you want to upload to, copy the ID, e.g. https://hashnode.com/<id>/dashboard

**Usage**:

```console
$ jupyter2hashnode [OPTIONS] NOTEBOOK_PATH [OUTPUT_PATH]
```

**Arguments**:

* `NOTEBOOK_PATH`: notebook file name or complete path  [required]
* `[OUTPUT_PATH]`: output folder name or complete output path where the files will be written to, if none creates output folder with the same name as the notebook file name

**Options**:

* `-j, --jwt TEXT`: JWT token for authentication at https://hashnode.com/api/upload-image.
* `-t, --token TEXT`: Token for authentication at https://api.hashnode.com  mutation createPublicationStory endpoint
* `-p, --publication TEXT`: ID of the Hashnode publication e.g. https://hashnode.com/<id>/dashboard
* `--title TEXT`: Article title  [required]
* `--hide-from-feed / --no-hide-from-feed`: Hide this article from Hashnode and display it only on your blog  [default: True]
* `--delete-files / --no-delete-files`: Delete all files after creating the publication story  [default: True]
* `--upload / --no-upload`: Upload the publication story to the Hashnode server  [default: True]
* `-v, --version`: Show the application's version and exit.
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.


# Using `jupyter2hashnode` as a library

class Jupyter2Hashnode

The Jupyter2Hashnode class is used to convert Jupyter Notebooks to Hashnode publication stories by compressing images, uploading images to the Hashnode server, and replacing image URLs in the markdown file.

Notes:
- To obtain JWT
    1. Open https://hashnode.com, account must be logged in
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

**Usage**:

```console
$ jupyter2hashnode [OPTIONS] HASHNODE_JWT HASHNODE_TOKEN HASHNODE_PUBLICATION_ID
```

**Arguments**:

* `HASHNODE_JWT`: [required]
* `HASHNODE_TOKEN`: [required]
* `HASHNODE_PUBLICATION_ID`: [required]

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.