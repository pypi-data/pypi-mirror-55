import yaml
from autoclass import autoclass
import os

@autoclass
class Config:
    def __init__(self,
                 project_dir: str,
                 customer: str,
                 src_lang: str,
                 tgt_lang: str,
                 flavor=None,
                 version=1,
                 processors=[],
                 truecaser=None,
                 tokenizer=None,
                 bpe=None,
                 trainer=None
                 ):
        pass

    @staticmethod
    def load(project_dir):
        with open(os.path.join(project_dir, 'config.yml'), "r") as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
        return Config(project_dir,
                      data['customer'],
                      data['srcLang'],
                      data['tgtLang'],
                      data['flavor'],
                      data['version'],
                      data['version'],
                      data['processors'],
                      data['tokenizer']
                      )

    def save(self):
        with open(os.path.join(self.project_dir, 'config.yml'), "w") as file:
            data = {'customer': self.customer,
                    'srcLang': self.src_lang,
                    'tgtLang': self.tgt_lang,
                    'flavor': self.flavor,
                    'version': self.version,
                    'processors': self.processors,
                    'tokenizer': self.tokenizer,
                    'truecaser': self.truecaser,
                    'bpe': self.bpe,
                    'trainer': self.trainer
                    }

            yaml.dump(data, file,  sort_keys=False)
