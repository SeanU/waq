var animDuration = 1000;

//http://stackoverflow.com/questions/1527803/generating-random-numbers-in-javascript-in-a-specific-range
function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function generateExecSparklineData(min,max){
  var returnArray=[];
  var datePointer = new Date();
  var i=0;
  //off by 1 error here, not sure why
  datePointer = new Date(datePointer.setDate(datePointer.getDate()+1));
  while(i<30){
  
    returnArray.push({
      date:datePointer,
      value:getRandomInt(min,max)
    });

    datePointer = new Date(datePointer.setDate(datePointer.getDate()-1));
    i++;
  }
  return returnArray;
}


//function to pull in data and select column
//not currently working
function chooseDataColumn(col, data) {
  var returnArray=[];

  return returnArray
}



//http://www.tnoda.com/blog/2013-12-19
function sparkline(elemId, data) {

  function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  }

  function prettyPrint(id,value){
    value = numberWithCommas(value);
    if (id.indexOf("cost") > -1){
      return "$"+value;
    }
    else{
      return value;
    }
  }

  data.forEach(function(d){
    d.date = new Date(d.date);
  })

  function getAvg(){
    var sum = 0;
    var avg = 0;
    for(var i=0; i<data.length; i++){
      sum = sum+data[i].value;
      avg = sum/data.length
    }
    return avg.toFixed(2);
  }

  function clickEventHandler(){
    var element = document.getElementById(elemId.replace("#",""));
    var isFlipped = element.getAttribute("data-flipped");
    console.log(element);
      if(!(elemId.indexOf("avgRating") > -1)){

        if(isFlipped === "false"){
          d3.select("#"+"current-path-"+elemId.replace("#","")).transition().duration(animDuration/1.5).style("opacity",0)
          d3.select("#this-spark-circle-"+elemId.replace("#","")).transition().duration(animDuration/1.5).style("opacity",0);
          d3.select("#text-value-"+elemId.replace("#","")).transition().duration(animDuration/1.5).style("opacity",0);

          d3.select(elemId+"-flip-number").transition().delay(animDuration/2).duration(animDuration/2).style("opacity",1);
          d3.select(elemId+"-flip-number-label").transition().delay(animDuration/2).duration(animDuration/2).style("opacity",1);
          d3.select(elemId).attr("data-flipped",true);
        }

        else{
          d3.select("#"+"current-path-"+elemId.replace("#","")).transition().delay(animDuration/1.5).duration(animDuration/2).style("opacity",1)
          d3.select("#this-spark-circle-"+elemId.replace("#","")).transition().delay(animDuration/1.5).duration(animDuration/2).style("opacity",1);
          d3.select("#text-value-"+elemId.replace("#","")).transition().delay(animDuration/1.5).duration(animDuration/2).style("opacity",1);

          d3.select(elemId+"-flip-number").transition().duration(animDuration/1.5).style("opacity",0);
          d3.select(elemId+"-flip-number-label").transition().duration(animDuration/1.5).style("opacity",0);
          d3.select(elemId).attr("data-flipped",false);
        }
      }
  }
  //leave room for the text value to the right
  var width = $(elemId).width()-20;
  var height = $(elemId).height();
  var x = d3.scale.linear().range([width-10, 0]);
  var y = d3.scale.linear().range([height-10, 0]);

  x.domain(d3.extent(data, function(d) { return d.date; }));
  y.domain(d3.extent(data, function(d) { return d.value; }));
  
  var line = d3.svg.line()
               .interpolate("basis")
               .x(function(d) { return x(d.date); })
               .y(function(d) { return y(d.value); });

  var svg = d3.select(elemId)
              .append('svg')
              .attr('width', width)
              .attr("class","sparkline-wrapper-svg")
              .attr('height', height)
              .append('g')
              .attr('transform', 'translate(0, 2)');

  svg.append('path')
     .datum(data)
     .attr('class', 'sparkline')
     .attr("id","current-path-"+elemId.replace("#",""))
     .attr('d', line);

  svg.append('circle')
     .attr('class', 'sparkcircle')
     .attr("id","this-spark-circle-"+elemId.replace("#",""))
     .attr('cx', x(data[data.length-1].date))
     .attr('cy', y(data[data.length-1].value))
     .style("opacity",0)
     .attr('r', 2);  

  var totalLength = d3.select("#current-path-"+elemId.replace("#","")).node().getTotalLength();

  d3.select("#current-path-"+elemId.replace("#",""))
    .attr("stroke-dasharray", totalLength + " " + totalLength)
    .attr("stroke-dashoffset", totalLength)
    .transition()
      .duration(animDuration)
      .ease("linear")
      .attr("stroke-dashoffset", 0);

  d3.select(elemId).append("text")
    .attr("class","text-value")
    .style("opacity","0")
    .attr("id","text-value-"+elemId.replace("#",""))
    .text(prettyPrint(elemId,data[data.length-1].value));

    d3.select("#this-spark-circle-"+elemId.replace("#","")).transition().delay(animDuration).duration(animDuration/1.5).style("opacity",1);
    d3.select("#text-value-"+elemId.replace("#","")).transition().delay(animDuration).duration(animDuration/1.5).style("opacity",1);

  d3.select(elemId).append("text")
    .attr("class","flip-descriptor-tag")
    .attr("id",elemId.replace("#","")+"-flip-number-label")
    .style("opacity","0")
    .text("Avg:")
      .append("text")
      .attr("class","text-flip-number")
      .attr("id",elemId.replace("#","")+"-flip-number")
      .style("opacity","0")
      .text(prettyPrint(elemId,getAvg()));

  d3.select(elemId)
    .attr("data-flipped",false)
    .on("click",clickEventHandler);

}




$( document ).ready(function() {

    sparkline('#sparkline-a-c1', generateExecSparklineData(500,2000));
    sparkline('#sparkline-a-c2', generateExecSparklineData(10,75));
    sparkline('#sparkline-a-c3', generateExecSparklineData(-1,5));
    sparkline('#sparkline-a-c4', generateExecSparklineData(-1,1));
    sparkline('#sparkline-a-c5', generateExecSparklineData(0,10));

    sparkline('#sparkline-b-c1', generateExecSparklineData(500,2000));
    sparkline('#sparkline-b-c2', generateExecSparklineData(10,75));
    sparkline('#sparkline-b-c3', generateExecSparklineData(-1,5));
    sparkline('#sparkline-b-c4', generateExecSparklineData(-1,1));
    sparkline('#sparkline-b-c5', generateExecSparklineData(0,10));
});