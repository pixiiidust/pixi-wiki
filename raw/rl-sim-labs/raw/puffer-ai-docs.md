---
source_url: https://puffer.ai/docs.html
ingested: 2026-06-18
sha256: 315e81b01d99927203c77a04becce6da951a8abe98459e611b20eaafb41a638f
---

PufferLib Docs
PufferLib is a fast and sane reinforcement learning library. Our key features are:

- PuffeRL: 20,000,000 step/second training in only ~5k lines of CUDA. Torch version up to 5,000,000.

- Ocean: 20+ environments from simple arcade games to massively multiagent sims

- Constellation: Performant experiment local + web visualization toolkit in C

- Protein: Our algorithm for automatic hyperparameter and reward tuning

These docs will get you started. Join the Discord to get help and report bugs. If you're new to RL, building and contributing a new env is the best way to learn, and we review PRs live.

# Installation

## Docker

git clone https://github.com/pufferai/puffertank cd puffertank ./docker.sh test
PufferLib uses CUDA, cuBLAS, NCCL, and Nsight. If that sounds annoying to set up, use our Docker. Use ssh -X on setup for remote work or graphics won't work. Need a different CUDA base or system packages? The Dockerfile is really simple. Edit it and run ./docker.sh build -d puffertank.dockerfile
## UV

curl https://raw.githubusercontent.com/PufferAI/PufferTank/refs/heads/4.0/install.sh | sh
Requires CUDA. If you don't want to deal with CUDA deps, use the Dockerfile.
## Installation Test

bash build.sh breakout puffer train breakout puffer eval breakout --load-model-path latest
Trains a policy. 3-5 seconds on an RTX 5090. Eval requires a graphical interface. Works over ssh -X. Docker over ssh requires -X when you first run the container. Running without -X and reconnecting with -X will not work.
# Cheat Sheet

puffer [train|eval|sweep] env_name [OPTIONS] # PufferLib CLI, available from package python -m pufferlib.pufferl [train|eval|sweep] env_name [OPTIONS] # Equivalent command from source # Building PufferLib bash build.sh ENV_NAME # Build training for a specific environment bash build.sh ENV_NAME --float # Use fp32 backend (default is bf16) bash build.sh ENV_NAME --profile # Build our profiling tools bash build.sh ENV_NAME --[local|fast|web] # Build debug/optimized/web env standalones, no training bash build.sh constellation --[local|fast|web] # Build Constellation experiment dashboard # Examples puffer train breakout --train.learning-rate 0.001 # Set other train params puffer train breakout --env.frameskip 3 # Set env params puffer train breakout --vec.num-threads 4 # Set vec params puffer train breakout --wandb --tag tag_name # Track with Weights and Biases puffer eval breakout # Render the env with a random agent puffer eval breakout --load-model-path path/model_file # Load a trained model puffer eval breakout --load-model-path latest # Load the latest model (ls -lt experiments | head) # Distributed training and Sweeps puffer sweep breakout # Run a hyperparameter sweep puffer sweep breakout --sweep.gpus N # Sweep with 6 GPUs puffer train nmmo3 --train.gpus N # Distributed training # Torch bash build.sh ENV_NAME --float # Torch is not stable in bf16 bash build.sh ENV_NAME --cpu # Mostly for Mac users. Expect under 200k sps. # Torch Distributed - you should really, really use our native backend if you are going to scale torchrun --standalone --nnodes=1 --nproc-per-node=6 -m pufferlib.pufferl train nmmo3 --slowly

# About PufferLib

The PufferLib 4.0 native backend is ~1500 lines of Python and ~5000 lines of CUDA C. A PyTorch backend is provided as an additional ~1000 lines of Python for quick prototyping and as a fallback. Fork the project and edit directly. There is no prebuilt package blackboxing functionality. Everything is written as simply and transparently as possible. If you're new to low-level dev, it's much easier than you think. Give the environment tutorial a try!

Memory Management: Tensors in PufferLib are just structs with a shape and a data pointer. Every tensor registers its size with an allocator at init time. After all tensors are registered, the allocator sums up the sizes and does a single allocation of continuous memory. There are separate allocators for weights, gradients, and activations. No tensors are created or reallocated afterwards. Static memory improves performance, simplifies cudagraph tracing, and cleans up profile timelines. Since weights and gradients are contiguous, we can apply updates to them in a single kernel without looping over tensors.

Tracing: Cudagraphs capture and replay GPU operations in order to reduce kernel launch overhead. At the start of each run, PufferLib runs a few warm up epochs on empty rollout buffers. It then separately traces both the rollout forward pass and the entire train minibatch + loss + policy update. We bloat memory a bit by tracing separate cudagraphs for each step during rollouts in order to avoid an extra data copy for intermediate graph buffers.

Vectorization: Environment instances are chunked into buffers, each of which is associated with a rollout worker on a separate CUDA stream. Within each buffer, environment execution is parallelized with OMP threading. Rollout workers are independent of each other but each process the same number of environment steps per epoch. Each buffer asynchronously queues data transfers to/from the GPU and uses pinned memory.

Kernels: The main consideration for performance is fusing small elementwise operations to reduce memory bandwidth. For most of our kernels, the efficiency of the compute load is secondary. The MinGRU kernels are load-bearing and have received more attention to performance. The learnable workload of MinGRU is a set of linear layers implemented as cuBLAS matmuls. None of our kernels include complex operations with tensor cores.

Algorithm: PufferLib implements a PPO-variant with improvements based on our own research. The main improvements are our use of Muon, a custom advantage function combining GAE and VTrace, and prioritized replay over trajectory segments collected from the current epoch using absolute advantage.
PufferNet: Our default model architecture combines MinGRU, an RNN that is parallelizable over the time dimension, with highway nets, a fancy residual that replaces expensive normalization layers. It's equal to or better than an LSTM on every environment we've tested and much faster.
Sweeps: The fundamental unit of compute in PufferLib is a hyperparameter sweep, not a single experiment. Protein is a tuning algorithm based on our own research. It combines Gaussian processes with a simple genetic algorithm over the Pareto-frontier defined by cost (experiment wall-clock time) and score. This is the main thing we haven't ported over to CUDA C yet.
# Tutorial: Writing Your Own Environment at Millions of SPS (steps/second)!

Ocean environments are written in C. It's very simple C. Like first 2 weeks of an intro systems course C. Follow this guide and then copy Squared (single-agent) or Target (multi-agent) to use as templates for your own environment. Both have detailed comments that walk you through the requirements. Find/replace the demo name with your environment name.

The .h file contains core environment logic. The .c file contains a standalone demo. Only the .h file is compiled when you run puffer build env_name . The standalone is compiled with puffer build env_name --local or --fast for the optimized build. Observations, actions, rewards, and terminals are each allocated as big chunks of memory that are contiguous across all (usually thousands) of environment instances.

Create a .ini file in the config/ directory with the settings for your environment. Copy the one for Squared or Target as a starting point. Your environment is now available for training just like any other Ocean environment:

puffer build env_name puffer train env_name

Use the --local compilation option for testing while writing your environment. It enables address sanitizer and will catch most indexing and overflow bugs. Here's a checklist of common bugs if your env is not training:

- Zero or incorrect observations/actions: Ensure you have defined your observation and action metadata (space/size/type) correctly in your binding.c. Note that observation buffers are not zeroed for you every step, so if you are only writing information to specific indicies (i.e. one-hots), be sure you are zeroing them. One memset is usually the quickest.

- NaN losses: If your losses NaN after 1 epoch, your environment almost certainly has data corruption. You are writing to memory that does not match the obs/action sizes you have defined, or you have defined them using the wrong types. If your losses NaN after a longer time, it may be hyperparameters.

- Incorrect or missing resets: Your environment should handle its own resets internally. For envs that never reset, it is often useful to respawn agents if they are stuck (e.g. no reward for 500 steps). If every rollout has the same number of timesteps, you should stagger your environments on init.

- Not zeroing observations: If you are writing over your observation buffers but only write to some elements each step, If you don't zero out rewards, they will retain their value from the previous step. Ditto for terminals. Zero them at the start of c_step to be safe. A single memset will do it for multiagent envs. If you are not setting every element of every obs (i.e. one-hots), make sure to clear those too.

- Manually inspect data scale: You want observations and rewards to be roughly in the range of -1 to 1. 0 to 1 is fine. -5 to 5 is kind of fine. Randomly having one obs with magnitude 1000 is not.

- Incorrect binding args: Ensure your binding sets the same args as your .c file. Call your init function if you have one.
# FAQ

Why is it called PufferLib? Would you have rathered yet another minimal tech logo? Here, have a pufferfish 🐡
I'm new to RL. How do I contribute? Start by building a simple new environment in C and getting it to train. I review environment PRs from new contributors live on stream.

How do I export screenshots/gifs? F12 for screenshots, control+F12 for gifs. This is built in to raylib.
Where did all the Python/third-party stuff go? It was all 100x+ slower than PufferLib is now. We do plan on hooking the C/C++ for Atari, NetHack, and maybe ProcGen into our low-level interface when we have time.
