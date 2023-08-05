# David R Thompson, Adam Erickson

from isofit.isofit import Isofit
from isofit.utils import surfmodel


# Build the surface model
surfmodel("configs/ang20171108t184227_surface.json")

# Run retrievals
model = Isofit("configs/ang20171108t184227_beckmanlawn-libradtran.json")
model.run()
