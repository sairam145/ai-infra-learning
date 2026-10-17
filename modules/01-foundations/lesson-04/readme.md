# Lesson 04: ML Frameworks — PyTorch Fundamentals for AI Infrastructure Engineers

## 1. Overview

Machine Learning (ML) frameworks provide the software libraries required to load, execute, train, and optimize machine learning models.

For an AI Infrastructure Engineer, understanding ML frameworks is important because deploying an AI application involves more than creating containers, provisioning infrastructure, and configuring Kubernetes. The model must also load correctly, execute efficiently, use available hardware properly, and respond to requests within acceptable latency and resource limits.

This lesson focuses on PyTorch fundamentals and demonstrates how model loading, inference configuration, batching, warm-up, benchmarking, and quantization affect model-serving performance.

The goal is not to become a machine learning researcher. The goal is to understand the model runtime well enough to deploy, troubleshoot, monitor, scale, and optimize AI workloads in production.

## 2. Learning Objectives

By completing this lesson, I learned how to:

- Understand the role of ML frameworks in AI infrastructure.
- Explain the difference between model architecture, model weights, and model artifacts.
- Load a pretrained model and tokenizer from Hugging Face.
- Understand PyTorch `state_dict` and model checkpoint management.
- Configure a model for inference using `eval()` and `torch.no_grad()`.
- Understand CPU and GPU device placement.
- Compare inference performance across different batch sizes.
- Understand model warm-up and its effect on first-request latency.
- Benchmark model inference performance.
- Save model weights and understand checkpoint size.
- Apply dynamic INT8 quantization to supported model layers.
- Compare FP32 and INT8 model sizes and inference latency.
- Interpret deprecation warnings and distinguish warnings from execution failures.
- Connect ML framework concepts to containerization, Kubernetes, AWS infrastructure, monitoring, and cost optimization.

## 3. Why ML Frameworks Matter for AI Infrastructure Engineers

In traditional cloud infrastructure, the primary responsibilities often include provisioning compute, networking, storage, security, deployment automation, monitoring, and scaling.

AI infrastructure adds another important component: the model runtime.

An AI application may use PyTorch to load and execute a trained model inside a container. Even when the container is running and Kubernetes reports the pod as healthy, the model may fail to load, consume excessive memory, run on the wrong device, or respond too slowly.

Understanding ML frameworks helps infrastructure engineers investigate these problems instead of treating the model as a black box.

### Common production scenarios

| Scenario | Why framework knowledge matters |
|---|---|
| Model fails to load | Checkpoint format, missing weights, incompatible architecture, or dependency versions may be responsible. |
| Inference is slow | Investigate warm-up, batch size, device placement, and model optimization. |
| Container runs out of memory | Understand model size, intermediate tensors, batch size, and runtime memory usage. |
| GPU utilization is low | Determine whether inference is CPU-bound, poorly batched, or otherwise unable to use the accelerator effectively. |
| Model deployment increases costs | Compare throughput, latency, resource utilization, and model optimization options. |
| First request is slow | Investigate model initialization and inference warm-up. |
| New model version behaves differently | Compare model artifacts, runtime versions, predictions, and benchmark results. |

**Key takeaway:** Kubernetes manages the application infrastructure, while the ML framework executes the model. Production AI reliability requires understanding both layers.

## 4. ML Framework Fundamentals

### 4.1 What is an ML framework?

An ML framework provides APIs and runtime components for working with machine learning models.

Common frameworks include:

- **PyTorch:** Widely used for deep learning, research, model inference, and LLM workloads.
- **TensorFlow:** Used for training, inference, and production machine learning pipelines.
- **JAX:** Used for high-performance numerical computing and machine learning.
- **ONNX Runtime:** Executes compatible models exported to the ONNX format.

For this lesson, PyTorch is the primary framework because it provides the model-loading, inference, and optimization concepts needed for later AI serving lessons.

### 4.2 What is a model?

A trained model typically consists of an architecture and learned parameters.

- **Architecture:** Defines the model's layers and computational structure.
- **Weights:** Numerical parameters learned during training.
- **Tokenizer or preprocessing logic:** Converts input text into the representation expected by the model.
- **Model artifact:** The files and configuration required to load and use a particular model version.

For example, the DistilBERT sentiment-analysis model used in this lesson receives text and predicts a sentiment label such as `POSITIVE` or `NEGATIVE`.

The model does not simply read raw text. The tokenizer first converts text into token IDs and related tensors that the model can process.

### 4.3 What is inference?

Inference is the process of using a trained model to generate a prediction for new input data.

For example:

Input:

`I love this product`

Output:

`POSITIVE`

Inference differs from training. During training, a model's parameters are updated. During normal production inference, the existing parameters are used to generate predictions without updating them.

For an AI Infrastructure Engineer, inference is particularly important because it determines the compute, memory, latency, throughput, and serving capacity required by an application.

## 5. Model Weights and `state_dict`

PyTorch models contain parameters such as weights and biases.

A `state_dict` is a mapping of parameter names to tensors, along with other registered model state where applicable. It is commonly used to save and restore a model's learned parameters.

Example:

```python
import torch

# Save a model's parameters.
torch.save(model.state_dict(), "model_weights.pth")

# Re-create the same model architecture first.
model = create_model()

# Load the saved parameters.
state = torch.load(
    "model_weights.pth",
    map_location="cpu",
    weights_only=True,
)

model.load_state_dict(state)
model.eval()
```

`create_model()` is a placeholder for the actual architecture construction code. It must be replaced with the correct model definition.

### Why this matters in production

Model artifacts need to be versioned, stored, and deployed consistently. A checkpoint may fail to load if the architecture is incompatible or the artifact is incomplete.

A `state_dict` alone is not generally a complete deployable application. The deployment may also require the architecture code, configuration, tokenizer, preprocessing logic, compatible libraries, and runtime settings.

For production systems, model artifact management should include version identifiers, integrity checks, access controls, and rollback procedures.

### Security consideration

Only load trusted model artifacts. Loading files from untrusted sources can introduce security risks, depending on the serialization format and loading method.

## 6. Inference Mode: `eval()` and `no_grad()`

Two important PyTorch concepts are `model.eval()` and `torch.no_grad()`.

### `model.eval()`

This switches the model into evaluation mode. It changes the behavior of modules such as dropout and batch normalization when those modules are present.

```python
model.eval()
```

This is generally appropriate when serving predictions from a trained model.

### `torch.no_grad()`

This disables gradient calculation within the context. Gradients are normally unnecessary for standard inference, so disabling them can reduce memory consumption and computation overhead.

```python
with torch.no_grad():
    outputs = model(**inputs)
```

For many modern inference applications, `torch.inference_mode()` is another option that can reduce additional autograd overhead:

```python
model.eval()

with torch.inference_mode():
    outputs = model(**inputs)
```

These mechanisms serve different purposes:

- `eval()` controls the behavior of relevant model layers.
- `no_grad()` disables gradient tracking within a context.
- `inference_mode()` provides a more restrictive inference-oriented execution mode.

They are not interchangeable. Calling `eval()` does not itself disable gradient tracking.

### Infrastructure relevance

Using the appropriate inference mode helps avoid unnecessary work and can improve the resource efficiency of model-serving containers.

## 7. CPU and GPU Device Placement

PyTorch can execute compatible operations on CPUs and supported accelerators such as NVIDIA GPUs.

Example:

```python
import torch

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

model = model.to(device)
inputs = {
    key: value.to(device)
    for key, value in inputs.items()
}

model.eval()

with torch.inference_mode():
    outputs = model(**inputs)
```

The model and its input tensors generally need to be on compatible devices.

### CPU inference

Advantages:

- Widely available.
- Often suitable for smaller models and moderate workloads.
- Does not require a GPU runtime.

Considerations:

- Performance depends on CPU capacity, model architecture, batch size, and runtime optimization.
- Large models or high request volumes may require substantial CPU resources.

### GPU inference

Advantages:

- Can accelerate many deep-learning workloads.
- Often beneficial for large models and high-throughput inference.

Considerations:

- Requires compatible hardware and software.
- GPU memory can become a limiting factor.
- Drivers, CUDA libraries, framework builds, container configuration, and Kubernetes device access must be compatible.

### Infrastructure relevance

When a model fails with a device mismatch or CUDA-related error, the problem may be in the application, container image, device configuration, or host environment. Increasing the number of pods alone may not solve it.

## 8. Batching

Batching groups multiple inputs together for a single model execution.

For example:

- Batch size 1: Process one input at a time.
- Batch size 8: Process eight inputs together.
- Batch size 32: Process thirty-two inputs together.

Batching can improve throughput by reducing per-request overhead and improving hardware utilization.

However, a larger batch can also increase memory consumption and the time an individual request waits before execution.

### Important performance metrics

**Latency:** How long a request takes to complete.

**Throughput:** How many inputs or requests can be processed per unit of time.

**Batch size:** How many inputs are processed together in one inference operation.

The fastest batch size is not necessarily the best production setting. The correct choice depends on the application's traffic, latency requirements, model size, hardware, and concurrency.

### Infrastructure relevance

Batching affects capacity planning, autoscaling, resource requests, and the number of inference replicas required to handle traffic.

For real-time APIs, dynamic batching may help improve throughput while enforcing a maximum waiting time. For offline workloads, larger batches may be acceptable.

## 9. Model Warm-Up

The first model inference can take longer than later inferences.

Possible reasons include:

- Model and runtime initialization.
- Memory allocation.
- Kernel initialization or selection.
- Lazy initialization in libraries.
- Compilation or specialization when applicable.
- Operating-system and filesystem caching.

A warm-up phase runs representative inputs before the model receives production traffic.

Example:

```python
model.eval()

with torch.inference_mode():
    for _ in range(3):
        _ = model(**warmup_inputs)
```

The input tensors must already be prepared and compatible with the model.

Three iterations are only an example, not a universal recommendation. The appropriate warm-up procedure depends on the model, runtime, hardware, and workload.

### Infrastructure relevance

Warm-up is relevant to startup latency, readiness probes, deployment rollouts, and autoscaling.

A pod should not receive production traffic until the application has initialized the model and can successfully perform inference. Readiness checks should reflect actual serving readiness rather than merely confirming that a process exists.

## 10. Model Optimization and Quantization

Model optimization aims to improve inference speed, memory consumption, throughput, or deployment efficiency.

Possible approaches include:

- Quantization.
- Compilation.
- Graph optimization.
- Exporting models to a supported runtime.
- Selecting a more suitable serving engine.
- Tuning batching and execution settings.

The correct optimization depends on the model, hardware, framework, and workload.

### 10.1 FP32

FP32 represents floating-point values using 32 bits.

It is a common baseline for numerical model parameters and can offer good compatibility, but it may require more storage and memory bandwidth than lower-precision representations.

### 10.2 INT8 quantization

INT8 quantization represents supported values using 8-bit integer formats. It can reduce the storage requirements of supported weights and may improve inference performance on compatible hardware.

The performance and quality effects depend on the model, operators, quantization method, and hardware.

Quantization can introduce numerical differences, so output quality should be validated before production deployment.

### 10.3 PyTorch quantization APIs

This lesson used the following API:

```python
from torch.ao.quantization import quantize_dynamic

quantized_model = quantize_dynamic(
    model,
    {torch.nn.Linear},
    dtype=torch.qint8,
)
```

This is a legacy eager-mode quantization approach and produced deprecation warnings in the environment used for the exercise. It remains useful for understanding the experiment, but new projects should evaluate the current `torchao` quantization APIs and the appropriate PyTorch-supported workflow.

Quantization support and performance depend on the model and runtime. Do not assume that every model or layer can be quantized using the same approach.

### 10.4 Compilation and export

`torch.compile` can optimize execution for supported models and environments. Compilation can introduce startup overhead and should be evaluated using representative inputs and steady-state measurements.

`torch.export` provides a mechanism to capture a model's computation for supported downstream workflows. It is not the same as simply saving a `state_dict`.

ONNX is another model representation that can be useful when a compatible ONNX Runtime deployment is appropriate.

These options should be evaluated based on compatibility, deployment requirements, measured performance, and operational complexity.

## 11. Hands-On Exercise: DistilBERT Sentiment Inference

### Objective

Build and benchmark a pretrained sentiment-analysis model using PyTorch and Hugging Face Transformers.

The exercise covers:

1. Loading a pretrained model and tokenizer.
2. Running inference on CPU.
3. Testing sample predictions.
4. Comparing batch sizes.
5. Saving FP32 model weights.
6. Applying dynamic INT8 quantization.
7. Comparing model artifact sizes and inference latency.

### Model used

Model ID:

`distilbert-base-uncased-finetuned-sst-2-english`

This is a pretrained DistilBERT model fine-tuned for binary sentiment classification.

The model and tokenizer are retrieved from Hugging Face when needed. An initial run may require internet connectivity and enough disk space for downloaded artifacts.

### Environment

The exercise was run in a Python virtual environment on Linux with Python 3.12 and PyTorch.

Exact dependency versions should be recorded from the environment rather than assumed.

Useful commands:

```bash
python --version
python -m pip show torch
python -m pip show transformers
```

Activate the project's virtual environment before running the benchmark.

### Run the benchmark

From the lesson directory:

```bash
python bench.py
```

The script should report the device, model information, warm-up measurements, batch-size measurements, sample predictions, saved FP32 weight size, and quantized model size and latency.

Use the actual output from your environment when documenting performance.

## 12. Benchmark Results

The following measurements are from the benchmark output captured during this exercise.

| Metric | FP32 | INT8 |
|---|---:|---:|
| Saved weight size | 268 MB | 139 MB |
| CPU latency for batch size 8 | 44.6 ms | 18.5 ms |
| Relative inference time | 1.00× baseline | Approximately 0.42× baseline |
| Relative speed | Baseline | Approximately 2.41× faster |

### Model size reduction

FP32 saved weights: 268 MB

INT8 saved weights: 139 MB

Absolute reduction:

268 MB − 139 MB = 129 MB

Percentage reduction:

(129 / 268) × 100 ≈ 48.1%

The quantized artifact was approximately 48.1% smaller by the reported file sizes.

### Inference speedup

FP32 batch-of-8 latency: 44.6 ms

INT8 batch-of-8 latency: 18.5 ms

Speedup:

44.6 / 18.5 ≈ 2.41×

The measured INT8 inference latency was approximately 58.5% lower than the FP32 latency in this particular test.

These results apply to the captured benchmark conditions. They are not a guarantee of the same improvement on other hardware, model versions, or serving workloads.

### Example predictions

The captured output included:

| Input | Predicted label | Reported score |
|---|---|---:|
| `I love this product` | POSITIVE | 1.00 |
| `This is the worst service ever` | NEGATIVE | 1.00 |

These examples show that the model produced the expected labels for the two sample inputs. The displayed score was rounded to two decimal places, so `1.00` does not establish perfect accuracy or guarantee correct predictions for other inputs.

## 13. Interpreting the Benchmark Correctly

The benchmark demonstrates why model-level measurements matter to infrastructure engineering.

### What the results indicate

- The saved INT8 artifact was smaller than the FP32 artifact.
- The INT8 path had lower measured latency for the tested batch of eight.
- Model optimization may improve storage efficiency and inference capacity.
- Benchmarking allows infrastructure decisions to be based on measurements instead of assumptions.

### What the results do not establish

- That INT8 will be faster on every CPU or GPU.
- That the quantized model will have identical accuracy on a representative dataset.
- That saved checkpoint size equals total runtime memory consumption.
- That the reported batch latency represents individual request latency in a concurrent production service.
- That the same speedup will occur after containerization or deployment to Kubernetes.

For a production benchmark, measure cold-start and steady-state latency separately. Include repeated runs, realistic concurrency, throughput, CPU and memory usage, and relevant percentile latencies such as p50, p95, and p99.

When comparing two models, keep the workload, input data, device, and measurement procedure consistent.

## 14. Deprecation Warnings Observed During the Exercise

The benchmark emitted warnings indicating that the legacy `torch.ao.quantization` APIs used in the script are being deprecated and that migration toward `torchao` quantization APIs is recommended.

The output also included a warning about quantized tensor creation functions.

### What this means

A deprecation warning generally indicates that an API is scheduled for removal or replacement in a future release. It does not, by itself, mean that the operation failed.

In this run, quantization completed and the script reported the INT8 weight size and latency, so the warnings did not prevent the demonstrated benchmark from completing.

For future projects:

- Record the PyTorch version used.
- Review the supported quantization workflow for that version.
- Evaluate `torchao` APIs for new quantization implementations.
- Test the optimized model for correctness and performance.
- Avoid suppressing warnings without understanding their implications.

## 15. Troubleshooting Notes

### Problem: Model download fails

Possible causes:

- Missing internet access.
- Network or proxy restrictions.
- Hugging Face service or download issues.
- Insufficient disk space or permissions.

Actions:

- Check network connectivity.
- Verify the model ID.
- Inspect the full exception.
- Confirm the cache directory has sufficient space and write permissions.

### Problem: Model checkpoint fails to load

Possible causes:

- Incompatible architecture.
- Incorrect checkpoint path.
- Missing or incompatible model files.
- Framework or serialization incompatibility.

Actions:

- Verify the artifact path.
- Confirm that the architecture matches the checkpoint.
- Review the loading error.
- Use trusted artifacts and the appropriate safe-loading options.

### Problem: CUDA is unavailable

Possible causes:

- CPU-only PyTorch installation.
- No compatible GPU.
- Missing or incompatible driver or runtime components.
- GPU not exposed to the container.

Actions:

```bash
python -c "import torch; print(torch.cuda.is_available())"
```

If the result is `False`, check the installed PyTorch build, host GPU, drivers, and container configuration before assuming the model is running on a GPU.

CPU execution is still valid for this lesson.

### Problem: Model inference fails with a device mismatch

Possible cause:

The model and input tensors may be on different devices.

Action:

Verify the model's device and move the model and input tensors to compatible devices before inference.

### Problem: Quantization is slower or produces unexpected outputs

Possible causes:

- The model or hardware does not benefit from the selected quantization method.
- The quantized operators differ in performance.
- The comparison uses inconsistent inputs or measurement conditions.
- Quantization introduces numerical differences.

Actions:

- Benchmark both versions consistently.
- Validate predictions on representative test data.
- Check the quantization API's supported layers and runtime requirements.
- Compare latency, throughput, memory use, and prediction quality before deciding which version to deploy.

## 16. AI Infrastructure Production Applications

The concepts from this lesson apply directly to production infrastructure responsibilities.

### Model deployment

- Package the model, tokenizer, configuration, and application dependencies.
- Retrieve versioned model artifacts from an approved storage or registry.
- Validate model loading before serving traffic.
- Keep deployment and model versions traceable.

### Containerization

- Build reproducible container images.
- Pin and validate compatible dependencies.
- Avoid unnecessarily including large development dependencies in serving images.
- Plan for model downloads, artifact storage, image size, and startup time.

### Kubernetes and EKS

- Configure CPU, memory, and GPU resource requests and limits appropriately.
- Implement meaningful readiness checks that verify inference readiness.
- Configure liveness checks to detect genuinely unhealthy processes without causing unnecessary restart loops.
- Scale according to appropriate workload metrics.
- Deploy new model versions with rollout and rollback controls.

### Observability

Monitor application and infrastructure metrics together:

- Request count and error rate.
- Inference latency and throughput.
- Model initialization and warm-up time.
- CPU and memory utilization.
- GPU utilization and GPU memory where applicable.
- Model version and serving configuration.
- Timeouts and failed predictions.

### Cost optimization

Compare the cost and performance effects of:

- CPU versus GPU execution.
- Model quantization and other optimizations.
- Batch size and request concurrency.
- Instance types and replica counts.
- Model artifact storage and download behavior.

The goal is not simply to reduce resource consumption. The goal is to meet the required latency, throughput, reliability, and prediction-quality targets at an appropriate cost.

## 17. Connection to My Existing AWS, DevOps, and EKS Skills

This lesson builds on existing infrastructure experience and adds model-runtime knowledge.

| Existing skill | How it applies to AI infrastructure |
|---|---|
| AWS | Provides compute, storage, networking, security, and monitoring services for AI workloads. |
| Terraform | Automates repeatable provisioning of the infrastructure supporting model serving. |
| Docker | Packages the model-serving application and its runtime dependencies. |
| Kubernetes / EKS | Schedules inference workloads, manages availability, and supports scaling and rollouts. |
| IAM and security | Controls access to model artifacts, storage, infrastructure, and serving endpoints. |
| CI/CD | Automates testing, artifact publication, image builds, and deployment of model-serving applications. |
| CloudWatch and observability tools | Help identify inference errors, latency increases, resource pressure, and capacity issues. |
| PyTorch | Helps diagnose model-loading, inference, device-placement, and performance problems. |

The combination of cloud infrastructure expertise and model-runtime fundamentals is valuable because production AI systems require both reliable infrastructure and efficient model execution.

## 18. Key Takeaways

After completing this lesson, I understand that:

1. ML frameworks provide the runtime needed to execute trained models.
2. A model's architecture, weights, tokenizer, and runtime dependencies all contribute to a working deployment.
3. `state_dict` is a common mechanism for saving and restoring model parameters.
4. `eval()` and `no_grad()` address different aspects of inference execution.
5. Model and input device placement must be compatible.
6. Batching trades off throughput, latency, and memory consumption.
7. Warm-up can reduce the impact of initialization overhead on early requests.
8. Quantization may reduce model artifact size and inference latency, but results depend on hardware and workload.
9. Benchmarking provides evidence for infrastructure sizing and optimization decisions.
10. Production AI serving requires integrating model-level monitoring with container, Kubernetes, and cloud observability.

## 19. Future Improvements

Possible follow-up exercises include:

- Add repeated measurements and calculate average and percentile latency.
- Compare multiple batch sizes using consistent measurement conditions.
- Track process memory and CPU utilization during inference.
- Validate FP32 and INT8 predictions using a larger representative dataset.
- Investigate current `torchao` quantization APIs.
- Compare eager execution with `torch.compile` where supported.
- Expose the model through a FastAPI inference endpoint.
- Build a Docker image and deploy it to a local Kubernetes cluster.
- Add readiness checks, metrics, structured logs, and load testing.
- Deploy the service to EKS and evaluate resource usage, scaling, and rollout behavior.

## 20. Conclusion

This lesson introduced the ML framework fundamentals required to understand AI model serving from an infrastructure perspective.

Using a pretrained DistilBERT sentiment-analysis model, I explored inference configuration, batching, warm-up, model checkpoint storage, benchmarking, and dynamic INT8 quantization.

The benchmark showed that the INT8 artifact was smaller and had lower measured CPU inference latency in the tested workload. These results demonstrate how framework-level optimization can influence infrastructure efficiency, although production decisions require broader validation.

The most important outcome is understanding that reliable AI infrastructure requires more than deploying a running container. The model must load correctly, execute efficiently, produce acceptable predictions, and meet the workload's operational requirements.

**Next lesson:** Continue into the next curriculum module, applying these fundamentals to model-serving workflows and production AI infrastructure.