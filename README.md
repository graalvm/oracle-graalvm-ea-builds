# Oracle GraalVM Early Access Builds

This repository hosts [Oracle GraalVM](https://graalvm.org) early access builds based on Oracle JDK.

We encourage your feedback and bug reports – please share them in the [Graal repository](https://github.com/oracle/graal).

## Install with SDKMAN!

Oracle GraalVM Early Access builds are available on [SDKMAN!](https://sdkman.io/)
Run the following command to install, for example, the Early Access build of Oracle GraalVM for JDK 24:
```bash
sdk install java 24.ea.3-graal
```
Substitute `24.ea.3` with a preferred release.
To check which GraalVM releases are available for installation, run: 
```bash
sdk list java
```

## Install from an Archive

Download an Oracle GraalVM Early Access build for your platform at [graalvm/oracle-graalvm-ea-builds/releases](https://github.com/graalvm/oracle-graalvm-ea-builds/releases) and install from the archive.

## Use in GitHub Actions

The [GitHub Action for GraalVM](https://github.com/marketplace/actions/github-action-for-graalvm) supports Oracle GraalVM Early Access builds. 
To set up the latest available Early Access build of Oracle GraalVM, set `java-version: 'latest-ea'` in your workflows.
More information is available [here](https://github.com/marketplace/actions/github-action-for-graalvm#options).
