(function() {

var section_height = 100;
var section_scale = d3.scale.ordinal();
var left_column_width = 80;

var width = 800

var svg = d3.select("body").append("svg");

svg
  .attr("height", 0)
  .attr("width",  width)

d3.json("normalized_data.json", function(error, json) {
  window.input_data = json
  var section_count = json.start.length

  var gene = json.gene
  var indicies = d3.range(section_count)

  svg.attr("height", section_height * section_count)

  function samples(id, i) {
    d3.select(this)
      .append("text")
      .text(gene[id])
      .attr("y", section_height / 2)
      .append("g")
      .attr("transform", function(id, i) { return "translate("+left_column_width+",0)" })
  }

  svg.selectAll("g.sample")
    .data(indicies)
    .enter()
      .append("g")
      .attr("class", "sample")
      .attr("transform", function(id, i) { return "translate(0,"+(section_height * id)+")" })
      .each(samples)
})

}());
