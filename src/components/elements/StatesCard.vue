<template>
  <div ref="card">
    <span class="map-title">
          <span style="color:#C63432;">Republican</span> vs. <span style="color:#439AD3;">Democratic</span> lead in 2020 presidential election
        </span>
    <div :id="'map-' + this.hashCode"></div>
  </div>
</template>
<script>
import * as d3 from "d3";
import {mapActions, mapGetters} from 'vuex';
import {legendColor} from "d3-svg-legend";
import * as topojson from "topojson-client";

export default {
  name: 'StatesCard',
  props: {
    title: String, // Title of the card.
    size: String, // Size of card in gutter.
    inGrid: Boolean, // Is this card in gutter?
    stats: Object, // Statistics
  },
  data: function () {
    return {
      states: {},
      results: {}
    }
  },
  computed: {
    hashCode: function () {
      return window.hashCode(Math.round(Math.random() * 100000) + "")
    }
  },
  mounted: function () {
    this.$nextTick(() => {
      this.initializeMap()
    })
  },
  methods: {
    ...mapActions([]),
    ...mapGetters([]),
    initializeMap: function () {
      var that = this;
      var width = this.$refs.card.scrollWidth;
      var height = width / 2.16; // Keep ratio of map.

      var projection = d3.geoAlbersUsa()
          .translate([width / 2, height / 2])
          .scale([width]);

      var path = d3.geoPath(projection)

      var color = d3.scaleQuantile()
          .domain([0, .40, .45, .5, .55, .60, 1])
          .range(["#C63432", "#E37D71", "#F6BEB6", "#C8DCf1", "#8DBAE2", "#439AD3"]);

      var svg = d3.select('#map-' + that.hashCode)
          .append("svg")
          .attr("width", width)
          .attr("height", height + 36)
          .attr("class", "map-svg");

      var div = d3.select("body").append("div")
          .attr("id", "state-tt")
          .attr("class", "tooltip")
          .style("opacity", 0);

      d3.selection.prototype.moveToFront = function () {
        return this.each(function () {
          this.parentNode.appendChild(this);
        });
      };

      d3.selection.prototype.moveToBack = function () {
        return this.each(function () {
          var firstChild = this.parentNode.firstChild;
          if (firstChild) {
            this.parentNode.insertBefore(this, firstChild);
          }
        });
      };

      d3.json("/data/uscounties.json").then(json => {
        that.states = json;

        d3.csv("/data/stateData.csv").then(data => {
          that.results = data.reduce((k, v) => ({...k, [v.state_id]: v}), {})

          svg.selectAll("path")
              .data(topojson.feature(that.states, that.states.objects.states).features)
              .enter()
              .append("path")
              .attr("d", path)
              .attr("id", function (d) {
                return d.id
              })
              .style("stroke", "#FFF")
              .style("stroke-width", "1")
              .style("fill", function (d) {
                if (that.results[d.id]) {
                  var result = that.results[d.id]["normalized_election_outcome"];
                  var value = result === "" ? null : result > .5 ? "DEM" : "REP";

                  if (value) return color(result);
                  return "#888";
                }

                return "#888";
              })
              .on("mouseover", function (d) {
                var sel = d3.select(this);
                sel.moveToFront();
                d3.select(this).transition().duration(300)
                    .style('stroke', '#000')
                    .style('stroke-width', 1.5);
                div.transition().duration(300)
                    .style("opacity", 1)
                div.text(that.results[this.id]["state"] !== ""
                    ? that.results[this.id]["state"] : "No Data")
                    .style("left", (d.pageX) + "px")
                    .style("top", (d.pageY - 30) + "px")
                    .style("opacity", 1);
              })
              .on("mouseout", function () {
                var sel = d3.select(this);
                sel.moveToBack();
                d3.select(this)
                    .transition().duration(300)
                    .style('stroke', '#FFF')
                    .style('stroke-width', 1);
                div.transition().duration(300)
                    .style("opacity", 0);
              });
        });
      });

      svg.append("g")
          .attr("class", "legendLinear")
          .attr("transform", "translate(" + (width / 2 - 110) + ", " + height + ")");

      var legendLinear = legendColor()
          .shapeWidth(30)
          .cells(6)
          .labels(["20+%", ">20%", ">10%", ">10%", ">20%", "20+%"])
          .orient('horizontal')
          .scale(color);

      svg.select(".legendLinear")
          .call(legendLinear);
    }
  }
};
</script>
<style scoped>

.actions {
  justify-content: center !important;
}
</style>