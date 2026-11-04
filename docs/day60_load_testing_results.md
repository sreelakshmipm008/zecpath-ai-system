# Day 60 - Load Testing Results

## Test Objective
Evaluate repeated resume-scoring execution under a simulated local workload.

## Test Environment
- Local Windows development environment.
- Python virtual environment.
- SentenceTransformer model: all-MiniLM-L6-v2.
- Candidate profiles per batch: 10.

## Test Results
- Simulated batches: 5.
- Total candidate scoring operations: 50.
- Batch 1: 0.4008 seconds.
- Batch 2: 0.0136 seconds.
- Batch 3: 0.0115 seconds.
- Batch 4: 0.0105 seconds.
- Batch 5: 0.0104 seconds.
- Average batch time: 0.0893 seconds.
- Average of batches 2-5: approximately 0.0115 seconds.

## Validation
- Full automated test suite: 244 passed.
- Python compilation check: completed without errors.

## Observations
Repeated scoring benefited from the existing embedding cache. The first batch was slower than subsequent batches, consistent with model initialization and cache warm-up effects.

## Limitations
This was a local simulated workload using repeated scoring of 10 configured candidates. It was not a concurrent-user, network API or production load test. No production throughput or horizontal-scaling claims are made.

## Conclusion
The local test confirms that repeated cached scoring is faster in this workload. Larger datasets and concurrent request testing are recommended before production deployment.
