# Contributing to MEDF

MEDF is a protocol focused on fixing document states,
not on judging correctness or authority.

Before proposing changes, please read 思想.md.

## Principles

- **No online dependency required** - Everything must work offline
- **No central authority assumed** - No servers, no APIs needed
- **No semantic normalization** - YAML/Markdown are derivatives, not canonical
- **Offline verification must remain possible** - Hash verification must work locally

Changes that violate these principles will not be accepted.

## How to contribute

### Issues

- Use GitHub Issues for discussion
- Clearly explain the problem or proposal
- Reference relevant principles from 思想.md

### Pull Requests

1. **Read 思想.md first** - Understand our philosophy
2. **Keep implementations minimal** - Less code is better
3. **Provide clear rationale** - Explain why the change is needed
4. **Follow existing patterns** - Match the codebase style

### Areas of contribution

- **Bug fixes** - Corrections to existing functionality
- **Documentation** - Improvements to clarity and completeness
- **Schema updates** - With strong justification and backward compatibility
- **CLI tools** - New features must be offline-first

### What we don't want

- Online dependencies (servers, APIs, databases)
- Complex abstractions beyond what's necessary
- "Convenience" features that violate core principles
- YAML/Markdown as canonical formats
- Semantic normalization or interpretation

## License

Any contribution you make will be under the MIT License, just like the project itself.

## Thank you

Contributions that align with our principles are welcome!
