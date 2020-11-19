# Week 12 Lab — HTML Applications

Let's build some applications using the same format we've been using so far:

```
├── app.py
├── mapbox_token.json
├── pg-credentials.json
├── static
│   ├── css
│   │   ├── normalize.css
│   │   ├── skeleton.css
│   │   └── style.css
│   └── images
│       └── favicon.png
└── templates
    ├── lab_input.html
    ├── point_map.html
    └── whereami.html
```

Our goal: Build a geocoding app like Google Maps!

For this, we'll use Mapbox's Geocoding API which we've used before.

We will be building to API endpoints:

1. `/` for the landing page
2. `/whereami` for the page displaying the geocoding results and a map

## 0. Let's look at things

* lab_app.py — endpoints, variables available, etc.
* HTML files — structure of page, variables expected


## 1. Hooking up the HTML form to the API

The [`templates/lab_input.html`](templates/lab_input.html) file has a basic text entry form and a submit button.

The [`lab_app.py`](lab_app.py) file has a few API endpoint sketched out.

**Tasks**

1. In the `lab_input.html` file, update the endpoint in the `action` attribute to point to the correct API endpoint.
2. In `lab_app.py`, fix the line in the `whereami` function so that the query string is correctly parsed and an address is passed to the Python environment.

Run the server `python lab_app.py` and try out some different address, place names, etc.

## 2. Return a webpage

Instead of returning the raw GeoJSON, let's template in some of the information in the GeoJSON object.


1. Let's parse out the **longitude** and **latitude** from the GeoJSON.
   1. Complete this line of code to get the longitude and latitude. There are a couple of more `['key']` or `[index]` items to put on the end of the `resp.json()` to get to the `longitude` and `latitude`. Look at the structure of the GeoJSON returned from the API response above.
      ```python
      lng, lat = resp.json()['']
      ```
2. Modify the `return resp.json()` line and replace with this:
   ```python
   return render_template('whereami.html', lng=lng, lat=lat, address=address)
   ```

## 3. Let's add the map!

Now that we have the lng/lat parsed out, let's add the map to the HTML page. There's a placeholder in `templates/whereami.html` for the HTML document that we'll build. Notice the line in `templates/whereami.html` near the end:

```HTML
{{ html_map | safe }}
```

This is where we can place the HTML map. The HTML map template is in `templates/point_map.html`. Let's take a look at it. By itself, this snippet of HTML and JavaScript won't work, but when embedded in `templates/whereami.html`, the Map has a location to go to (`<div id="map"></div>`).

1. What variables is the `whereami.html` expecting in the template?
2. Alter the return value of the `whereami` function by giving it a new argument `html_map` and setting it equal to the `render_template()` function with the `whereami.html` file as the template, and filling in the appropriate variables that the template is expecting.


## 4. Let's give users more options for exploring the map

Let's provide some pre-canned addresses by making a drop down selector.

```HTML
<select name="address-dropdown" id="pre-selected-addresses">
  <option value="Meyerson Hall, University of Pennsylvania">Meyerson Hall, University of Pennsylvania</option>
  <option value="Temple of Heaven, Beijing, China">Temple of Heaven, Beijing, China</option>
</select>
```

1. Add a couple more `<option>` tags like below and place within the form on the `templates/lab_input.html` page.
2. Modify the `whereami` function on how it parses the form results. Notice that the dropdown has a different `name`.
