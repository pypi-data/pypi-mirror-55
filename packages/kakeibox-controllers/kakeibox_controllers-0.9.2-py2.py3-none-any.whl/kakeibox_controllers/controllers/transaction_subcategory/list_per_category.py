from kakeibox_controllers.controllers.controller_delete_actions \
    import KakeiboxControllerDelete
from kakeibox_core.entry_points.commands import commands


class TransactionSubcategoryListPerCategory(KakeiboxControllerDelete):

    def execute(self, input):
        self.input = input
        self.command = commands.list_per_category()
        return super(TransactionSubcategoryListPerCategory, self).execute()
