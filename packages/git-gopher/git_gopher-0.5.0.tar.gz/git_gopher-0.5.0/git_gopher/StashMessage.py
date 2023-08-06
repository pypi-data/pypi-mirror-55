from git_gopher.CommandInterface import CommandInterface

class StashMessage(CommandInterface):
    def __init__(self, hist_command_runer, git_data_getter):
        self._hist_command_runer = hist_command_runer
        self._git_data_getter = git_data_getter

    def run(self):
        stash_message = self._git_data_getter.get_stash_message_from_input('git stash push -m "[your message here]"')

        if stash_message:
            return self._hist_command_runer.run(['git', 'stash', 'push', '-m', stash_message])
