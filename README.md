![Daratos Logo](https://raw.githubusercontent.com/LostLaser/Daratos/master/logo/logo_100x293.png)

Daratos is a tool to determine the political leaning of a news article that you find on the web. Bias predictions are pulled from [The Bipartisan Press'](https://www.thebipartisanpress.com/) AI.

## Consumer Offerings
You can install the web extension [here](#) (Link to be added later).

## Road Map
  - Web extension for a wide range of browsers
  - Publicly accessible API
  - User labeling of data

## Running The Code
  1. Fork and clone the repository.
  2. Make sure python 3.7 is installed on your machine.
  1. Install dependencies.
     ```
     cd Daratos_API
     pip install -r requirements.txt
     ```
  2. Run the flask api in skeleton mode. Prediction will be turned off in skeleton mode.
     ```
     export PREDICTION_API_KEY="MISSING"
     python app.py runserver
     ```
  3. Add the extension to your browser.
      - [Firefox](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/Temporary_Installation_in_Firefox)
      - [Chrome](https://support.google.com/chrome/a/answer/2714278?hl=en) (Follow the second step)
  4. Navigate to any [supported web page](https://github.com/LostLaser/Daratos/blob/master/supported_sites.md).
  5. Click the extension button near the top right of your browser window.


## Contributing

### Creating a pull request
  - Pull requests are welcome! Please open an issue first to discuss what you would like to change.

### Coding style
  - Try your best to follow the python coding style specified [here](https://realpython.com/python-pep8/).

### Commits
Each commit should have a single purpose. If a commit contains multiple unrelated changes, the changes should be split into separate commits.