from kakeibox_controllers.controllers.controller_update_actions \
    import KakeiboxControllerUpdate
from kakeibox_core.entry_points.commands import commands


class TransactionCategoryUpdate(KakeiboxControllerUpdate):

    def execute(self, code, transaction_category):

        self.input = {
            'code': code, 'transaction_category': transaction_category}
        self.command = commands.update_category()
        return super(TransactionCategoryUpdate, self).execute()
