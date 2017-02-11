function myFunction() {
    var input, filter, table, tr, td, i;

    input = document.getElementById('name_search');

    filter = input.value.toUpperCase();

    table = document.getElementById('tournament_list_table');
    tr = table.getElementsByTagName("tr");

    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[1];
        if (td) {
            if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
                    tr[i].style.display = "";
            }
            else {
                    tr[i].style.display = "none";
            }
        }
    }
}
