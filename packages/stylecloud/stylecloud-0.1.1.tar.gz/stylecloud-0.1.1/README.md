# stylecloud

Generate stylistic wordclouds, including gradients and icon shapes!

stylecloud is a Python package that leverages the popular [word_cloud](https://github.com/amueller/word_cloud) package, adding useful features to create truly unique word clouds!

* Icon shapes for wordclouds (via [Font Awesome](https://fontawesome.com) 5.11.2)
* Support for advanced color palettes (via [palettable](https://jiffyclub.github.io/palettable/))
* Directional gradients w/ the aforementioned palettes.
* Supports reading a file of text, or reading a pre-generated CSV with words and counts.
* Command Line Interface!

This package is a more formal implementation of my [stylistic word cloud project](https://minimaxir.com/2016/05/wordclouds/) from 2016.

## Installation

You can install stylecloud via pip:

```sh
pip3 install stylecloud
```

## Usage

You can use stylecloud in a Python script or as a standalone CLI app.

Python script:

```python
import stylecloud

stylecloud.gen_stylecloud(file_path='constitution.txt')
```

But you can do so much more! You can use the [free Font Awesome icons](https://fontawesome.com/icons?d=gallery&m=free) to change the shape, change the color palette to one from [palettable](https://jiffyclub.github.io/palettable/) for a custom style, change the background color, and, most importantly, add a gradient so the colors flow in a specified direction!

```python
import stylecloud

stylecloud.gen_stylecloud(file_path='constitution.txt',
                          icon_name='fas fa-dog',
                          palette='colorbrewer.diverging.Spectral_11',
                          background_color='black',
                          gradient='horizontal')
```

You can also use the CLI for even faster stylecloud generation! For the simple flag stylecloud above:

```sh
stylecloud --file_path constitution.txt
```

For the more complex dog-gradient stylecloud:

```sh
stylecloud --file_path constitution.txt --icon_name 'fas fa-dog' --palette colorbrewer.diverging.Spectral_11 --background_color black --gradient horizontal
```

### Helpful Parameters

These parameters are valid for both the Python function and the CLI (you can use `stylecloud -h` to get this information as well).

* text: Input text. Best used if calling the function directly.
* file_path: File path of the input text/CSV. Best used on the CLI.
* gradient: Direction of gradient. (if not None, the stylecloud will use a directional gradient) [default: `None`]
* size: Size (length and width in pixels) of the stylecloud. [default: `512`]
* icon_name: Icon Name for the stylecloud shape. (e.g. 'fas fa-grin') [default: `fas fa-flag`]
* palette: Color palette (via palettable) [default: `cartocolors.qualitative.Bold_6`]
* background_color: Background color (name or hex) [default: `white`]
* max_font_size: Maximum font size in the stylecloud. [default: `200`]
* max_words: Maximum number of words to include in the stylecloud. [default: `2000`]
* stopwords: Boolean to filter out common stopwords. [default: `True`]
* output_name: Output file name of the stylecloud. [default: `stylecloud.png`]
* font_path: Path to .ttf file for font to use in stylecloud. [default: uses included Staatliches font]
* random_state: Controls random state of words and colors.

## Helpful Notes

* The primary goal of this package is to create data visualizations of text that provide a unique aesthetic. Word clouds have tradeoffs in terms of a persuasive data visualization, but this is explicitly trying to create a viz that looks cool!
* This package is released as a separate package from `wordcloud` due to the increase in scope and Python dependencies.
* The ideal fonts for generating a good stylecloud are a) bold/high weight in order to increase readability, and b) condensed/low kerning to fit more text. Both of these traits are why [Staatliches](https://fonts.google.com/specimen/Staatliches) is the default font for stylecloud (overriding Droid Sans in the base `word_cloud`).
* You may want to consider doing post-processing after generating a stylecloud: for example, adding color masks, adding perception skew, feed it to a style transfer AI model, etc.
* Due to the size of the included Font Awesome font files, they will not be updated on every new FA release.
* It's recommended to use FA icons which are large with heavy weight; thin icons might constrain the text too much.
* If using the default random-color-sampling method, it's recommended to use a qualitative palette. Inversely, if using a gradient, it's recommended to use a *non*qualitative palette.
  
# To Do

* Support custom font files (e.g. Font Awesome Pro)
* Create an app running stylecloud

## Maintainer/Creator

Max Woolf ([@minimaxir](https://minimaxir.com))

*Max's open-source projects are supported by his [Patreon](https://www.patreon.com/minimaxir) and GitHub Sponsors. If you found this project helpful, any monetary contributions to the Patreon are appreciated and will be put to good creative use.*

## License

MIT

Font Awesome icon font files included per the terms in its [SIL OFL 1.1 License](https://scripts.sil.org/cms/scripts/page.php?site_id=nrsi&id=OFL).

Staatliches font included per the terms in its [SIL OFL 1.1 License](https://scripts.sil.org/cms/scripts/page.php?site_id=nrsi&id=OFL).
