import giga

class NotImplementedFor(ValueError):

  def __init__(self, platform):
    super().__init__(f'Config not implemented for {platform}')
