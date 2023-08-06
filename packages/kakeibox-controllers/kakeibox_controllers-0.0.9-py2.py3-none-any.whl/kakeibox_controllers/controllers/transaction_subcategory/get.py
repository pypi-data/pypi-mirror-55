from kakeibox_controllers.controllers.controller_get_actions \
    import KakeiboxControllerGet
from kakeibox_core.entry_points.commands import commands


class TransactionSubcategoryGet(KakeiboxControllerGet):

    def execute(self, input):
        self.input = input
        self.command = commands.get_subcategory()
        return super(TransactionSubcategoryGet, self).execute()
