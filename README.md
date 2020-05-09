![Daratos Logo](https://raw.githubusercontent.com/LostLaser/Daratos/master/logo/logo_100x293.png)

Daratos is a tool to determine the political leaning of a news article that you find on the web. Bias predictions are pulled from [The Bipartisan Press'](https://www.thebipartisanpress.com/) AI.

[![Build Status](https://dev.azure.com/jtgolds6/Daratos/_apis/build/status/Daratos-API%20Docker%20container-CI?branchName=master)](https://dev.azure.com/jtgolds6/Daratos/_build/latest?definitionId=3&branchName=master)

## Consumer Offerings
You can install the chrome web extension [here](https://chrome.google.com/webstore/detail/daratos/fkaiddmagelkbjnnjcnekcnohmkbplkb).

## Road Map
  - Web extension for a wide range of browsers
  - Publicly accessible API
  - User labeling of data

## Running The Code
  1. Fork and clone the repository.
  1. Make sure python 3.7 is installed on your machine.
  1. Install dependencies.
     ```
     cd Daratos_API
     pip install -r requirements.txt
     ```
  1. Run the flask api in skeleton mode. Prediction will be turned off in skeleton mode.
     ```
     export PREDICTION_API_KEY="MISSING"
     python app.py runserver
     ```
  1. Add the extension, located under Daratos_EXT, to your browser.
      - [Firefox](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/Temporary_Installation_in_Firefox)
      - [Chrome](https://support.google.com/chrome/a/answer/2714278?hl=en) (Follow the second step)
  1. Navigate to any news article.
  1. Click the extension button near the top right of your browser window.


## Contributing
### Coding style
- Try your best to follow the python coding style specified [here](https://realpython.com/python-pep8/).

### Commits
- Each commit should have a single purpose. If a commit contains multiple unrelated changes, the changes should be split into separate commits.

### Testing
- Code should pass all tests before a pull requst is made for the API
  - Running the test suite:
    1. Switch to the API folder (Daratos_API)
    1. Run this command: ```pytest```
    1. Correct any errors that may have shown up

### Creating a pull request
- Pull requests are welcome! Please open an issue first to discuss what you would like to change.
