class _State:
    """Mutable state shared across all steps in a scenario.

    context.attribute = value inside a step writes to the step-scope layer,
    which is popped when the step ends.  Mutating an object that lives in the
    scenario-scope layer (set by before_scenario) persists for the whole scenario.
    """
    def __init__(self):
        self.nav_hwnd = None
        self.ar_hwnd = None
        self.payment_hwnd = None
        self.idspay_hwnd = None
        self.customer_edit = None
        self.table = None
        self.existing_ar_handles = set()
        self.service_manager_hwnd = None


def before_scenario(context, scenario):
    context.s = _State()
