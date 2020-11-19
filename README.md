# Week 12 — HTML Applications

## Lecture

* [Slide deck](https://docs.google.com/presentation/d/1CZHQXWWaJZm0-m2fXatV-bgE41qVSu4YqPtpZFNFhG8/edit?usp=sharing)
* [form_app.py](form_app.py)
* [app.py](app.py)

## Lab

* [Writeup](Lab.md)
* Flask App
  * [`lab_app.py`](lab_app.py)
  * Template Files:
    * [`templates/lab_input.html`](templates/lab_input.html)
    * [`templates/whereami.html`](templates/whereami.html)
    * [`templates/point_map.html`](templates/point_map.html)

## Lecture Outline

1. How're project proposals doing?
   * Any project pieces that you need help with?
     * Interactive or static graphs?
2. Where we're going (update)
   * This week: HTML pages with goodies
   * Next week and week following: AWS EC2 — setting up a cloud-based server
3. HTML Forms
   * What are they? A collection of HTML components that take in user input: text, check boxes (true/false), selections from a list, etc. They're much more user-friendly than typing query parameters into a browser address bar
   * What do they do? Take user input and send it to whatever is specified by `action`. In the Codecademy Forms lesson, the submit button didn't actually forward along any data, it just went to a new page.
   * Where is the data sent when we hit 'submit'?
     * Form elements each have data that is sent to the `action` endpoint in the form of `name=value` pairs
   * What are the components?
     * `text`,
   * Structure: `name`, `type`, `value`
   * How do they integrate with Flask or JavaScript?
4. Architecture of an HTML application
   * Show diagram — API call, fetching and processing of data, calling template, filling in template, sending output to browser
   * What to do if an error occurs?
5. Additional Flask things
   * Response class — Body, status code, content type
6. HTML Goodies
   * Install `matplotlib` and `bokeh`
   * Create a static image and insert into page
     * Great example: <https://stackoverflow.com/a/50728936/3159387>
     * Another (with idea of different file formats): <https://gist.github.com/illume/1f19a2cf9f26425b1761b63d9506331f>
   * Interactive chart
     * Quite complicated but it has the core essentials: <https://towardsdatascience.com/https-medium-com-radecicdario-next-level-data-visualization-dashboard-app-with-bokeh-flask-c588c9398f98>
     * Another example (using Bokeh, but not very pretty): <https://www.fullstackpython.com/blog/responsive-bar-charts-bokeh-flask-python-3.html>
     * Another bokeh example: <https://medium.com/@n.j.marey/my-experience-with-flask-and-bokeh-plus-a-small-tutorial-7b49b2e38c76>


## Recommended Readings

* [HTML Forms explained (Mozilla)](https://developer.mozilla.org/en-US/docs/Learn/Forms/Your_first_form)
