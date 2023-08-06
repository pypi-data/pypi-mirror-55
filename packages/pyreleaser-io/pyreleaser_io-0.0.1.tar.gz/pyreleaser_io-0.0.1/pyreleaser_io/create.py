import logging
import pyreleaser_io.vcs.github
import pyreleaser_io.vcs.missing
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

vcs = {
    "github": pyreleaser_io.vcs.github,
    "none": pyreleaser_io.vcs.missing
}


def get_vcs(settings):
    driver = False
    _module = None
    for name, module in vcs.items():
        logger.debug(f"trying to setup VCS {name}")
        _module = module
        driver = module.get_instance(settings.get(name, {}))
        if driver:
            logger.debug(f"got a VCS driver! {name}")
            break

    return _module, driver


def interactive(settings):
    vcs_module, vcs_driver = get_vcs(settings)

    print("Lets make something...")
    project = {}
    project["name"] = input("project name? ")

    default_project_url = vcs_module.project_url(project, vcs_driver)
    default_description = "I'll add this later..."
    project["url"] = input(f"Project URL? [{default_project_url}]") or default_project_url
    project["description"] = input(f"Project description? [{default_description}]") or default_description

    vcs_module.add_user_info(project, vcs_driver)

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
