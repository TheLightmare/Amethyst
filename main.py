import git
import os
import shutil

def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

is_first_launch = True
# initialize the Amethyst working directory if it does not exist
if os.path.isdir("Amethyst"):
    is_first_launch = False
else:
    os.mkdir("Amethyst")
    with open("Amethyst/settings.txt", "w") as f:
        f.write("")
    with open("Amethyst/shared_projects.txt", "w") as f:
        f.write("")

# clone the repo if first launch
if is_first_launch :
    repo = git.Repo.clone_from("git@github.com:TheLightmare/Amethyst_projects.git", "Amethyst/temp")
else :
    repo = git.Repo("Amethyst/temp")


with open("Amethyst/shared_projects.txt") as f:
    projects = f.readlines()
for project in projects :
    (name, raw_dirs) = project.split(" ")
    dirs = raw_dirs.split(",")

    if os.path.isdir(name) :
        if os.path.isdir("Amethyst/temp/" + name):
            shutil.rmtree("Amethyst/temp/" + name)
        os.mkdir("Amethyst/temp/" + name)
        for shared_dir in dirs :
            os.mkdir(f"Amethyst/temp/{name}/{shared_dir}")
            copytree(f"{name}/{shared_dir}", f"Amethyst/temp/{name}/{shared_dir}")
        repo.index.add(name.strip() + "/*")
        #we push if we have it
        repo.index.commit("update")
        repo.remotes.origin.push()

repo.remotes.origin.pull()


for dir in os.listdir("Amethyst/temp") :
    for project in projects :
        (name, raw_dirs) = project.split(" ")
        dirs = raw_dirs.split(",")
        if dir == name :
            if not os.path.isdir(dir) :
                os.mkdir(dir)
            copytree("Amethyst/temp/"+dir, dir)