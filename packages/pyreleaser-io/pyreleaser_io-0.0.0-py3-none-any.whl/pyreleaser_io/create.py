import logging
import pyreleaser_io.github
import pyreleaser_io.template
import pyreleaser_io.util
import os

logger = logging.getLogger(__name__)

layouts = {
    "simple": [
        "MANIFEST.in.jinja2",
        "README.md.jinja2",
        "setup.py.jinja2"
    ]
}


def interactive(settings):
    print("Lets make something...")
    project = {}
    project["name"] = input("project name? ")

    g = pyreleaser_io.github.get_instance(settings.get("github"))
    default_project_url = pyreleaser_io.github.project_url(project, g)
    default_description = "I'll add this later..."
    project["url"] = input(f"Project URL? [{default_project_url}]") or default_project_url
    project["description"] = input(f"Project description? [{default_description}]") or default_description

    pyreleaser_io.github.add_user_info(project, g)

    create_project(project)


def simple_skeleton(project):
    project_name = project.get("name")
    project_src = os.path.join(project_name, project_name)
    init_py = os.path.join(project_src, "__init__.py")

    os.mkdir(project_name)
    for template_file in layouts.get("simple"):
        pyreleaser_io.template.render_to_file(
            template_file,
            target_dir=project_name,
            project=project
        )
    os.mkdir(project_src)
    open(init_py, "a").close()

    pwd = os.getcwd()
    os.chdir(project_name)
    pyreleaser_io.util.run("pipenv install -e .")
    os.chdir(pwd)

    print("all done!")


def create_project(project):
    project_name = project.get("name")
    if os.path.isdir(project_name):
        logger.error(f"Already exists: {project_name}")
    else:
        logger.info("Creating project...")
        simple_skeleton(project)
