import xlrd

from ar.loader.WtVariantInfoLoader import WtVariantInfoLoader


class WtManuallyEnterLoader(WtVariantInfoLoader):
    def load(self, variantInput, loader_config):
        distLoader = {
            "code": "0"
        }
        if "customData" in variantInput:
            distLoader.update(variantInput["customData"])
        else:
            pass
        self.data = distLoader
