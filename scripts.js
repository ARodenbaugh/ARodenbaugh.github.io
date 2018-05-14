$.get("data.csv", function(data){
var html = '<table id = "myTable"; align="center">';
html += "<thead>";
html += "<tr>";
html += "<th style= 'color: rgb(0,20,58); background-color: rgb(189,191,214); font-size:150%;'>Acronym</th>";
html += "<th style= 'color: rgb(0,20,58); background-color: rgb(189,191,214); font-size:150%;'>Stands For</th>";
html += "<th style= 'color: rgb(0,20,58);background-color: rgb(189,191,214); font-size:150%;'>Affiliation</th>";
html += "<th style= 'color: rgb(0,20,58); background:linear-gradient(to right, rgb(189,191,214), rgb(229,230,239)); font-size:150%;'>Description</th>";
html += "</tr>";
html += "</thead>";

var rows = data.split("\n");

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
//insert into div
$('#container').append(html);

});
