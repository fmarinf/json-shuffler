import json
import random
import mmap

class ShuffleJSON:
    
    def __init__(self, input_file, batch_size=None):
        self.input_file = input_file
        self.batch_size = batch_size
    
    def shuffle_json(self):
        
        with open(self.input_file, 'r') as file_obj:
            with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_READ) as file_map:
                file_content = file_map.read().decode('utf-8')
                data = json.loads('[' + file_content.replace('\n', ',\n') + ']')
        
        if self.batch_size is None or self.batch_size <= 0:
            self.batch_size = len(data)
        else:
            self.batch_size = min(self.batch_size, len(data))
        
        random.shuffle(data)
        
        with open(self.input_file, 'w') as f:
            if self.batch_size == len(data):
                json.dump(data, f, indent=4)
            else:
                batches = [data[i:i+self.batch_size] for i in range(0, len(data), self.batch_size)]
                for i, batch in enumerate(batches):
                    if i > 0:
                        f.write('\n')
                    json.dump(batch, f, indent=4)
        
        return len(data)