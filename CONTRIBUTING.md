# Contributing to ByteWise Voice

Thanks for your interest! The project is in early development, so things change quickly.

## Before you start

- For anything bigger than a small fix, **open an issue first** so we can agree on the approach.
- Check [DEVELOPMENT_PLAN.md](DEVELOPMENT_PLAN.md) for the architecture and coding standards.

## Contributor License Agreement (CLA)

Before your first pull request can be merged, you'll be asked to sign our CLA. A bot comments on your pull request with a link, and signing takes one click.

**Why:** ByteWise Voice is open source under AGPL-3.0, and the project also offers paid add-ons and commercial licences to fund development. The CLA gives the project the rights it needs to do both. Your contribution always stays available under AGPL-3.0.

## Workflow

1. Fork the repo and create a branch: `feat/short-name` or `fix/short-name`
2. Make your change, with tests
3. Use [Conventional Commits](https://www.conventionalcommits.org/): `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`
4. Open a pull request with a clear description. Add screenshots for UI changes

## Pull request checklist

- [ ] Works on macOS **and** Windows (or explain which one you couldn't test)
- [ ] Tests added or updated, CI is green
- [ ] UI changes checked in dark and light themes, and usable with the keyboard
- [ ] Docs updated if behaviour changed
- [ ] No secrets, model files or voice recordings committed

## Voice recordings

**Never commit recordings of real people's voices**, including your own. Test audio in `tests/fixtures/` must be synthetic or clearly licensed.

## License

By contributing, you agree that your contributions are licensed under the AGPL-3.0 and covered by the CLA.
