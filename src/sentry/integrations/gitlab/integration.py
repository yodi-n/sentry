from __future__ import absolute_import

from sentry.integrations import Integration
from sentry.integrations.constants import ERR_INTERNAL, ERR_UNAUTHORIZED
from sentry.integrations.exceptions import ApiError
from sentry.models import Repository

API_ERRORS = {
    404: 'Gitlab returned a 404 Not Found error. If this repository exists, ensure'
         ' that your installation has permission to access this repository',
    # ' (https://github.com/settings/installations).',
    401: ERR_UNAUTHORIZED,
}


class GitlabIntegration(Integration):

    def get_client(self):
        return None  # GitlabApiClient()

    def search_issues(self, query):
        return self.get_client().search_issues(query)

    def get_unmigratable_repositories(self):
        accessible_repos = self.get_repositories()
        accessible_repo_names = [r['identifier'] for r in accessible_repos]

        existing_repos = Repository.objects.filter(
            organization_id=self.organization_id,
            provider='gitlab',
        )

        return filter(
            lambda repo: repo.name not in accessible_repo_names,
            existing_repos,
        )

    def reinstall(self):
        self.reinstall_repositories()

    def message_from_error(self, exc):
        if isinstance(exc, ApiError):
            message = API_ERRORS.get(exc.code)
            if message:
                return message
            return (
                'Error Communicating with Gitlab (HTTP %s): %s' % (
                    exc.code, exc.json.get('message', 'unknown error')
                    if exc.json else 'unknown error',
                )
            )
        else:
            return ERR_INTERNAL
