function searchTable() {
  var input, filter, table, tr, td, i, count, array;
  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  count = 0;
  array = [];
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[0];
    // if letters exists in acronym, display that entry
    if (td) {
      if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
        array.push(tr[i]);
        // hide entries that don't match search
      } else {
        tr[i].style.display = "none";
        count++;
      }
    }
    // Display no results found if display is blank
    if(count == tr.length-1){
      document.getElementById('output').innerHTML = '<i>No results found.</i>';
      //document.getElementById('mycount').innerHTML = count;
    }
    else{
      document.getElementById('output').innerHTML = '';
    }
  }

  // Color every even row
  for (j=0; j<array.length+1; j++){
  	if (j % 2 == 0){
    	array[j].style.backgroundColor = "rgb(225,226,231)";
    }
    else{
    	array[j].style.backgroundColor = "rgb(189,191,214)";
    }
  }
}
