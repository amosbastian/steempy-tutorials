class Transfer():
    def __init__(self, operation, block, timestamp):
        self.account = operation['from']
        self.to = operation['to']
        self.amount = operation['amount']
        self.memo = operation['memo']
        self.block = block
        self.timestamp = timestamp

    def print_operation(self):
        print('\nBlock:', self.block, self.timestamp)
        print('Operation: transfer')
        print('From:', self.account)
        print('To:', self.to)
        print('Amount:', self.amount)
        print('Memo:', self.memo)
        print('')


class Transfer_to_vesting():
    def __init__(self, operation, block, timestamp):
        self.account = operation['from']
        self.to = operation['to']
        self.amount = operation['amount']
        self.block = block
        self.timestamp = timestamp

    def print_operation(self):
        print('\nBlock:', self.block, self.timestamp)
        print('Operation: transfer_to_vesting')
        print('From:', self.account)
        print('To:', self.to)
        print('Amount:', self.amount)
        print('')


class Withdraw_vesting():
    def __init__(self, operation, block, timestamp):
        self.account = operation['account']
        self.vesting_shares = operation['vesting_shares']
        self.block = block
        self.timestamp = timestamp

    def print_operation(self):
        print('\nBlock:', self.block, self.timestamp)
        print('Operation: withdraw_vesting')
        print('Account:', self.account)
        print('Vesting shares:', self.vesting_shares)
        print('')


class Convert():
    def __init__(self, operation, block, timestamp):
        self.owner = operation['owner']
        self.request_id = operation['request_id']
        self.amount = operation['amount']
        self.block = block
        self.timestamp = timestamp

    def print_operation(self):
        print('\nBlock:', self.block, self.timestamp)
        print('Operation: convert')
        print('Owner:', self.owner)
        print('Request ID:', self.request_id)
        print('Amount:', self.amount)
        print('')
