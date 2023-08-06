from kakeibox_controllers.controllers.controller_list_actions \
    import KakeiboxControllerList
from kakeibox_core.entry_points.commands import commands


class TransactionCategoryList(KakeiboxControllerList):

    def execute(self):
        self.command = commands.list_categories()
        return super(TransactionCategoryList, self).execute()
