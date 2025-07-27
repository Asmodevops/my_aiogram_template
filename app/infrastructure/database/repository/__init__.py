from .users import UserRepository

REPOSITORIES = {
    "user_repo": UserRepository,
}


def init_repositories(session):
    return {name: repo_class(session) for name, repo_class in REPOSITORIES.items()}


__all__ = ["init_repositories", "UserRepository"]
