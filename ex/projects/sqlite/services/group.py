from shared import parallel, Const, SyncAction

class Group:
    def __init__(self, email="", name="", group_id=""):
        self.id = group_id
        self.name = name
        self.email = email
        self.users = []
        self.sync_action = SyncAction.NONE
        self.parent = ""
        self.pattern_verified = False

    @staticmethod
    def from_gws_group(gws_group):
        group = Group(email=gws_group["email"], name=gws_group["email"].split("@")[0], group_id=gws_group["id"])
        group.pattern_verified = group.name.lower().startswith(Const.GROUP_PREFIXES) \
            and group.name.lower().lower().endswith(Const.GROUP_SUFFIX)
        return group

    @staticmethod
    def from_gws_groups(gws_groups):
        result = parallel.execute(
            method=Group.from_gws_group,
            args_list=[{'gws_group': gws_group} for gws_group in gws_groups])

        if result.has_errors():
            raise Exception('User data normalization failed.')

        groups = []
        for result in result.results:
            groups.append(result)

        return groups

    @staticmethod
    def from_gh_team(gh_group):
        group = Group(group_id=gh_group["id"], name=gh_group["slug"])
        group.parent = gh_group["parent"]["slug"] if gh_group["parent"] is not None else ""
        group.pattern_verified = group.name.lower().startswith(Const.GROUP_PREFIXES) \
            and group.name.lower().lower().endswith(Const.GROUP_SUFFIX)
        return group

    @staticmethod
    def from_gh_teams(gh_groups):
        result = parallel.execute(
            method=Group.from_gh_team,
            args_list=[{'gh_group': gh_group} for gh_group in gh_groups ])
        if result.has_errors():
            raise Exception('User data normalization failed.')

        users = []
        for result in result.results:
            users.append(result)

        return users
