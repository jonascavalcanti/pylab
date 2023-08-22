from .group import Group

class SyncData:
    def __init__(self):
        self.gws_groups: [Group] = []
        self.gh_groups: [Group] = []
        self.email_gh_usernames: [dict] = []
        self.root_gh_team_id = ""
        self.root_custom_gh_team_id = ""
        self.gh_pending_invites = []
        self.gh_legacy_inactive_users = []
