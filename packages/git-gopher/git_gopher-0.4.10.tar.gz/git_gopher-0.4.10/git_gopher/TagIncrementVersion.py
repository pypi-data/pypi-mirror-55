from git_gopher.CommandInterface import CommandInterface

class TagIncrementVersion(CommandInterface):
    def __init__(self, hist_command_runer, git_data_getter, version_incrementer):
        self._hist_command_runer = hist_command_runer
        self._git_data_getter = git_data_getter
        self._version_incrementer = version_incrementer

    def run(self):
        most_recent_tag = self._git_data_getter.get_most_recent_tag()
        preview = 'echo "git tag $(ggo-get-incremented-version ' + most_recent_tag + ' {2})"'
        semantic_part = self._git_data_getter.get_semantic_part(preview=preview)
        new_version = self._version_incrementer.increment(most_recent_tag, semantic_part)
        self._hist_command_runer.run(['git', 'tag', new_version])
