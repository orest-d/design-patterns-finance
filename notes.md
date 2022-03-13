# Design patterns in finance

* Discuss the pipeline implementations
  - What are the pros and cons?
  - Dependencies vs mental load, fragility and maintainability
* Discuss OOP vs available data types - plasma
  - Strategy - Euler or something else? Scikit algorithms
* Functions and closures instead of OOP - shocks
  - problem, plain python functions - shocks1
  - parametric shocks, functional approach - shocks2
  - callables: shock3
  - shock3: Mixin, Proxy, Decorator, Adapter
  - State - portfolio2a

```
Adapter    A -> B
Decorator  A -> A + something
Proxy      A -> A
State      A(1/2/3) -> A1/A2/A3
Mixin      A -> A + something
Servant    A -> A + Something   - we will not use
Facade     A,B,C,D,E -> F       - will come later
```

* Scenarios and Iterator
  - start simple - use dictionary - scenarios1
  - Pandas, iterator, another adapter - scenarios2
  - Monte Carlo scenarios as an iterator - scenarios3
  - mention iter and comprehension (x for ...) as iterators

* Portfolio - Composite
  - portfolio1

## Exercise
* implement scenarios with pandas, some shocks and portfolio.
* Possibly implement Monte Carlo scenario generator - or just steal the code

* Pricing
  - vanilla options - portfolio 2
  - Note how volatility appeared in Asset, but it is not always well defined
  - parameterize the pricing engine - Bridge - portfolio6
  - other examples -  drawing API, e.g. matplotlib backend, cairo

* Extending portfolio - more patterns, quickly...
  - Null object, object behaving in a very neutral way - portfolio2
  - visitor (short) - portfolio3
  - iterator (again) as an alternative to visitor - portfolio 4
  - some creation patters - "Factory"-like methods/builder, Prototype - portfolio5
  - Nice to have: __str__, __repr__, clone, to_dict, from_dict - kind of Memento
  - JSON and YAML

## Exercise
* improve the portfolio - add some derivative (bond?) and a pricing engine
* don't spend time on visitor, children, to_dict, from_dict
* clone could be nice
 
* Configuration and singleton
  - Singleton is like global variable - and global variables are bad
  - It is ok, if it is overridable in a safe way
  - Classic Singleton config1
  - Class with only class attributes and class methods - config2
  - My favourite - config() function, Lazy Initialization - config3
  - YAML, update_config - config4
  - argparse - config5
  - use to make database connections - config 6
  
* Putting all together - Simulation
  - Simulation initialization - dependency injection
  - Factory methods
  - Builder pattern - see experiment

* Actually - we should vectorize
  - VectorizedSimulation
  - be careful about memory
  - scalability using batches BatchSimulation
  - Timer - RAII (Resource acquisition is initialization (RAII)
  
## Exercise
Make a simulation

* Misc
  - Vectorization over portfolio, Interpreter - dfp1
  - Chain of responsibility - dfp3
  - Finally - pipeline with liquer - if time allows