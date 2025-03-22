from pydantic import BaseModel
from pydantic._internal._model_construction import ModelMetaclass
from typing import Any
import logging
import time

class MyModelMetaclass(ModelMetaclass):
    def __instancecheck__(self, instance: Any) -> bool:
        """Override ABC logic to disable caching causing memory and performance issues."""
        if not hasattr(instance, '__pydantic_decorators__'):
            return False
        return self in instance.__class__.__mro__

class MyBaseModel(BaseModel, metaclass=MyModelMetaclass):
    pass

class MyEntity1Pattern(MyBaseModel):
    pass

class MyEntity2Pattern(MyBaseModel):
    pass

  
def _get_my_entity1_pattern():
    class MyTest1(MyEntity1Pattern):
        pass
    
    return MyTest1
  
def _get_my_entity2_pattern():
    class MyTest2(MyEntity2Pattern):
        pass
    
    return MyTest2

class Measurement(BaseModel):
    my_entity_1_pattern_check: float = 0
    my_entity_2_pattern_check: float = 0
    success: int = 0
    failed: int = 0

    def count(self, input: bool) -> None:
        if input:
            self.success += 1
        else:
            self.failed += 1
    
def test_performance():
    my_objects = []
    logging.info("Started getting objects to check")
    for i in range(10000):
        if i % 2 == 0:
            my_objects.append(_get_my_entity1_pattern()())
        else:
            my_objects.append(_get_my_entity2_pattern()())
    
    logging.info("Completed len(my_objects) = %d", len(my_objects)) 
    logging.info("Started checking objects")

    measurement = Measurement()
    for m in my_objects:
        start = time.time()
        measurement.count(isinstance(m, MyEntity1Pattern))
        measurement.my_entity_1_pattern_check += time.time() - start

        start = time.time()
        measurement.count(isinstance(m, MyEntity2Pattern))
        measurement.my_entity_2_pattern_check += time.time() - start

    logging.info("Completed checking classes")
    logging.info("measures:\n%s", measurement.model_dump_json(indent=4))
