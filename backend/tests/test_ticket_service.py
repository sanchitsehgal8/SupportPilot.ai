from backend.services.ticket_service import TicketService


class DummyDB:
    def __init__(self):
        self._tables = {'tickets': []}
    def table(self, name):
        class Q:
            def __init__(self, parent, name):
                self.parent = parent
                self.name = name
                self._query = []
            def insert(self, data):
                        self.parent._tables[self.name].append(data)
                        class R:
                            def __init__(self, d):
                                self.data = [d]
                            def execute(self):
                                return self
                        return R(data)
            def select(self, *args, **kwargs):
                class R:
                    def __init__(self, data_list):
                        self.data = data_list
                    def eq(self, a, b):
                        return self
                    def execute(self):
                        return self
                return R(self.parent._tables[self.name])
            def update(self, data):
                class R:
                    def __init__(self, d):
                        self.data = [d]
                    def eq(self, a, b):
                        return self
                    def execute(self):
                        return self
                return R(data)
            def range(self, a, b):
                class R:
                    data = self.parent._tables[self.name][a:b+1]
                    def execute(self):
                        return R
                return R
        return Q(self, name)


def test_create_and_get_ticket():
    db = DummyDB()
    service = TicketService(db)
    res = service.create_ticket('cust_1', 'Test ticket', 'This is a test', 'low')
    assert res['success']
    ticket = service.get_all_tickets()
    assert len(ticket) == 1
