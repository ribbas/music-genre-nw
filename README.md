# Music Genre Network Graph

Network graph of music genres and their origins and subgenres scraped off
Wikipedia. The network graph is constructed in a hierarchical layout to
demonstrate origin-subgenre relationships.

## Data

Initially, the list of genres only consisted of heavy metal subgenres as an
attempt to remind [metal elitists](https://www.urbandictionary.com/define.php?term=Metal%20Elitist) of
the origins of such a majestic music genre. Once realized the roots of many of
the subgenres existed beyond the scope of heavy metal, such as jazz fusion and
blues, an attempt was made to analyze all the music genres off Wikipedia.

![wiki table](https://raw.githubusercontent.com/sabbirahm3d/music-genre-nw/master/static/img/wiki-table.png)

<sub>Wikipedia tables used for scraping relationships between genres</sub>

The subgenres were obtained in an iterative [dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming) method and therefore did not require extensive [scraping](https://towardsdatascience.com/ethics-in-web-scraping-b96b18136f01).

## Graph

Each genres were scraped for their origins and subgenres to construct their
individual subtrees. These subtrees determined the edges required to
constructed the directed graph. Once constructed, the positions of the network
graph nodes were generated to draw in a [force-directed hierarchical layout](https://graphviz.gitlab.io/_pages/pdf/dotguide.pdf).

[Graphviz](http://www.graphviz.org/) was used to generate the positions for the
hierarchical layout of the network graph, and [Plotly](https://plot.ly/) was
used to visualize the data.

## Disclaimer

The relationships between the genres were determined by the data collected from
Wikipedia. It is known that Wikipedia can be highly
subjective, but it is [generally accurate on high level](https://www.zmescience.com/science/study-wikipedia-25092014/). This graph
should not be used in an argument to classify artists, albums or singles. Also, no one likes a [gatekeeper](https://www.reddit.com/r/gatekeeping/)!
