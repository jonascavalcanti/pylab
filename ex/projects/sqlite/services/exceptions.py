class MemberNotInGroup(Exception):

    def __init__(self, email, group):
        super().__init__(f"user {email} is not in group {group}")


class MemberAlreadyInGroup(Exception):

    def __init__(self, email, group):
        super().__init__(f"user {email} is already in group {group}")


class MemberRequireApproval(Exception):

    def __init__(self, email, group):
        super().__init__(f"user {email} needs a manager/owner approval for group {group}")
