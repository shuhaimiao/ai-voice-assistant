# Effective Prompting Guide for AI Collaboration

## Best Practices for Working with Trae AI

1. **Be Specific**: Clearly state your goals, requirements, and constraints
2. **Provide Context**: Share relevant code snippets, error messages, or background information
3. **Break Down Tasks**: Divide complex problems into smaller, manageable steps
4. **Iterate**: Start with simple implementations and refine based on results
5. **Use Examples**: Provide sample inputs/outputs when possible

## Prompt Structure Recommendations

```
[Context/Background]
<Provide relevant information about the project>

[Current State]
<Describe what currently exists or what you've tried>

[Goal]
<Clearly state what you want to achieve>

[Constraints]
<List any limitations or requirements>

[Examples]
<Provide sample inputs/outputs if applicable>
```

## Documentation Strategy

- Use `docs/features` for detailed specifications
- Use `docs/guidelines` for coding standards
- Keep README.md for high-level overview
- Create separate markdown files for major features

## Development Workflow

1. **Requirement Elaboration**:
   - Create feature documents
   - Define acceptance criteria

2. **Design Brainstorming**:
   - Document design decisions
   - Create architecture diagrams

3. **Task Breakdown**:
   - Create work breakdown structure
   - Estimate complexity

4. **Implementation**:
   - Implement smallest viable feature first
   - Iterate based on feedback

## Example Prompts

"I'm implementing text-to-speech conversion. Currently I have a basic Python script that prints text. I want to convert text to speech using Coqui XTTS v2. The input is a string, output should be a WAV file. Can you help implement the core TTS function?"

"I need to set up voice cloning. I have 3 voice samples in WAV format. How should I structure the data loading and model initialization for Coqui XTTS v2's voice cloning feature?"