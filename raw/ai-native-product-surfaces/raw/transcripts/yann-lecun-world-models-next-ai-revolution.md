---
source_url: https://youtu.be/72Xj8k5WQX4?si=tFQOgcbG-xzmz7WI
ingested: 2026-06-26
sha256: b9eb1d14ab4133de9902cdc46cbdc6b3410b601d35175b57dab3244dc17f7fd5
source_type: transcript
speaker: Yann LeCun
---

# World Models: Possibly the Enabler for the Next AI Revolution

**Format:** Cleaned Markdown transcript
**Source:** User-provided transcript
**Note:** Light cleanup applied for punctuation, paragraphing, and obvious speech disfluencies. Meaning preserved.

## Talk

**Speaker:**

Yeah, I’ll talk about world models, possibly the enabler for the next AI revolution.

There are a lot of machine learning people in the room, perhaps. I have bad news for you: machine learning sucks. When we compare the learning abilities of machines with humans and animals, clearly there is a big gap.

People and animals can learn new tasks extremely quickly and with very few trials, very few samples. People have common sense. Animals too, physical common sense. There are a lot of tasks that we can accomplish zero-shot, even if we have never faced them before.

How do we do this with machines? We have very powerful AI techniques that everybody is using, but they do not really handle the real world. They do not handle continuous, high-dimensional, noisy data. Language is easy by comparison. The real world is messy. Language is simple.

This connects with what Vladlen said earlier, and Jitendra as well: Moravec’s paradox. Things that are simple for humans are difficult for computers, and things that are complicated for humans turn out not to be that difficult for computers, like playing chess, computing integrals symbolically, solving equations, proving math theorems, and so on.

How is it that a 10-year-old can basically do what you would like a domestic robot to do, and do most of those tasks without actually being trained to do them? The first time you ask them, they can do it. They may not want to do it, but they can.

How come any teenager can learn to drive a car in a few hours of practice, yet self-driving car companies have literally millions of hours of training data? Despite that, they cannot use those millions of hours of training data to get a machine, just imitating humans, to drive at the same level of reliability. Otherwise, we would have Level 5 self-driving cars, and we do not. At best in the consumer car business, we have Level 2 or 3. Robo-taxis are heavily engineered with various sensors and other things.

So we keep bumping into Moravec’s paradox, and we really have to go beyond this.

If you believe that intelligence requires grounding, and some philosophers and certainly some language people do not believe that is necessary, but I think it is, then this matters. Like Vladlen, we are in Switzerland, outside Jean Piaget. He was a big influence on me.

Piaget had a debate with Noam Chomsky in France in the late 1970s. They were debating whether language was innate or learned. There were transcriptions of that debate, with people participating in it. One of them was a guy who had worked with Piaget and was a professor at MIT. He was talking about the perceptron, saying that these simple machine learning models were capable of learning surprisingly complex tasks, and that this might be evidence that learning is possible, contrary to what Chomsky was saying.

This guy was Seymour Papert. He was a professor at MIT, and 10 years before that he had written a book that basically killed the entire field of neural nets by pointing out the limitations of the perceptron. But here he was 10 years later arguing that those things were actually interesting to study.

Piaget is often quoted as saying: “Intelligence is not what you know, it is what you do when you do not know.” In fact, he never actually said this. It is apocryphal. But other psychologists distilled his thinking into this sentence, which he never said.

Intelligence is not an accumulation of declarative knowledge. LLMs are an accumulation of declarative knowledge. Not just that, but the main reason they are useful is because they can accumulate a lot of declarative knowledge.

Intelligence is not a collection of skills. You can probably build a machine to accomplish almost any task if you spend enough resources on it, including things like self-driving. But that is not really what intelligence is.

Intelligence is the ability to learn to drive in about 20 hours, to learn any new task with very little training, or to accomplish new tasks. That is really what intelligence is. That is really what Piaget means.

That means we are not going to have any simple measure of intelligence, because any particular task can always be cracked if you spend enough effort and time. It is more about how adaptive you are.

This connects to something Vladlen said: the notion of AGI is complete nonsense. Human intelligence is specialized. The characterization of human intelligence is that it is very quickly adaptive, and we can learn new tasks. All of us know different sets of knowledge and have different skills, because we have been exposed to different environments and have had to solve different problems. We are adaptive. That is really what intelligence is.

## How Humans and Animals Learn

How do humans learn, and animals for that matter?

A lot of learning takes place in the early months of life, mostly by observation. A two-month-old baby can gesticulate and can develop a dynamical model of its own limbs, but basically cannot affect the world. It cannot move an object or anything. But it can learn a lot of things about the world.

One thing a baby can learn really quickly is that the world is three-dimensional. Why? Because the fact that every point in the world has a distance from us is the best way to explain how our view of the world changes when we move our head. Babies do not necessarily move their heads, but they are being moved. They see parallax and derive from this the fact that the world is three-dimensional.

We can do this with learning machines today. They learn that the world is three-dimensional only by being exposed passively to videos. That is interesting.

Basic concepts like object permanence are learned really quickly. Notions of stability, rigidity, and things like that. But what we would consider intuitive physics, things like inertia and gravity, take nine months for human infants. It is shorter for most animals.

If you put an eight-month-old or nine-month-old on a high chair and put a bunch of toys in front of them, the child will most likely systematically take all the toys, throw them on the floor, and watch the result. They are doing the experiment that gravity applies to everything.

That takes a long time. How does that happen? What type of learning is taking place? They are doing experiments, but they can also learn about gravity by observation.

If you show the scenario at the bottom, where a car is on a platform and you push it off the platform, but it appears to float in the air, a six-month-old will barely pay attention. They have not learned about gravity yet. A 10-month-old will be very surprised, like the little girl in the slide.

That is how psychologists measure whether a baby has learned a particular concept about the world, through violation of expectation. We can use those techniques to test whether machine learning systems have acquired some notion of common sense.

There is a lot that can be said about this. Jitendra and I collaborated on a paper here, mostly written by Emmanuel Dupoux, and Jitendra had very little contribution to it, on this whole set of questions.

## What Intelligence Is

What is intelligence really, if it is not an accumulation of skills or declarative knowledge?

It is the ability to accomplish new tasks and solve new problems without prior training.

Again, AGI makes no sense as a phrase. Human intelligence is specialized. The question is not whether you know how to do everything. The question is whether you can learn quickly how to do anything, or a wide spectrum of things.

This is a somewhat philosophical paper at the bottom, written by some of my young colleagues.

Here is a simple calculation. There are still a lot of people, particularly on the west coast of the US, who believe that we are going to reach what they call AGI by scaling up LLMs, maybe training them on synthetic data, maybe using a few tricks in post-training and reinforcement learning. I think that is impossible.

I am a believer in grounded intelligence. You can do this simple calculation.

A typical LLM today is trained on something like 20 trillion words. That corresponds to about 30 trillion tokens. Each token is about three bytes, so the data volume is about 10^14 bytes. This would take about 400,000 years for any human to read.

Compare this with what a four-year-old has seen during his or her life. That is about 16 hours of wake time per day, which is a small amount of video, about 30 minutes of YouTube uploads. We have two million optic nerve fibers carrying about one byte per second each. So the data volume that a four-year-old has seen through vision, and probably through touch as well, is about 10^14 bytes.

A four-year-old has seen the world through vision with the same amount of data as 400,000 years of text, with all the human-produced text publicly available on the internet.

We are not going to get to anything like human-like intelligence by just training on text. It is just not going to happen.

Of course, you might say video is much more redundant than text. But that is a feature, not a bug. If you want to train a system, particularly using self-supervised learning, you need redundancy in the data. If you do not have redundancy, you cannot learn anything. Redundancy is a good thing. You do not want too much of it, though.

## Inference by Optimization

There is another question about the right properties of intelligent systems. In my opinion, an important property is the mode of inference.

Does the system compute its output by propagating through a fixed number of layers of some neural net? Or consider the alternative: computing the output by searching for an output that is most compatible with the input.

You observe a situation. That runs through some perception module that produces some representation of the current state of the world as you observe it. You can directly produce an action. That is a reactive system.

Or you could imagine an action and have the intelligent system figure out whether it is a good action for this observation. Is this something that will accomplish the task I want?

The objective here characterizes whether the task the system wants to accomplish has been accomplished. Think of it as a cost function. It is not used for learning. It is used for inference. Think of it as negative likelihood in a probabilistic inference model, or as I prefer to think of it, an energy function.

The inference process is a process by which you search for an output that minimizes some energy function at inference time. That is intrinsically more powerful computationally than just propagation through a fixed number of layers.

Contrast the model on the left, which is LLM-like. You take a window of inputs, run it through a fixed number of layers of a big neural net with a few hundred billion parameters, and produce one token. Then you shift that token into the input and produce the second token, and so on.

That is autoregressive prediction. Every token involves a fixed amount of computation: running through a fixed number of layers of some neural net. This is not a good model of reasoning.

The way you coerce an LLM to do reasoning is that you trick it into generating more tokens. But that is not the way we reason. We reason internally. We do not reason in token space, or even in language.

Compare this with the model on the right, which is a slight specialization of the previous one.

You perceive the world or your environment. You get some idea of the current state of the world. Then you imagine a sequence of actions, a proposal for an action. You feed it to an internal world model, and the world model predicts the outcome. Then it feeds this outcome to an objective that measures to what extent a task has been accomplished.

Then, by optimization, you search for an action sequence that optimizes this objective, or minimizes this energy, at inference time.

In my opinion, that is a much more powerful model. But you need a world model.

## A World Model Architecture

I settled on this idea or architecture about five years ago. I wrote a long paper about it and put it online in 2022 with some general architecture. If you want to take pictures, here are QR codes. It is relatively easy to read, but long.

It is based on the idea that reasoning and planning are essential, and they proceed by energy minimization rather than forward propagation. For this to work, you need a world model.

It is the same process I described before, with a few additional tricks.

You observe the environment. A perception module produces a representation of the initial state of the world, but only a representation of what you currently perceive. You may have to combine this with the content of a memory to get a complete idea of the state of the world, or at least what you know about it.

Then you feed this to your world model, together with a proposal for an action sequence. Your world model predicts the outcome of that action sequence. You feed this to an objective, an energy function, that measures to what extent a particular task has been accomplished.

This function outputs zero if the task is accomplished, and some positive number if the task is not accomplished. Perhaps it measures some distance to the task being accomplished.

You can have another set of objectives that are guardrails. They ensure that whatever state sequences the system is going to take the world through will not kill anyone, hurt anyone, or have any deleterious effect.

A system constructed this way can be made intrinsically safe because it has to obey and optimize the guardrail objective with every output it produces.

This is not the case for an LLM. The only way an LLM can be made safe or non-toxic is by fine-tuning it. There is always a way to break the conditioning, or jailbreak the system. Here, you cannot jailbreak a system like this. It can do nothing but optimize the guardrail objectives and the task objective.

If you have a world model, there are certainly a lot of roboticists and optimal control people in the room, you can apply this world model multiple time steps. Each action sequence can be decomposed into a sequence. The guardrails can be applied to all the steps in the sequence.

That is the way you would use a world model. The way you plan by optimization is akin to model predictive control, MPC, very classical stuff in optimal control going back to the 1960s.

## Hierarchical Planning

Ultimately, what you want is something that can do hierarchical planning. All of us do hierarchical planning. Animals do hierarchical planning.

What is hierarchical planning? Suppose I am sitting in my office at NYU and I want to be in Paris tomorrow. There is no way I can plan my entire trip to Paris in terms of muscle actions 10 milliseconds by 10 milliseconds, which are the elementary actions that humans can do.

I cannot do that because, first of all, it is too long. Second, I do not have the information. I do not know how long I will have to wait on the street before a taxi stops. There is no way I can plan the entire thing.

I have to do hierarchical planning.

At a high level, I can say: I do not know how long it will take me to go to the airport, but maybe roughly an hour or an hour and a half. So I need to get to the airport and catch a plane. That is a two-step high-level plan. I do not need to know many details to make that plan.

Now I have a subgoal: being at the airport. I am in New York, so going to the airport involves going down to the street, hailing a taxi, and going to the airport.

Now I need to go down to the street. I am in an NYU building, so that involves walking to the elevator, pushing the button, getting down, and walking out the door.

Now I have a subgoal: getting to the elevator. You can go down this hierarchy.

At some point, you get to a point where the action you need to take is very simple. It is something you are familiar with. You may not have to use your full mental power to plan the action. You can probably stand up from your chair without having to think about it. That could just be a policy.

Ultimately, we want systems to do hierarchical planning.

How do we solve that? This is an unsolved problem. If you are a roboticist, or an AI for robotics person, or an agentic AI person starting a PhD on this topic, this is a great topic. It is completely open. Nobody knows how to do this, or nobody has proved that they know how to do this.

## Training World Models

Now the big question is: how are we going to train those models?

Hierarchical or not, let us start with non-hierarchical. First we have to figure out what architecture to give them. A natural instinct these days is to train a generative model.

In fact, I have been working on trying to train world-model-like things for about 15 years, mostly failing for the first 10, because I was trying to train generative models.

What is a generative model?

Self-supervised learning has been incredibly successful in the context of language. You take a string of words, remove some of the words, corrupt the input, run the corrupted input through a big neural net, and train it to recover the missing parts.

That works amazingly well for text. The original models like BERT used to do this. An LLM is a special case where the only word you remove is the last one, so the entire system is trying to produce the next word in a sequence.

It works amazingly well and it scales if you do it right.

It does not work if you apply it to video.

If you take a video and show the initial segment of the video to the system, then ask it to predict what will happen next at a pixel level, it does not really work. The representations you get from the system for your video are not particularly good.

The reason is that you simply cannot predict everything that takes place in a video. There is an infinite number of plausible things.

In text, it is easy because there is only a finite number of words. You can get the system to produce a probability distribution over all possible words or tokens in your dictionary.

You cannot do this with video. There is an incredibly large number of possible video frames.

Take an example. If I take a video of this room, start here, slowly rotate the camera, stop here, and ask the system to continue the video, it is probably going to predict that we are in some sort of classroom or auditorium, that the room has a finite size, that there might be windows on this side, and things like that.

There is absolutely no way the system can predict what all of you look like, or which chairs are unoccupied. It is impossible. You just do not have the information.

So when you train a system to make this kind of prediction, you kill it.

Of course, you are going to tell me: but we can train systems to produce cute videos. Video generation, yes. But this prediction is usually done in representation space, not pixel space. It is only a second stage that turns the predictions into high-resolution, high-frame-rate videos. The system only needs to produce one cute-looking video. It does not need to actually represent all plausible videos. That is a much simpler problem.

As I said, I have been working on this for the better part of the last 15 years. Here is a 10-year-old paper where we tried to train a neural net to predict short video clips, two frames from four frames of context. You get blurry predictions. Why? Because the system predicts the average of everything that can happen.

Of course, you can correct that with latent variable models like diffusion models, which we did not know at the time. We tried to use GANs and things like that, but were not too successful. Perhaps using latent variable models would help, diffusion models in particular, which of course produce cute videos.

Do they actually understand the world? The evidence is no.

## Joint Embedding Predictive Architecture

Here is my solution: an architecture called joint embedding, or more precisely Joint Embedding Predictive Architecture, JEPA, shown on the right.

On the left you have a generative architecture. You observe X, maybe you observe A, an action that is taking place, and you observe the result Y. The system is trying to reconstruct Y in its most minute details.

With JEPA, you observe X, Y, and A, but you encode both X and Y, and prediction takes place in that representation space.

That is a major difference. The system can essentially eliminate from the input, by constructing a representation of Y, all the information about Y that is simply not predictable. That makes the prediction more abstract, with fewer details, but more accurate in a way.

How do you train a generative model? It is easy because the cost is just a reconstruction cost. You train it to reconstruct. You can train it as an autoencoder, but then you need to restrict the information content in the code, or as a denoising autoencoder, which is what a lot of techniques like masked autoencoders have attempted to do.

That means taking an input, corrupting it in some way, and training an autoencoder to recover the initial one. Diffusion models are a special case of this general idea of denoising.

The bad news is that when you train systems of this type to learn representations of images, you do not get good representations. If you use the representations of images obtained this way and feed them to a downstream task that you train supervised, the results are not great.

To get good results, you have to use joint embedding architectures. All the best systems that use self-supervised learning to train image or video representation systems use joint embedding. None of them uses reconstruction.

For images, either you have two views of the same scene and you train a neural net to produce representations, telling the system you want those two representations to be identical, or you use the corruption technique. You take an input, corrupt it or transform it in some way, and train this JEPA architecture to predict the representation of the original image from the representation of the corrupted version.

There is a big issue: the system can collapse.

Generative models can also collapse to some extent. If you train an autoencoder without a restriction on the information content of the code, your autoencoder learns the identity function. That is a collapse. It is not going to learn anything useful.

Similarly, a system like this can collapse by completely ignoring the inputs and producing constant representations. Then the prediction problem is trivial. If you just train a system of this type to minimize prediction error, it is going to collapse. It is not going to do anything useful.

The whole trick of self-supervised learning for joint embedding systems is how you prevent collapse.

My favorite concept for preventing collapse is information maximization. You come up with an objective function that measures some sort of information content of the representation that comes out of your encoders, and you try to maximize that information content. Your cost function is minus the information, or something like that.

There are a bunch of techniques for this from the last six or seven years, with names like MCR, MCR^2, VICReg, VICRegL, and Barlow Twins. Barlow Twins and VICReg come from people working with me. The other ones are from other groups. MCR comes from Berkeley, and MCR^2 from a colleague at NYU in neuroscience.

This idea of JEPA is gaining popularity. There are about 1,700 papers that mention “joint embedding predictive architecture” spelled out on Google Scholar.

## Measuring Information Content

There is an issue with this type of method: how do you measure information content?

We need a cost function that is a differentiable measure of information content so we can backpropagate gradients and maximize it.

The bad news is that, first, we do not have objective measures of information content, because all the proper definitions are based on knowing the distribution of the vectors, or whatever you want to measure the information content of. We do not know the distribution. We only have samples coming out of an encoder.

How do you compute information content from a finite number of samples? That is the first problem.

The second problem is that, to maximize something, you would need a lower bound on information content, so that when you maximize, you push the actual information content up. The problem is that every empirical measure we have is an upper bound.

So what do we do? We come up with a good upper bound, cross our fingers, show some theorems, and so on.

## Energy-Based Models

The way to properly explain how you can train self-supervised learning systems, and every learning system really, is a framework I call energy-based models. I have been advocating for this for 20 years or so.

The basic idea is this: if you want to capture the dependency between two variables X and Y, and there is no real functional relationship between X and Y, meaning there is no single Y for a given X, only a dependency, then you cannot run a function that computes Y from X.

This is indicated by the diagram on the right. You have a bunch of data points, the black dots, and they indicate some sort of dependency between X and Y.

How do you capture this dependency, given that you cannot run a function that computes Y from X?

One way is to learn or build a contrast function, an energy function, that tells you whether a point in this XY space is near the training data or not.

Think of it as a landscape where the black dots are in the valley. In Switzerland, there would be a lake. Then you get level curves. As you move outside of those regions, the altitude goes up. The energy goes up.

Now, if I give you a value for X, you can infer a bunch of values for Y that are compatible with X. There are values of Y that minimize the energy. It is the kind of inference I was talking about earlier: inference by optimization, not by forward propagation.

You can possibly do it the other way around. If I give you Y, you can infer X from Y and give me multiple answers.

In situations like video prediction, where there is basically an infinite number of possible answers, the proper way to train a system of this type is to think of it in terms of energy-based models.

Probabilistic models are a special case where your energy has a particular form and the way you train it has a particular loss function. This is a slightly more general framework than probabilistic inference and learning.

To train an energy-based model, you have to prevent collapse. The collapse problem I was telling you about before would be manifested by the energy function being flat everywhere. You train the system to minimize energy for a bunch of training samples, and the system gives you an energy function that is zero everywhere.

That is what an autoencoder that learns the identity function does. That is what a JEPA that ignores the input and produces constant representation does. It has zero prediction error for everything. So it is a collapse.

To prevent collapse, you need one of two things.

One is contrastive methods. You generate points outside the region of data and push the energy up. You come up with a cost function that makes sure the energy of the data points comes down and the energy of other points is higher.

There is another set of methods, which I have come to prefer: regularized methods. They work by minimizing the volume of space that can take low energy. If you push down the energy of certain regions, the rest has to go up because there is only a small volume of low energy to go around.

In practice, this reduces to one of those two methods.

## Information Maximization

Let us go back to this idea of information maximization.

Suppose I run a batch of samples through one of the encoders. I get a matrix where each row is the representation for one sample, and each column is the value of one variable in the representation for all samples.

There are two ways to make that matrix informative.

One way is to make sure all the rows are different.

Another way is to make sure all the columns are different. You want to make sure the columns are different because if all the columns are the same, every variable in the representation carries the same information. That is not very informative.

You want each variable in the representation to be maximally disentangled from the others, to give independent information from the other variables.

That is an example of what we can call dimension-contrastive methods, which are a form of regularized method.

At the bottom, the type of criterion that makes the rows all different corresponds to contrastive methods, or sample-contrastive methods.

Sample-contrastive methods are very popular for certain applications. A lot of the perceptual pipelines in LLMs are trained with a technique called CLIP, which is basically a contrastive method that does joint embedding between images and text.

But I prefer the other one.

## Abstraction and Prediction

The idea that you need to find an abstract representation of an input to make prediction is very natural.

We do this all the time as humans. We do this all the time as scientists and engineers. Animals do it too.

In principle, I could explain or simulate everything taking place in this room at the level of quantum field theory or particle physics. I could simulate the trajectory of every particle in this room, going all the way down to simulating all of our brain processes and everything. In principle, running the simulation, I could figure out whether any of you actually understand the words I am saying, whether you are sleeping, or whether you are totally bored.

Of course, that is completely impractical.

What we do in science is invent abstractions that allow us to make predictions. Those abstractions ignore a lot of details about the underlying state of the system.

We invent abstractions from quantum fields to particles, atoms, molecules, proteins, organelles, cells, organisms, individuals, societies, and ecosystems. Every level in this hierarchy is a particular level of abstraction with which we describe the world. It allows us to make longer-range predictions than the levels below by ignoring many details of the lower level.

That is why the way to understand what is going on in this room at the moment is more at the level of psychology than at the level of particle physics.

Of course, physicists always make fun of everyone by saying that everything is just applied physics. Even psychology is applied physics to some extent. But in fact, there is specific knowledge about chemistry that does not derive directly from physics.

This abstraction contains new knowledge, information, or structure that was not apparent at the level below.

This idea of JEPA constructs on the concept that you need to find an abstraction to be able to make predictions.

Suppose you want to design an airplane. You need to design the airfoils for the airplane, so you do computational fluid dynamics. You simulate the flow of air around the wing. You model the state of the air in every little cube around the wing by velocity, density, and so on, and then you solve Navier-Stokes partial differential equations. That simulates the flow of air.

But it ignores a huge amount of detail in the underlying mechanism. The underlying mechanism is molecules of air bumping into each other and bumping into the plane.

You never simulate fluids at that level. It is too complicated, and it would diverge from reality really quickly because it has too many details. You have to ignore details to be able to make accurate long-term predictions.

We do this in science all the time.

World models should not be simulators. They should work in abstract space. They should not be digital twins, which is a buzz phrase. They should definitely not be generative models, as I just explained. They should not be video generation systems.

A lot of people are working on video generation and calling this world models. They are not world models. They are video generation systems.

One big message from my talk is: if you want to use world models, do not work on video generation. That is a different problem. If you want to produce cute videos, work on video generation. But if you want to control robots or industrial processes or understand the world, do not work on generation.

You want models to control complex systems where you cannot model the dynamics by writing a bunch of equations.

If you have a humanoid robot, or any kind of robot, you can write down the dynamical equations and simulate the dynamics of the robot. You can get your humanoid robot to do somersaults and kung fu and whatever. That is simple.

As soon as a robot starts to interact with the real world, it becomes much more complicated. That is more difficult to reduce to simple equations.

Think about a complex system like a turbojet, a chemical plant, a patient, or a robot that interacts with the real world in complex ways. You cannot reduce this to a small number of equations.

You have to learn a phenomenological model of the whole system, the system you control and its interaction with the environment, so you can make predictions and plan a sequence of actions to arrive at a particular outcome.

That is a world model. The concept is very old. It goes back to the 1960s and is the root of optimal control.

## SIGReg

Now I come to a particular technique that I am very fond of, and that I think we will expand over the next few months and years to do this information maximization. It is called SIGReg: Sliced Isotropic Gaussian Regularization.

The trick is the following.

You run a batch of samples through your encoders, and you get a bunch of points in a vector space, with dimension equal to the dimension of your representation space.

We are going to try to make the distribution of those points isotropic Gaussian, with the same variance in all dimensions.

Why? Because an isotropic Gaussian is a distribution where all variables are independent. They are maximally informative individually. It is also the distribution that has maximum entropy for a given variance, but we do not really care about that. What is interesting is that it makes the variables independent of each other.

How do we do this?

Of course, we do not have the distribution. We just have a bunch of points. It may be a high-dimensional space, like 2,000 dimensions, and we may have a few hundred or a few thousand points. How can we make sure this is a Gaussian?

Here is the trick. You project the individual points along a single direction, and what you get is a marginal distribution.

Of course, you still have discrete points. You do not have a continuous density. You have discrete points.

One trick is to compute the cumulative distribution that those points give you. It is a staircase because you have discrete points in one dimension.

Then you can ask: what is the distance between the staircase, the empirical cumulative distribution of my points, and the cumulative distribution of a Gaussian?

You can do that because you know what the Gaussian looks like. For every point on the staircase, you can tell whether it is to the left or to the right of the ideal Gaussian. That gives you a gradient: do I move the point this way or that way in that projection?

It gives you a gradient for every training sample in your batch.

If you make the distribution Gaussian along that projection by gradient descent, it makes the marginal distribution Gaussian along this projection.

There is a theorem that says if you do this along lots and lots of directions, then in the limit your joint distribution is actually isotropic Gaussian.

What we need to do is many projections. For all of those projections, compute those gradients, move the points, or backpropagate through the network and change the weights, so that the points move and the overall distribution becomes more Gaussian.

If you apply this to a distribution like the one on the top left, an X shape in two dimensions among 1024, and do gradient descent, you move the points. You do not train a neural net in that example. The technique I am advocating for gives you something that is sort of Gaussian-ish.

This really works in practice. We have applied it to training world models that are action-conditioned, and we have used them for planning. It works decently. The source code is available. It is very simple. You can train it on one GPU.

What we need to do with this technique is scale it up. There are a few other things we need to do, but that is the main one.

In simple cases, you can train this world model and use it to plan simple actions, as in Push-T or simple robotic situations in simulated environments. That needs to be scaled up, but it is good work.

There is a theoretical paper that we put out just a few days ago. If you make the hypothesis that the underlying distribution of your data is actually an isotropic Gaussian, and assume that the observations you get from the world are some complicated nonlinear transformation of those points, like a spiral transformation, then if you train a neural net with SIGReg on it, it will recover the original Gaussian in representation space.

It is not a general proof that it works in every case. But it is a proof that if your original explanatory variables are Gaussian, the system will recover those variables up to a rotation.

## Distillation Methods: I-JEPA, V-JEPA, and DINO

We can use these techniques in the context of self-supervised learning to train an image recognition system.

There is another set of techniques that I should mention because they work really well and are the ones that have been scaled up so far. SIGReg is conceptually my favorite method, but it is very recent and we have not scaled it up yet. These other methods are based on distillation, and we have scaled them up and obtained really good results for both images and video, with techniques like I-JEPA and V-JEPA.

What is the basic idea of those distillation methods?

You still have two encoders. So it is a JEPA architecture.

You take an input, transform it, corrupt it, or mask it, and then train the system to predict in representation space. But you do not propagate gradients through the encoder on the right.

Those are two encoders with identical architectures, and they kind of share the weights. The encoder on the right uses an exponential moving average over time of the weights of the encoder on the left.

The encoder on the left gets gradients and gets updated all the time. The encoder on the right gets updated more slowly and shares the weights.

This is derived from intuitive ideas by people at Google DeepMind who were using techniques like this to stabilize the variance in reinforcement learning. They realized you could apply this to self-supervised learning from images. They called this BYOL, Bootstrap Your Own Latent.

There are a whole bunch of methods from Meta in particular, such as SwAV and others, that use this exponential moving average idea.

A particular method called I-JEPA, which I show here, produces really good results. With I-JEPA, we were able to compare results against a generative approach called MAE, masked autoencoder. I-JEPA is not only better, it is much faster to train.

Another technique is called DINO. Many of you, I am sure, have heard of it. I know some of you have used it because there were projects in the robot demos that used DINO.

This was done by some of our former colleagues at Meta in Paris. It is completely self-supervised. It is a joint embedding architecture. It uses distillation, with various tricks I am not going to explain. There is a lot of engineering behind it.

These systems basically, at this time, produce the best generic representations of images. If you have any type of vision task you want to do, this is probably the best encoder for images.

Among other things, what we have done is use DINO as an encoder, train a world model, and do planning.

## Planning Demo

Let me show you a cute video.

You have an initial state of a simulated environment with pretty complex dynamics. You have goals at the top. At the bottom, what you see is the sequence of actions of a planner that uses this trained world model to get the world to a configuration as close as possible to the original one in less than 25 steps.

This has been applied to a number of different scenarios, like double pendulum, Push-T, and others. It now works really well.

## V-JEPA and Common Sense

More recently, we applied this to video.

You take a video, mask a big chunk of it, and train the JEPA to produce good representations, so that it can predict the representation of a full video from the representation of a partially masked one.

Once the system is trained, you use the encoder as a way to extract features from the video, and you train a head on top of it to accomplish some task.

It works really well, state of the art for many traditional vision tasks, particularly from video: action recognition, action prediction, and so on.

Instead of boring you with a table of results, one interesting thing I want to mention is that V-JEPA has learned some level of common sense.

Because we train it to predict what will happen next in a video, we can train a predictor to do that and measure its internal prediction error. We can show it a video and monitor the internal prediction error at every time step.

This system takes a window of 16 frames. We slide those frames over a video and measure the prediction error for the next 15 or 16 frames.

The cool thing is that if you show it a video where something impossible happens, something unphysical, the prediction error shoots to the roof.

It is like the little girl in one of the early slides looking at the scene of the car not falling.

If you have a video of a ball being thrown and the ball disappears, the prediction error shoots through the roof.

That is interesting because it is the first time, at least from my point of view, that I have seen a completely self-supervised system acquire some level of common sense, telling you what is possible and what is not possible.

Let me skip this. It is cute, but no. It just says V-JEPA can be used for planning. New versions of this do a better job at planning and everything.

Here is an interesting thing. Remember I told you that the way babies learn the world is three-dimensional is because it is the best way to explain how your view of the world changes when you move your head.

We took the representation learned by some version of V-JEPA called V-JEPA 2.1, and then trained a head on top of it to predict depth from a single image. It does a really good job. It produces really good results, in fact better than DINOv3.

That shows that this system, by just being trained to fill in the blanks in videos at a representation level, basically understands, in double quotes, that the world is three-dimensional. It understands the notion of object. If you use the representation as input to a segmentation system, it works decently well, and for various other things.

## Conclusion

Let me conclude.

Abandon generative models. I mean if you work on LLMs, of course, but you should not work on LLMs. At least if you are in academia, you should absolutely not work on LLMs. There is nothing you can bring to the table.

Abandon generative models in favor of joint embedding architectures if you are interested in intelligence.

Abandon probabilistic models in favor of energy-based models. I did not have time to really explain why.

I made an argument in favor of regularized methods, or information maximization through variables instead of samples. So, dimension-contrastive methods rather than sample-contrastive methods, though sample-contrastive methods have many practical applications.

I have been saying forever to abandon reinforcement learning. I do not really mean abandon it. I mean minimize its use because it is so horribly inefficient in terms of sample efficiency.

I know there are people here who work on this, but reinforcement learning is what you do when you are desperate and there is nothing else you can do.

You have to do most of the learning by observation, learning world models, and so on. Once you have good representations, you can use reinforcement learning on top of them because you already have good representations and will not require too many samples. Sometimes you cannot avoid it.

If you are interested in making real progress in AI, in grounded AI, AI for the real world, or physical AI, do not work on LLMs. Do not work on generative models either.

As you can probably guess, this does not make me very popular in Silicon Valley.

As many of you probably know, I left Meta at the end of last year and formed a new company, heard in the transcript as “AMI Labs.” Its purpose is AI for the real world, physical AI. Robotics is a use case, but it is not just that. It is control of industrial processes, anything that is high-dimensional, continuous, and noisy, for which LLMs are completely helpless.

That is the kind of problem we are working on.

That is it. Thank you very much.

*[Applause]*

## Q&A

**Moderator:**

Okay. I know there are many questions. Maybe we will take one or two, but then we have to wrap up. Please, quick questions and quick answers.

**Audience question:**

Thanks for the talk. I wanted to ask about the guardrails that you mentioned on one of the earlier slides, where you also talked about MPC.

Engineers love MPC because they can put in their constraints and describe them in state space, like 3D space. But from what I understand, in your system everything works in representation space.

How do I even get a constraint like “do not bump into the wall” into this representation space? Do you envision the system learning the constraints by itself, or can engineers really put them in?

**Speaker:**

No, you would have to learn a very small head on top of your representation that maps that to the constraint you are interested in. That part has to be trained, but you can train it with a very small number of samples because it is tiny, basically just a projection.

**Audience question:**

But you need a different encoder for each kind of constraint that you might want to put in?

**Speaker:**

Well, you need a different projector for each constraint.

If your task is to open a door, I am not talking about a constraint, I am talking about a task objective. You need some cost function to tell you: is the door open or not? That might have to be trained when you train the system to accomplish the task. But basically, that requires two samples.

**Audience:**

All right. Thanks.

**Moderator:**

Okay. I think we will have to leave it here. Thank you, Yann, very much.

**Speaker:**

All right. Thank you.

*[Applause]*
