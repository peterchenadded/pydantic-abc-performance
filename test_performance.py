from pydantic import BaseModel
import logging
import time

class MyEntity1Pattern(BaseModel):
    pass

class MyEntity2Pattern(BaseModel):
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
