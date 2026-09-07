import time
from typing import Dict
from packages.logger.logger import logger

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, recovery_timeout: float = 60.0):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failures: Dict[str, int] = {}
        self.last_failure_time: Dict[str, float] = {}
        self.states: Dict[str, str] = {} # CLOSED (healthy), OPEN (blocked), HALF-OPEN (testing)

    def is_available(self, service_name: str) -> bool:
        state = self.states.get(service_name, 'CLOSED')
        if state == 'CLOSED':
            return True
        if state == 'OPEN':
            now = time.time()
            if now - self.last_failure_time.get(service_name, 0) > self.recovery_timeout:
                self.states[service_name] = 'HALF-OPEN'
                logger.info(f'[CIRCUIT] Service {service_name} entered HALF-OPEN state.')
                return True
            return False
        return True # HALF-OPEN

    def record_success(self, service_name: str):
        self.failures[service_name] = 0
        self.states[service_name] = 'CLOSED'

    def record_failure(self, service_name: str, error: str = ''):
        count = self.failures.get(service_name, 0) + 1
        self.failures[service_name] = count
        self.last_failure_time[service_name] = time.time()
        logger.warning(f'[CIRCUIT] Service {service_name} recorded failure #{count}: {error}')
        if count >= self.failure_threshold:
            self.states[service_name] = 'OPEN'
            logger.error(f'[CIRCUIT] Service {service_name} tripped circuit breaker -> OPEN for {self.recovery_timeout}s')

circuit_breaker = CircuitBreaker()
