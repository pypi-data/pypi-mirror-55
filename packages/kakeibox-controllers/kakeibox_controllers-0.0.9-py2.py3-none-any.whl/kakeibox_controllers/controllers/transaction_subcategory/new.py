from kakeibox_controllers.controllers.controller_new_actions \
    import KakeiboxControllerNew
from kakeibox_core.entry_points.commands import commands


class TransactionSubcategoryNew(KakeiboxControllerNew):

    def execute(self, input):
        self.input = input
        self.command = commands.new_subcategory()
        return super(TransactionSubcategoryNew, self).execute()
