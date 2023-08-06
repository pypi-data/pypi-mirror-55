from kakeibox_controllers.controllers.controller_delete_actions \
    import KakeiboxControllerDelete
from kakeibox_core.entry_points.commands import commands


class TransactionCategoryDelete(KakeiboxControllerDelete):

    def execute(self, input):
        self.input = input
        self.command = commands.delete_category()
        return super(TransactionCategoryDelete, self).execute()
