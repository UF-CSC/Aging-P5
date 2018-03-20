from Core.Module import Module

class SkimTreeZMuMuSkimmer(Module):
    def analyze(self,event):
        return event._passZmumusel[0]
