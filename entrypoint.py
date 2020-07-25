import os
import subprocess as sp
import glob
from PIL import Image

# GITHUB_EVENT_NAME = os.environ['GITHUB_EVENT_NAME']

# Set repository
# CURRENT_REPOSITORY = os.environ['GITHUB_REPOSITORY']
# TODO: How about PRs from forks?
# TARGET_REPOSITORY = os.environ['INPUT_TARGET_REPOSITORY'] or CURRENT_REPOSITORY
# PULL_REQUEST_REPOSITORY = os.environ['INPUT_PULL_REQUEST_REPOSITORY'] or TARGET_REPOSITORY
# REPOSITORY = PULL_REQUEST_REPOSITORY if GITHUB_EVENT_NAME == 'pull_request' else TARGET_REPOSITORY

# Set branches
# GITHUB_REF = os.environ['GITHUB_REF']
# GITHUB_HEAD_REF = os.environ['GITHUB_HEAD_REF']
# GITHUB_BASE_REF = os.environ['GITHUB_BASE_REF']
# CURRENT_BRANCH = GITHUB_HEAD_REF or GITHUB_REF.rsplit('/', 1)[-1]
# TARGET_BRANCH = os.environ['INPUT_TARGET_BRANCH'] or CURRENT_BRANCH
# PULL_REQUEST_BRANCH = os.environ['INPUT_PULL_REQUEST_BRANCH'] or GITHUB_BASE_REF
# BRANCH = PULL_REQUEST_BRANCH if GITHUB_EVENT_NAME == 'pull_request' else TARGET_BRANCH

# GITHUB_ACTOR = os.environ['GITHUB_ACTOR']
# GITHUB_REPOSITORY_OWNER = os.environ['GITHUB_REPOSITORY_OWNER']


#################
GITHUB_TOKEN = os.environ['INPUT_GITHUB_TOKEN']


MAX_HEIGHT_WIDTH = os.environ['INPUT_BASE_HEIGHT_WIDTH'] or "500"
INPLACE = os.environ['INPUT_INPLACE'] or False

################################
# INPLACE = True
# MAX_HEIGHT_WIDTH =500
def commit_changes():
    """Commits changes.
    """
    set_email = 'git config --local user.email "custom-thumbnail@master"'
    set_user = 'git config --local user.name "custom-thumbnail"'

    sp.call(set_email, shell=True)
    sp.call(set_user, shell=True)

    git_checkout = f'git checkout {TARGET_BRANCH}'
    git_add = f'git add .'
    git_commit = 'git commit -m "Action: Images resized"'
    print('Committing reports.......')

    sp.call(git_checkout, shell=True)
    sp.call(git_add, shell=True)
    sp.call(git_commit, shell=True)


def push_changes():
    """Pushes commit.
    """
    set_url = f'git remote set-url origin https://x-access-token:{GITHUB_TOKEN}@github.com/{TARGET_REPOSITORY}'
    git_push = f'git push origin {TARGET_BRANCH}'
    sp.call(set_url, shell=True)
    sp.call(git_push, shell=True)


def main():

    # Recusrively get all the image files (jpg,jpeg,png)

    result = []
    for name in glob.glob('./**/*.png',recursive = True): 
        result.append(name) 

    for name in glob.glob('./**/*.jpg',recursive = True): 
        result.append(name) 

    for name in glob.glob('./**/*.jpeg',recursive = True): 
        result.append(name) 
  

    max_height_width = int(MAX_HEIGHT_WIDTH)
    size = max_height_width,max_height_width
    import os
    if not os.path.exists('./.thumbnails'):
        os.makedirs('./.thumbnails')
    for entry in result:

        out_file = os.path.basename(entry)
        file_name = os.path.splitext(entry)[0]
        file_ext = os.path.splitext(entry)[1]
        try:
            im = Image.open(entry)
            im.thumbnail(size,Image.ANTIALIAS)
            if INPLACE==True:
                im.save(entry)
                print(f"wrote:  {entry} ----> {entry}")
            else:
                out_path = os.path.abspath(f"./.thumbnails/{out_file}")
                # out_path = os.path.abspath(os.path.join(os.getcwd(),"..",".thumb",out_file))
                im.save(out_path)
                print(f"wrote:  {entry} ----> {out_path}")


        except IOError:
            print(f" can not create thumbnail for {entry} Error: {IOError}")



#     commit_changes()
#     push_changes()


if __name__ == '__main__':
    main()