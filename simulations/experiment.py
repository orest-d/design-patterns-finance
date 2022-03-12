from simulation import *
from pricing import PricingEngineWithProxyAndResidual
from shocks import relative_shock
from portfolio import *
from shocks import danske_100, no_shock
import pandas as pd

baseline = Simulation()

modified_pricing = baseline.clone().with_pricing_engine(
    PricingEngineWithProxyAndResidual()
)

banks_minus100bps = relative_shock(NORDEA_TICK, 0.99) #+ relative_shock(DANSKE_TICK, 0.99)

data = []
for shock_name, shock in [
    ("-", no_shock),
    ("Danske Bank = 100", danske_100),
    ("Banks -100bps", banks_minus100bps),
]:
    for model_name, model in [
        ("Baseline", baseline),
        ("Modified pricing", modified_pricing),
    ]:
        model = model.clone().with_shock(shock)
        data.append(
            dict(
                model=model_name,
                shock=shock_name,
                mean_price=model.mean_price,
                volatility=model.price_volatility,
            )
        )

df = pd.DataFrame(data)
df.to_excel("experiment.xlsx")
