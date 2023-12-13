from logzero import logger
import toml
from src.faceswap.faceswap_main import faceswap
from src.lipsync.lipsync_main import lipsync
from src.superres.superres_main import superres
class SyncedUp:
    def __init__(self, configs):
        self.configs = configs

    
    def run(self):

        pipeline = self.configs['pipeline']['processes']

        for process in pipeline:

            # convert the name to the function
            process_func = getattr(self, process)

            # run the function
            process_func()
    
    def faceswap(self):
        logger.debug("Running faceswap")
        faceswap(self.configs).run()
        pass

    def lipsync(self):
        logger.debug("Running lipsync")
        lipsync(self.configs).run()
        pass

    def superres(self):
        logger.debug("Running superres")
        superres(self.configs).run()
        pass



if __name__ == "__main__":
    configs = toml.load('config.toml')
    logger.debug("Loaded configs")
    syncedup = SyncedUp(configs)
    syncedup.run()
    