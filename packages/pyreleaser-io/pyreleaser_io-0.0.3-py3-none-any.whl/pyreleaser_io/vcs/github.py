import logging
try:
    from github import Github, BadCredentialsException
except ModuleNotFoundError:
    logging.error("github module not avaiable, please install pygithub")
    github = None

logger = logging.getLogger(__name__)


def get_instance(gh_settings):
    driver = None
    if gh_settings:
        token = gh_settings.get("token", False)
        if not token:
            raise RuntimeError("GitHub token not available! - check your settings file")

        # attempt to use the driver - if our token was bad this will blow up
        try:
            g = Github(token)
            g.get_user().id
            driver = g
        except BadCredentialsException as e:
            logger.warning(f"github login error: {e.data}")

    else:
        logging.warning("no github credentials available in settings file...")

    return driver


def add_user_info(project, g):
    user = g.get_user()
    project["author"] = user.name

    # always blank for some reason...
    project["author_email"] = user.email


def project_url(project, g):
    return f"https://github.com/{g.get_user().login}/{project.get('name')}.git"
