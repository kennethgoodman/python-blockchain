from envlib import get_env
from hashlib2 import sha
from json import JSONEncoder
import time
from ecc import check_signature
from Script import ScriptEvaluator
from UTXO import UTXO

class DefaultJSONEncoder(JSONEncoder):
    def default(self):
        return self.__dict__

class Input(DefaultJSONEncoder):
    def __init__(self, input_data, input_tx_hash, input_tx_index):
        self.input_data = input_data
        self.input_tx_hash = input_tx_hash
        self.input_tx_index = input_tx_index
        DefaultJSONEncoder.__init__(self)

    def default(self):
        return self.__dict__

    def __hash__(self):
        x = str(self.input_data) + self.input_tx_hash + self.input_tx_index
        h = sha(x)
        return h

    def default(self):
        return {
            'input_data': self.input_data,
            'input_tx_hash': self.input_tx_hash,
            'input_tx_index': self.input_tx_index,
        }

    @staticmethod
    def from_json(input):
        return Input(eval(input['input_data']), input['input_tx_hash'], input['input_tx_index'])

class Inputs(DefaultJSONEncoder):
    def __init__(self, inputs):
        self.inputs = inputs
        DefaultJSONEncoder.__init__(self)

    def __hash__(self):
        x = list(map(str,map(hash, self.inputs)))
        h = sha(' '.join(x)) 
        return h

    def default(self):
        return list(map(lambda i: i.default(), self.inputs))

class Output(DefaultJSONEncoder):
    def __init__(self, address, amount, script): 
        # 1 = P2PKH
        self.address = address
        self.amount = amount
        self.script = script
        DefaultJSONEncoder.__init__(self)

    def __hash__(self):
        h = sha(self.address + str(self.amount) + str(self.script))
        return h

    def default(self):
        return {'address':self.address, 'amount': self.amount, 'script': self.script}

    @staticmethod
    def from_json(output):
        return Output(output['address'], output['amount'], output['script'])

class Outputs(DefaultJSONEncoder):
    def __init__(self, outputs):
        self.outputs = outputs

    def __hash__(self):
        h = sha(' '.join(map(str, map(hash, self.outputs))))
        return h

    def default(self):
        return list(map(lambda o: o.default(), self.outputs))


class Transaction(DefaultJSONEncoder):
    def __init__(self, inputs, outputs, ts, tx_hash=None):
        self.inputs = inputs
        self.outputs = outputs
        self.ts = ts 
        self.tx_hash = hash(self) if tx_hash is None else tx_hash
        DefaultJSONEncoder.__init__(self)

    def verify(self):
        """
            1. verify transaction is valid:
                a. Funds not already spent
                b. Has rights to send from that output
            2. TX hash is correct
        """
        def verify_not_double_spend():
            """ Call UTXO and make sure it is currently in there """
            print("Have not checked: verify_is_rightful_spender")
            return True  # TODO: this
        
        def verify_is_rightful_spender():
            def verify_input(input):
                """
                    find script, check that is verified
                """
                output_tx = UTXO.get_output_tx(input.input_tx_hash, input.input_tx_index)  # TODO: this
                script = output_tx.script
                script_with_inputs = script.format(**input.input_data)  # TODO: this
                return ScriptEvaluator(script_with_inputs).eval_script()
            return all(map(verify_input, self.inputs))

        def verify_tx_hash():
            return hash(self) == self.tx_hash

        return verify_not_double_spend() and verify_is_rightful_spender() and verify_tx_hash()

    def __hash__(self):
        return sha(self.encode())

    @staticmethod
    def create_coinbase_tx():
        ts = time.time()
        inputs = Inputs( [Input('', '', '', '')] )
        outputs = Outputs( [Output(get_env('my_address',''), 25)] )
        return Transaction(inputs, outputs, ts)

    @staticmethod
    def from_json(transaction_json):
        inputs = Inputs(list(map(Input.from_json, transaction_json['inputs'])))
        outputs = Outputs(list(map(Output.from_json, transaction_json['outputs'])))
        return Transaction(inputs, outputs, transaction_json['timestamp'], transaction_json['tx_hash'])

    def default(self):
       return {
            'inputs': self.inputs.default(),
            'outputs': self.outputs.default(),
            'timestamp': self.ts,
            'tx_hash': self.tx_hash,
       }

    def encode(self):
        return str(hash(self.inputs) + hash(self.outputs) + sha(self.ts)).encode()

def test():
    inputs = [Input('', '', '', '')]
    inputs_o = Inputs(inputs)
    outputs = [Output(my_address, 25)]
    outputs_o = Outputs(outputs)
    tx = Transaction(inputs_o, outputs_o)
    print(tx, tx.tx_hash)
    print(Transaction.create_coinbase_tx().tx_hash)
