(function() {

var width = 800;

var section_height = 50;
var left_column_width = 0;
var left_column_initial_offset = 200;
var right_column_width = width - left_column_width;

var svg = d3.select("body").append("svg");

svg
  .attr("height", 0)
  .attr("width",  width);

d3.json("normalized_data.json", function(error, data) {
  var section_count = Math.min(50, data.start.length);

  var gene = data.gene;
  var indicies = d3.range(section_count);

  var samples_flat = _.flatten(_.values(data.samples));
  var min = _.min(samples_flat);
  var max = _.max(samples_flat);

  var samples_data = []
  _.each(indicies, function(id) {
    samples_data[id] = _.pluck(data.samples, id)
  })

  var height = section_height * section_count;
  svg.attr("height", height);

  var section_x = d3.scale.linear()
    .domain([min, max])
    .range([left_column_initial_offset, right_column_width])

  var container = svg

  container
    .append("rect")
    .attr("class", "overlay")
    .attr("x", left_column_width)
    .attr("width", right_column_width)
    .attr("height", height)

  var highlights = container.append("g")
  for(var i = 0; i < section_count; i = i + 2) {
    highlights
      .append("rect")
      .attr("y", i * section_height)
      .attr("width", right_column_width)
      .attr("height", section_height)
      .attr("fill", "#aaf")
  }

  var zoomed = function() {
    console.log("zoomed")
    var sections = container.selectAll("g.section").data(indicies)

    sections.enter()
      .append("g")
      .attr("class", "section")
      .attr("transform", function(id, i) { return "translate(0,"+(section_height * id)+")" })

    sections.each(samples)
  }

  var zoom = d3.behavior.zoom()
    .x(section_x)
    .scaleExtent([1, 8])
    .on("zoom", zoomed)

  container.call(zoom)

  var samples = function(id, i) {
    var elem = d3.select(this);

    var label = elem.select("text.label");

    if(label.empty()) {
      elem
        .append("text")
        .attr("class", "label")
        .text(gene[id])
        .attr("y", section_height / 2);
    }

    var samples_group = elem.select("g.samples")
    var right_column

    if(samples_group.empty()) {
      right_column = elem
        .append("g")
        .attr("class", "samples")
        .attr("transform", function(id, i) { return "translate("+left_column_width+",0)" });
    } else {
      right_column = samples_group
    }

    var circles = right_column.selectAll("circle").data(samples_data[id])

    circles.enter()
      .append("circle")
      .attr("r", 3)

    circles
      .attr("cx", section_x)
      .attr("cy", section_height / 2);

    circles.exit()
      .remove()
  };

  zoomed()
})

}());
