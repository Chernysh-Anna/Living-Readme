# General Documentation Standards

## Team Documentation Principles

All documentation in this project must adhere to our team's standards of **clarity** and **brevity**.

### Clarity

- **Use simple, direct language** - Avoid jargon unless necessary
- **Be specific** - Provide concrete examples over abstract descriptions
- **Structure logically** - Use headings, lists, and sections to organize information
- **Define terms** - Explain technical concepts when first introduced
- **Show, don't just tell** - Include code examples, diagrams, or screenshots where helpful

### Brevity

- **Get to the point** - Lead with the most important information
- **Remove redundancy** - Say things once, say them well
- **Use concise sentences** - Prefer active voice and short paragraphs
- **Eliminate filler** - Every sentence should add value
- **Link instead of repeating** - Reference existing documentation rather than duplicating it

### Documentation Types

#### README Files
- Start with a clear one-sentence description
- Include a quick start section within the first few paragraphs
- Use visual hierarchy (headings, lists, code blocks)
- Keep the main README focused; link to detailed docs

#### Code Comments
- Explain *why*, not *what* (code shows what)
- Document non-obvious decisions and gotchas
- Keep comments up-to-date with code changes
- Use docstrings for public APIs

#### Technical Specifications
- Define scope and objectives clearly
- Use diagrams for complex architectures
- Include decision rationale
- Keep specifications current

### Quality Checklist

Before committing documentation, verify:

- [ ] Can a new team member understand this in 5 minutes?
- [ ] Have I removed all unnecessary words?
- [ ] Are examples concrete and runnable?
- [ ] Is the structure logical and scannable?
- [ ] Have I linked to related documentation?

### Examples

**❌ Poor (Verbose, Unclear):**
```markdown
In order to get the application up and running on your local development 
environment, you will need to first make sure that you have installed all 
of the necessary dependencies that are required by the application, and 
then you can proceed to start the development server.
```

**✅ Good (Clear, Brief):**
```markdown
## Quick Start

1. Install dependencies: `npm install`
2. Start dev server: `npm run dev`
```

---

*These standards apply to all documentation: README files, code comments, technical specs, and inline documentation.*