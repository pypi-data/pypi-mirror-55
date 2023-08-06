from kakeibox_controllers.controllers.controller_new_actions \
    import KakeiboxControllerNew
from kakeibox_core.entry_points.commands import commands


class TransactionCategoryNew(KakeiboxControllerNew):

    def execute(self, input):
        self.input = input
        self.command = commands.new_category()
        return super(TransactionCategoryNew, self).execute()
