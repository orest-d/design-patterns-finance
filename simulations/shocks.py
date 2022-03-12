class ShockMixin:  # Mixin, can be further extended
    def __add__(self, shock):
        return CombinedShock(self, shock)

    def __mul__(self, value):
        return RelativelyScaledShock(value, self)

    def __rmul__(self, value):
        return RelativelyScaledShock(value, self)


class ShockProxy(ShockMixin):  # Proxy
    def __init__(self, shock):
        self.shock = shock

    def __call__(self, scenario):
        return self.shock(scenario)


def rich_shock(f):
    return ShockProxy(f)


@rich_shock
def no_shock(scenario):
    return scenario


@rich_shock  # Python decorator
def danske_100(scenario):
    scenario = {**scenario}
    scenario["CPH:DANSKE"] = 100.0
    return scenario


class RelativelyScaledShock:  # Another proxy
    def __init__(self, scaling_factor, shock):
        self.scaling_factor = scaling_factor
        self.shock = shock

    def __call__(self, scenario):
        shocked_scenario = self.shock(scenario)
        return {
            key: scenario[key]
            + self.scaling_factor * (shocked_scenario[key] - scenario[key])
            for key in scenario.keys()
        }


class CombinedShock:  # Combinator
    def __init__(self, shock1, shock2):
        self.shock1 = shock1
        self.shock2 = shock2

    def __call__(self, scenario):
        scenario = self.shock1(scenario)
        scenario = self.shock2(scenario)
        return scenario


class ScenarioShock(ShockMixin):  # Adapter
    def __init__(self, scenario):
        self.scenario = scenario

    def __call__(self, scenario):
        scenario = {**scenario}
        scenario.update(self.scenario)
        return scenario


def absolute_shock(risk_factor, value):
    @rich_shock
    def do_shock(
        scenario, risk_factor=risk_factor, value=value
    ):  # Be careful about passing parameters
        scenario = {**scenario}
        scenario[risk_factor] = value
        return scenario

    return do_shock

    # alternatively use lambda function
    return lambda shock, risk_factor=risk_factor, value=value: absolute_shock1(
        scenario, risk_factor, value
    )


def relative_shock(risk_factor, value):
    @rich_shock
    def do_shock(
        scenario, risk_factor=risk_factor, value=value
    ):  # Be careful about passing parameters
        scenario = {**scenario}
        scenario[risk_factor] = scenario[risk_factor] * value
        return scenario

    return do_shock
