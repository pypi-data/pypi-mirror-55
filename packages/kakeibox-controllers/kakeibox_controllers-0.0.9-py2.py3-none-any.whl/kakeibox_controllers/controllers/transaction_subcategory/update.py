from kakeibox_controllers.controllers.controller_update_actions \
    import KakeiboxControllerUpdate
from kakeibox_core.entry_points.commands import commands


class TransactionSubcategoryUpdate(KakeiboxControllerUpdate):

    def execute(self, code, transaction_subcategory):
        self.input = {
            'code': code, 'transaction_subcategory': transaction_subcategory}
        self.command = commands.update_subcategory()
        return super(TransactionSubcategoryUpdate, self).execute()
