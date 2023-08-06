from git_gopher.CommandInterface import CommandInterface
from git_gopher.NoTagsException import NoTagsException

class BranchTag(CommandInterface):
    def __init__(self, hist_command_runer, git_data_getter):
        self._hist_command_runer = hist_command_runer
        self._git_data_getter = git_data_getter

    def run(self):
        try:
            from_tag = self._git_data_getter.get_tag_name(preview='echo "git checkout -b [new_branch_name] {2}"')
        except NoTagsException:
            print("No tags exist for this repository")
            return

        if from_tag:
            new_branch_name = self._git_data_getter.get_branch_name_from_input()
            self._hist_command_runer.run(['git', 'checkout', '-b', new_branch_name, from_tag])
