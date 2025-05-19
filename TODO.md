# Release TODO List for linalg CLI Tool

## Package Structure
- [ ] Verify package structure follows standards
- [ ] Ensure all required files are present (README.md, LICENSE, etc.)
- [ ] Confirm the entry point in pyproject.toml is correctly defined

## Packaging Information
- [ ] Add author information to pyproject.toml
- [ ] Add license information (and create LICENSE file)
- [ ] Add project URL (GitHub/GitLab repository)
- [ ] Add classifiers for development status, intended audience, etc.
- [ ] Add keywords for better discoverability

## Version Management
- [ ] Implement semantic versioning scheme
- [ ] Create CHANGELOG.md to track changes between versions
- [ ] Set up automated version bumping process

## CLI Entry Point Configuration
- [ ] Verify CLI entry point is properly configured
- [ ] Test invocation via CLI name (`linalg`) after installation
- [ ] Consider adding shell completions for better user experience

## Documentation
- [ ] Expand documentation with more detailed examples
- [ ] Add installation instructions (pip, pipx)
- [ ] Consider creating a documentation site

## Testing for Distribution
- [ ] Create test environment to verify package installation
- [ ] Test installation via pip
- [ ] Test installation via pipx
- [ ] Test on different operating systems if targeting multiple platforms

## PyPI Account Setup
- [ ] Create an account on PyPI (Python Package Index)
- [ ] Set up API tokens for automated publishing
- [ ] Configure credentials securely for CI/CD if applicable

## Build and Release Process
- [ ] Set up build process using build tools
- [ ] Create distribution packages (wheel and sdist)
- [ ] Test uploading to TestPyPI first
- [ ] Upload packages to PyPI
- [ ] Set up continuous deployment for future releases

## pipx Compatibility
- [ ] Ensure the tool works well with pipx (isolated environment)
- [ ] Test pipx installation specifically
- [ ] Document pipx installation instructions

## Post-Release
- [ ] Monitor for any issues after release
- [ ] Be ready to quickly deploy fixes if needed
- [ ] Gather user feedback for future improvements

## CI/CD Enhancements (Optional)
- [ ] Set up CI/CD pipeline for automated testing and releases
- [ ] Configure testing across multiple Python versions
- [ ] Add release automation to deploy on version tag creation