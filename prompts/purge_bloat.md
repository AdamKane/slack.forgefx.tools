This prompt is about finding unused code in our project and nuking it. This is typically referred to 
as "purging bloat" by me, but gennerally referred to as "dead code elimination" by others.

The goal is to find code that is no longer used by the project.

The prompt should output a numbered list of files that are candidates for removal, along with a brief explanation
of why they are candidates for removal.

Here's the the prompt to our AI coding assistant:

----


```
Please review the entire (@codebase) codebase and output a numbered list of files that are candidates for removal.
For each file, please provide a brief explanation of why it is a candidate for removal.

In other words, please perform a holistic review of the codebase, and identify files that are no longer used by the project.

Some things to consider when purging bloat:

- Is the file necessary?
- Does anything reference the file?
- Is the file used by an integration?
- Is the file used by a test?
- Is the file used by an example?
- Is the file used by a demo?
- Is the file used by a tutorial?
- Is the file used by a blog post?
- Is the file used by a book?
- Is the file used by a video?

If a file is used by only one or two things, maybe there's a way to refactor the codebase to eliminate the file?
```






