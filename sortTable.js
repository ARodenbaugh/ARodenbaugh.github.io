function sortTable() {
  var selected = document.getElementById("selectedValue").value;
  var table = document.getElementById("myTable");
  var tr = table.getElementsByTagName("tr");
  var rows, switching, i, x, y, shouldSwitch;

  /* SORT BY ACRONYM */
  if (selected=="Acronym"){
    switching = true;
    // loop that continues until no switching has been done
    while (switching) {
      switching = false;
      rows = table.getElementsByTagName("TR");
      // loop through all table rows (except the headers)
      for (i = 1; i < (rows.length - 1); i++) {
        shouldSwitch = false;
        // get the two elements you want to compare
        x = rows[i].getElementsByTagName("TD")[0];
        y = rows[i + 1].getElementsByTagName("TD")[0];
        // check if the two rows should switch
        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
          // if so, mark as a switch and break the loop
          shouldSwitch= true;
          break;
        }
      }
      if (shouldSwitch) {
        // If marked as shouldSwitch, make the switch and set switching to true
        rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
        switching = true;
      }
    }
  }

  /* SORT BY AFFILIATION */
  if (selected == "Affiliation"){
    switching = true;
    // loop that continues until no switching has been done
    while (switching) {
      switching = false;
      rows = table.getElementsByTagName("TR");
      // loop through all table rows (except the headers)
      for (i = 1; i < (rows.length - 1); i++) {
        shouldSwitch = false;
        // get the two elements you want to compare
        x = rows[i].getElementsByTagName("TD")[2];
        y = rows[i + 1].getElementsByTagName("TD")[2];
        // check if the two rows should switch
        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
          // if so, mark as a switch and break the loop
          shouldSwitch= true;
          break;
        }
      }
      if (shouldSwitch) {
        // If marked as shouldSwitch. make the switch and set switching to true
        rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
        switching = true;
      }
    }
  }
}
