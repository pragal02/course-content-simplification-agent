# Course Content Simplification Agent

## Problem Statement

Academic course materials often contain complex technical terminology and explanations that may be difficult for students with different levels of prior knowledge.

## Proposed Solution

The Course Content Simplification Agent uses IBM Granite through IBM watsonx.ai to transform academic content into explanations suitable for the learner's selected proficiency level.

## Core Prompt Logic

The system accepts course content and a proficiency level:

- Beginner
- Intermediate
- Advanced

The model adjusts vocabulary, depth, examples, and technical detail according to the selected level while preserving important technical meaning.

## Expected Output

1. Simplified Explanation
2. Key Concepts
3. Important Terms and Definitions
4. Example or Analogy
5. Short Summary
6. Quick Questions

## Technology

IBM watsonx.ai  
IBM Granite Foundation Model  
Prompt Engineering  
Generative AI

## Project Implementation

The working prototype was created and tested in IBM watsonx.ai using a Granite foundation model. The saved prompt provides the course content and learner proficiency level as inputs and generates a structured explanation.

## Sample Input

Topic: Computer Networks

Content: A computer network is a collection of interconnected devices that communicate and share resources using communication protocols.

Learner Level: Beginner

## Sample Expected Output

### Simplified Explanation
A computer network is a group of connected devices such as computers, phones, and servers that can communicate and share information.

### Key Concepts
- Connected devices
- Communication
- Resource sharing
- Network protocols

### Example
A college Wi-Fi network connects student laptops and phones so they can access the internet and other shared services.

### Summary
A computer network allows connected devices to communicate and share resources.

### Quick Questions
1. What is a computer network?
2. Why are devices connected in a network?

## Result

The prototype demonstrates that IBM Granite can generate level-appropriate explanations of academic content while maintaining the important technical concepts.
