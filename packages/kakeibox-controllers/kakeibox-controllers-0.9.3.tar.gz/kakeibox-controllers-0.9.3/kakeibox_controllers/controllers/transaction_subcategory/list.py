from kakeibox_controllers.controllers.controller_list_actions \
    import KakeiboxControllerList
from kakeibox_core.entry_points.commands import commands


class TransactionSubcategoryList(KakeiboxControllerList):

    def execute(self):
        self.command = commands.list_all_subcategories()
        return super(TransactionSubcategoryList, self).execute()
