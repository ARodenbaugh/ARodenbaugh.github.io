$.get("data.csv", function(data){
var html = '<table id = "myTable"; align="center">';
// add header elements
html += "<thead>";
html += "<tr>";
html += "<th style= 'color: rgb(0,20,58); background-color: rgb(189,191,214); font-size:180%;'>Acronym</th>";
html += "<th style= 'color: rgb(0,20,58); background-color: rgb(189,191,214); font-size:180%;'>Stands For</th>";
html += "<th style= 'color: rgb(0,20,58);background-color: rgb(189,191,214); font-size:180%;'>Affiliation</th>";
html += "<th style= 'color: rgb(0,20,58); background:linear-gradient(to right, rgb(189,191,214), rgb(229,230,239)); font-size:180%;'>Description</th>";
html += "</tr>";
html += "</thead>";

// get rows from csv
var myrows = data.split("\n");

// get rid of trailing row in CSV before making table
rows = myrows.slice(0, -1);

// add each row to the table
rows.forEach(function getvalues(ourrow){

  html += "<tr>";

  var columns = ourrow.split(":");

  html += "<td style= 'color: rgb(7,5,77)'><b>" + columns[0] + "</b></td>";
  html += "<td style= 'color: rgb(7,5,77)'>" + columns[1] + "</td>";
  html += "<td style= 'color: rgb(7,5,77)'>" + columns[2] + "</td>";
  html += "<td style= 'color: rgb(7,5,77)'>" + columns[3] + "</td>";
  //close row
  html += "</tr>";
})
// close table
html += "</table>";


// add row colors
//html +="<style> table tr:nth-child(even) {background:linear-gradient(to right, rgb(189,191,214),rgb(189,191,214),rgb(189,191,214), rgb(229,230,239));}</style>";
//html +="<style> table tr:nth-child(odd) {background-color: rgb(225,226,231);}</style>";

//insert into div
$('#container').append(html);

});
