# napari-flicker

## Usage

Start napari with the plugin:

```bash
napari --with napari-flicker 'Flicker Widget'
```

## Development

Start development environment with the following command:

```bash
pixi shell --environment development
```

After updating code in the environment, you can run the tests with:

```bash
pixi run --environment test tox
```

Formatter and linter can be run with:

```bash
pixi run --environment development pre-commit run --all-files
```

## Record of steps taken in initializing the repository

This repository is prepared by the follwowing command:

```bash
gh repo create --private napari-flicker
mkdir napari-flicker
cd napari-flicker
git init
pixi init --format pyproject
# add packages required for napari-plugin-template
echo '\n[tool.pixi.feature.development.dependencies]' >> pyproject.toml
echo '\n[tool.pixi.feature.test.dependencies]' >> pyproject.toml
pixi workspace environment add test --feature test
pixi workspace environment add development --feature development --feature test
pixi add --feature test tox pytest pytest-cov pytest-qt napari
pixi add --feature test --pypi pyqt5 napari
pixi add --feature development copier jinja2-time npe2 pre-commit

git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin git@github.com:amano-takahisa/napari-flicker.git
git push -u origin main
```

Enter to the `development` environment, and run copier

```bash
pixi shell --environment development
copier copy --trust https://github.com/napari/napari-plugin-template tmp
```

Then, set anapari-plugin-template options as follows:

```console
🎤 The name of your plugin, used to name the package and repository
   napari-flicker
🎤 Display name for your plugin in the napari GUI
   Flicker
🎤 Plugin module name, usually the same as the name of the plugin package, but lower
   napari_flicker
🎤 Short description of what your plugin does
   Blinking layers in napari
🎤 Email address
   amano.takahisa@gmail.com
🎤 Developer name
   Taka
🎤 Github user or organisation name
   amano-takahisa
🎤 Github repository URL
   https://github.com/amano-takahisa/napari-flicker
🎤 Include reader plugin?
   Yes
🎤 Include writer plugin?
   Yes
🎤 Include sample data plugin?
   Yes
🎤 Include widget plugin?
   Yes
🎤 Use git tags for automatic versioning?
   Yes
🎤 Install pre-commit? (Code formatting checks)
   Yes
🎤 Install dependabot? (Automatic security updates of dependency versions)
   Yes
🎤 Which licence do you want your plugin code to have?
   Apache Software License 2.0
```

Move necessary files in tmp to the root directory.

```bash
rm -rf src
mv tmp/.github .
mv tmp/.napari-hub .
mv tmp/src .
cat tmp/.gitignore >> .gitignore
mv tmp/.pre-commit-config.yaml .pre-commit-config.yaml
mv tmp/LICENSE LICENSE
mv tmp/MANIFEST.in MANIFEST.in
mv tmp/tox.ini tox.ini
```

And manually merge following files:

```bash
pyproject.toml
README.md
```

remove the tmp directory:

```bash
rm -rf tmp
```

drop black from pre-commit configuration.


format the code:

```bash
git add .
pixi shell --environment development
pre-commit run --all-files
pre-commit run --all-files
```

Finally, commit the changes:

```bash
git add -u
git commit -m "Initialize the napari-flicker plugin"
git push
```
