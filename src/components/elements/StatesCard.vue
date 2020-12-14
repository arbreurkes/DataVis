<template>
  <div ref="card">
    <md-button v-if="zoomed" class="md-fab zoom-button" @click="clicked">
      <md-icon>zoom_out</md-icon>
    </md-button>
    <span class="map-title">
        <span :style="statOne === 'DEM_votes' ? 'color:#439AD3;' : 'color:#C63432;'">
          {{ statOne === "election_lead" ? "Republican" : statOne }}</span>
        <span v-if="statOne === 'election_lead' || statTwo !== 'None'">
          vs.
          <span style="color:#439AD3;">
            {{ statOne === "election_lead" ? "Democratic" : statTwo }}
          </span>
        </span>
      {{ statOne === "election_lead" ? "lead " : "" }}during 2020 presidential election
      <md-icon class="info-icon">info
          <md-tooltip md-direction="bottom">Click a state for more details.</md-tooltip>
      </md-icon>
    </span>
    <div :id="'map-' + this.hashCode"></div>
  </div>
</template>
<script>
import * as d3 from "d3";
import {mapGetters} from 'vuex';
import {legendColor} from "d3-svg-legend";
import * as topojson from "topojson-client";

export default {
  name: 'StatesCard',
  props: {
    title: String, // Title of the card.
  },
  data: function () {
    return {
      states: {},
      results: {},
      countyResults: {},
      color: {},
      countyColor: {},
      focusedState: null,
      visibleCounties: [],
      zoomed: false,
      clicked: {},
      stateData: {},
      countyData: {}
    }
  },
  computed: {
    hashCode: function () {
      return window.hashCode(Math.round(Math.random() * 100000) + "")
    },
    statOne: function () {
      return this.getStatOne()
    },
    statTwo: function () {
      return this.getStatTwo()
    }
  },
  watch: {
    statOne: function () {
      this.initializeMap();
    },
    statTwo: function () {
      if (this.statOne) this.initializeMap();
    }
  },
  mounted: function () {
    var that = this;

    this.$nextTick(() => {
      d3.select("body").append("div")
          .attr("id", "state-tt")
          .attr("class", "tooltip")
          .style("opacity", 0);

      d3.json("/data/uscounties.json").then(json => {
        d3.csv("/data/stateData.csv").then(data => {
          d3.csv("/data/countyData.csv").then(countyData => {
            that.states = json;
            that.stateData = data;
            that.countyData = countyData;
            that.results = data.reduce((k, v) => ({...k, [v.state_id]: v}), {})
            that.countyResults = countyData.reduce((k, v) => ({...k, [v.id]: v}), {})

            this.initializeMap();
          });
        });
      });
    })
  },
  methods: {
    ...mapGetters(['getStatOne', 'getStatTwo']),
    initializeMap: function () {
      var that = this;
      var width = this.$refs.card.scrollWidth;
      var height = width / 2.16; // Keep ratio of map.
      var centered;

      var projection = d3.geoAlbersUsa()
          .translate([width / 2, height / 2])
          .scale(width);

      var path = d3.geoPath(projection)

      d3.select('#map-' + that.hashCode).html("")
      var svg = d3.select('#map-' + that.hashCode)
          .append("svg")
          .attr("width", width)
          .attr("height", height + 36)
          .attr("class", "map-svg");

      var div = d3.select("#state-tt")

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

      var sortNumeric = function (a, b) {
        if (a > b) return 1;
        else if (a === b) return 0;
        return -1;
      }
      var statOne = that.stateData.map((x) => parseFloat(x[that.statOne])).sort(sortNumeric);
      var statTwo = that.stateData.map((x) => parseFloat(x[that.statTwo])).sort(sortNumeric);
      var quantileOne = (statOne.length / 4).toFixed(0);
      var quantileTwo = (statTwo.length / 4).toFixed(0);
      var domainOne = [0, statOne[quantileOne], statOne[quantileOne * 2], statOne[quantileOne * 3],
        statOne[statOne.length - 1]];
      var domainTwo = [0, statTwo[quantileTwo], statTwo[quantileTwo * 2], statTwo[quantileTwo * 3],
        statTwo[statTwo.length - 1]];

      var countyStatOne = that.countyData.map((x) => parseFloat(x[that.statOne])).sort(sortNumeric);
      var countyStatTwo = that.countyData.map((x) => parseFloat(x[that.statTwo])).sort(sortNumeric);
      var countyQuantileOne = (countyStatOne.length / 4).toFixed(0);
      var countyQuantileTwo = (countyStatTwo.length / 4).toFixed(0);
      var countyDomainOne = [0, countyStatOne[countyQuantileOne], countyStatOne[countyQuantileOne * 2],
        countyStatOne[countyQuantileOne * 3], countyStatOne[countyStatOne.length - 1]];
      var countyDomainTwo = [0, countyStatTwo[countyQuantileTwo], countyStatTwo[countyQuantileTwo * 2],
        countyStatTwo[countyQuantileTwo * 3], countyStatTwo[statTwo.length - 1]];

      if (that.statOne === "election_lead" && that.statTwo === "None") {
        that.color = that.countyColor = d3.scaleQuantile()
            .domain([0, .40, .45, .5, .55, .60, 1])
            .range(["#C63432", "#E37D71", "#F6BEB6", "#C8DCf1", "#8DBAE2", "#439AD3"]);
      } else if (that.statTwo === "None" && (that.statOne === "DEM_votes" || that.statOne === "dem_votes_%")) {
        that.color = d3.scaleLinear()
            .domain([0, statOne[statOne.length - 1]])
            .range(["#FFFFFF", "#439AD3"]);
        that.countyColor = d3.scaleLinear()
            .domain([0, countyStatOne[countyStatOne.length - 1]])
            .range(["#FFFFFF", "#439AD3"]);
      } else if (that.statOne === "percentageMen" || that.statOne === "percentageWomen") {
        that.color = d3.scaleQuantile()
            .domain(domainOne)
            .range(["#FFFFFF", "#FBD8D2", "#F3B1A7", "#E78A7E", "#D86257", "#C63432"]);
        that.countyColor = d3.scaleQuantile()
            .domain(countyDomainOne)
            .range(["#FFFFFF", "#FBD8D2", "#F3B1A7", "#E78A7E", "#D86257", "#C63432"]);
      } else if (that.statTwo === "None") {
        that.color = d3.scaleLinear()
            .domain([0, statOne[statOne.length - 1]])
            .range(["#FFFFFF", "#C63432"]);
        that.countyColor = d3.scaleLinear()
            .domain([0, countyStatOne[countyStatOne.length - 1]])
            .range(["#FFFFFF", "#C63432"]);
      } else {
        var palette = [["#dedede", "#abc5d6", "#76abcd", "#3f90c5"],
          ["#d3aaa9", "#a297a3", "#70839c", "#3b6e96"],
          ["#c77372", "#99666e", "#695869", "#384a65"],
          ["#b9312f", "#8e2b2d", "#62252b", "#341f29"]];

        that.color = function (value) {
          var x = (x) => {
            if (x < domainOne[1]) return 0;
            else if (x < domainOne[2]) return 1;
            else if (x < domainOne[3]) return 2;
            else return 3;
          }

          var y = (y) => {
            if (y < domainTwo[1]) return 0;
            else if (y < domainTwo[2]) return 1;
            else if (y < domainTwo[3]) return 2;
            else return 3;
          }

          return palette[x(value[0])][y(value[1])];
        }

        that.countyColor = function (value) {
          var x = (x) => {
            if (x < countyDomainOne[1]) return 0;
            else if (x < countyDomainOne[2]) return 1;
            else if (x < countyDomainOne[3]) return 2;
            else return 3;
          }

          var y = (y) => {
            if (y < countyDomainTwo[1]) return 0;
            else if (y < countyDomainTwo[2]) return 1;
            else if (y < countyDomainTwo[3]) return 2;
            else return 3;
          }

          return palette[x(value[0])][y(value[1])];
        }
      }

      var format = function (domain, label) {
        if (that.statOne === "election_lead") {
          var percentageLead = (Math.abs(label - .5) * 200);
          if (percentageLead < 10) return "<10%";
          else if (percentageLead < 20) return "<20%";
          else return "20+%";
        } else if (domain > 10000000) {
          return (parseFloat(label) / 1000000).toFixed(label > 10000000 ? 0 : 1) + "M";
        } else if (domain > 1000000) {
          return (parseFloat(label) / 1000000).toFixed(1) + "M";
        } else if (domain > 10000) {
          return (parseInt(label) / 1000) + "K";
        } else if (domain > 1000) {
          return (parseFloat(label) / 1000).toFixed(1) + "K";
        } else if (domain <= 100 && domain > 10) {
          return (parseFloat(label)).toFixed(label > 10 ? 0 : 1) + "%";
        } else return (parseFloat(label)).toFixed(1) + "%";
      }

      var showStateCounties = function (id) {
        var filterfunc = (x) => {
          var countyId = x.id.toString().replace("county", "");
          return countyId === id ||
              (countyId.length === (id.length + 3) && countyId.substr(0, id.length) === id.toString());
        }

        that.visibleCounties = ([...svg.selectAll("path")._groups[0]]).filter(filterfunc);
        that.visibleCounties.forEach(x => {
          var countyId = x.id.replace("county", "");

          if (that.countyResults[countyId]) {
            var result = that.countyResults[countyId][that.statOne];
            if (that.statTwo !== "None") {
              result = [result, that.countyResults[countyId][that.statTwo]]
            }
            var value = result === "" ? null : true;

            x.style.display = "block";
            if (value) x.style.fill = that.countyColor(result);
            else x.style.fill = "#888888";
          } else {
            x.style.fill = "#888888";
          }
        })
      }

      var clicked = function (d) {
        if (that.focusedState) that.focusedState.style.display = "block";
        that.visibleCounties.forEach(x => {
          x.style.display = "none";
        })

        if (d.target.__data__) {
          var x, y, k;
          var source = d.target.__data__;

          that.focusedState = d.target;
          that.focusedState.style.display = "none";

          if (source && centered !== source) {
            var centroid = path.centroid(source);
            x = centroid[0];
            y = centroid[1];
            k = 3;
            centered = source;
            that.zoomed = true;
          }

          showStateCounties(source.id.toString());
        } else {
          x = width / 2;
          y = height / 2;
          k = 1;
          centered = null;
          that.zoomed = false;
        }

        svg.selectAll("path")
            .classed("active", centered && function () {
              return source === centered;
            });

        svg.transition()
            .duration(750)
            .attr("transform", "scale(" + k + ")translate(" + ((width / 2) - x) + "," + ((height / 2) - y) + ")");
      }
      that.clicked = clicked;

      svg.append("g")
          .selectAll("path")
          .data(topojson.feature(that.states, that.states.objects.counties).features)
          .enter()
          .append("path")
          .attr("d", path)
          .attr("id", function (d) {
            return "county" + d.id;
          })
          .attr("display", "none")
          .style("stroke", "#BBBBBB")
          .style("stroke-width", "1")
          .style("fill", "#888888")
          .on("mouseover", function (d) {
            var source = d.target.__data__;
            var sel = d3.select(d.target);
            sel.moveToFront();
            d3.select(d.target).transition().duration(300)
                .style('stroke', '#000')
                .style('stroke-width', 1.5);
            div.transition().duration(300)
                .style("opacity", 1)
            div.text(that.countyResults[source.id]["county"] !== ""
                ? that.countyResults[source.id]["county"] + ": "
                + format(countyStatOne[countyStatOne.length - 1], that.countyResults[source.id][that.statOne])
                + (that.statTwo !== "None"
                    ? ", " + format(countyStatTwo[countyStatTwo.length - 1], that.countyResults[source.id][that.statTwo])
                    : "")
                : "No Data")
                .style("left", (d.pageX) + "px")
                .style("top", (d.pageY - 30) + "px")
                .style("opacity", 1);
          })
          .on("mouseout", function (d) {
            var source = d.target;
            var sel = d3.select(source);
            sel.moveToBack();
            d3.select(source)
                .transition().duration(300)
                .style('stroke', '#BBB')
                .style('stroke-width', 1);
            div.transition().duration(300)
                .style("opacity", 0);
          })

      svg.append("g")
          .selectAll("path")
          .data(topojson.feature(that.states, that.states.objects.states).features)
          .enter()
          .append("path")
          .attr("d", path)
          .attr("id", function (d) {
            return "state" + d.id
          })
          .style("stroke", "#BBBBBB")
          .style("stroke-width", "1")
          .style("fill", function (d) {
            if (that.results[d.id]) {
              var result = that.results[d.id][that.statOne];
              if (that.statTwo !== "None") {
                result = [result, that.results[d.id][that.statTwo]]
              }
              var value = result === "" ? null : true;

              if (value) return that.color(result);
              return "#888888";
            }

            return "#888888";
          })
          .on("mouseover", function (d) {
            var source = d.target.__data__;
            var sel = d3.select(d.target);
            sel.moveToFront();
            d3.select(d.target).transition().duration(300)
                .style('stroke', '#000')
                .style('stroke-width', 1.5);
            div.transition().duration(300)
                .style("opacity", 1)
            div.text(that.results[source.id]["state"] !== ""
                ? that.results[source.id]["state"] + ": "
                + format(statOne[statOne.length - 1], that.results[source.id][that.statOne])
                + (that.statTwo !== "None"
                    ? ", " + format(statTwo[statTwo.length - 1], that.results[source.id][that.statTwo])
                    : "")
                : "No Data")
                .style("left", (d.pageX) + "px")
                .style("top", (d.pageY - 30) + "px")
                .style("opacity", 1);
          })
          .on("mouseout", function (d) {
            var source = d.target;
            var sel = d3.select(source);
            sel.moveToBack();
            d3.select(source)
                .transition().duration(300)
                .style('stroke', '#BBB')
                .style('stroke-width', 1);
            div.transition().duration(300)
                .style("opacity", 0);
          })
          .on("click", function (d) {
            clicked(d)
          });

      if (that.statTwo === "None") {
        svg.append("g")
            .attr("class", "legendLinear")
            .attr("transform", "translate(" + (width / 2 - 110) + ", " + height + ")");

        var legendLinear = legendColor()
            .shapeWidth(30)
            .cells(6)
            .labels((d) => {
              return format(d.domain[1], that.statOne === "election_lead"
                  ? [0, .41, .46, .5, .55, .61, 1][d.i]
                  : d.generatedLabels[d.i]);
            })
            .labelFormat(d3.format(".2f"))
            .orient('horizontal')
            .scale(that.color);

        svg.select(".legendLinear")
            .call(legendLinear);
      } else {
        var nums = d3.range(16).map(function (d) {
          var x = d % 4;
          var y = Math.floor(d / 4);
          var color = that.color([domainOne[x], domainTwo[y]]);

          return {x: x, y: y, color: color}
        })

        var size = 30;

        var legend = svg.append("g")
            .attr("class", "legendLinear")
            .attr("transform", "translate(" + (width - 220) + ", " + (height - 100) + ") rotate(-135)");

        legend.selectAll("rect")
            .data(nums)
            .enter()
            .append("rect")
            .attr("x", function (d) {
              return d.x * size
            })
            .attr("y", function (d) {
              return d.y * size
            })
            .attr("width", size)
            .attr("height", size)
            .attr("fill", function (d) {
              return d.color;
            });

        legend.append('defs')
            .append('marker')
            .attr('id', 'arrow')
            .attr('legendLinear', [0, 0, 10, 10])
            .attr('refX', 5)
            .attr('refY', 5)
            .attr('markerWidth', 10)
            .attr('markerHeight', 10)
            .attr('orient', 'auto-start-reverse')
            .append('path')
            .attr('d', d3.line()([[0, 0], [0, 10], [10, 5]]))
            .attr('stroke', 'black');

        legend.append('path')
            .attr('d', d3.line()([[0, 0], [0, 120]]))
            .attr('stroke', 'black')
            .attr('marker-end', 'url(#arrow)')
            .attr('fill', 'none');

        legend.append("text")
            .attr("y", 14)
            .attr("x", -60)
            .attr('text-anchor', 'middle')
            .attr("class", "myLabel")
            .text(that.statOne)
            .attr("transform", "rotate(-180)");

        legend.append('path')
            .attr('d', d3.line()([[0, 0], [120, 0]]))
            .attr('stroke', 'black')
            .attr('marker-end', 'url(#arrow)')
            .attr('fill', 'none');

        legend.append("text")
            .attr("y", 14)
            .attr("x", 60)
            .attr('text-anchor', 'middle')
            .attr("class", "myLabel")
            .text(that.statTwo)
            .attr("transform", "rotate(90)");
      }
    }
  }
};
</script>
<style scoped>
.zoom-button {
  top: 48px;
  right: 0;
  position: absolute;
  background-color: var(--mdc-theme-secondary) !important;
}
</style>
<style>
.map-svg {
  margin: 0 auto;
}

.map-title {
  display: inline-block;
  width: 100%;
  text-align: center;
  font-size: 12pt !important;
}

.label {
  line-height: 8pt;
  font-size: 8pt;
}

div.tooltip {
  position: absolute;
  left: 75px;
  text-align: center;
  height: 36px;
  line-height: 16px;
  padding: 10px;
  font-size: 14px;
  background: #FFFFFF;
  border: 1px solid #989898;
  pointer-events: none;
}
</style>