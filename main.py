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

if os.path.isdir("Amethyst"):
    is_first_launch = False
else:
    os.mkdir("Amethyst")
    with open("Amethyst/settings.txt", "w") as f:
        f.write("")
    with open("Amethyst/shared_projects.txt", "w") as f:
        f.write("")


if is_first_launch :
    repo = git.Repo.clone_from("git@github.com:TheLightmare/Amethyst_projects.git", "Amethyst/temp")
else :
    repo = git.Repo("Amethyst/temp")


with open("Amethyst/shared_projects.txt") as f:
    projects = f.readlines()
for project in projects :
    if os.path.isdir(project.strip()) :
        shutil.rmtree("Amethyst/temp/" + project.strip())
        os.mkdir("Amethyst/temp/" + project.strip())
        copytree(project.strip(), "Amethyst/temp/"+project.strip())
        repo.index.add(project.strip() + "/*")

repo.index.commit("update")
repo.remotes.origin.push()
repo.remotes.origin.pull()

for dir in os.listdir("Amethyst/temp") :
    for project in projects :
        if dir == project :
            if not os.path.isdir(dir) :
                os.mkdir(dir)
            copytree("Amethyst/temp/"+dir, dir)