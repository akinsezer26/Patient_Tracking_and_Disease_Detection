$("document").ready(function(){
    $("#btnHastaAra").click(function(){
        var hastaAdi = $("#hastaAdi").val();
        var hastaSoyAdi = $("#hastaSoyAdi").val();
        var TC = $("#TC").val();

        $("table tbody").empty();

        $.ajax({
            url: "http://localhost:5000/hastaAra/",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({"message": [hastaAdi,hastaSoyAdi,TC]}) 
               }).done(function(data) {
                for(i in data.response){
                        name = JSON.stringify(data.response[i][0]).replace(/['"]+/g, ''); 
                        Surname = JSON.stringify(data.response[i][1]).replace(/['"]+/g, ''); 
                        Tc = JSON.stringify(data.response[i][2]).replace(/['"]+/g, ''); 
            
                        var markup = "<tr><td>" + name + "</td>  <td>" + Surname + "</td><td>" + Tc + "</td><td><input type='checkbox' name='myCheckbox' id="+"checkbox" + i + "name='myCheckbox' onclick=\"selectOnlyThis(this)\"></td></tr>";
                        $("table tbody").append(markup);
                        }  
         });    
    });

    $("#btnTahlil").click(function(){
        var myCheckbox = document.getElementsByName("myCheckbox");
        var checkedID;
        for(i=0 ; i<myCheckbox.length;i++){
            if(myCheckbox[i].checked)
                checkedID = i;
        }
        var table = document.getElementsByTagName('table')[0];
        var checkedRow = table.rows[checkedID+1];
        var pname = checkedRow.firstChild.textContent;
        var pSurname = checkedRow.children[1].textContent;
        var pTc = checkedRow.children[2].textContent;

        var checkboxRontgen = document.getElementById("checkboxRontgen");
        var checkboxKalp = document.getElementById("checkboxKalp");
        var sikayet = $("#textSikayet").val();

        $.ajax({
            url: "http://localhost:5000/tahlilGir/",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({"message": [pname,pSurname,pTc,checkboxRontgen.checked,checkboxKalp.checked, sikayet]}) 
               }).done(function(data) {
                    alert("Tahlil Girildi");
         });    
    });
});

function selectOnlyThis(id){
    var myCheckbox = document.getElementsByName("myCheckbox");
    Array.prototype.forEach.call(myCheckbox,function(el){
      el.checked = false;
    });
    id.checked = true;
  }


  function readURL(input) {

    if (input.files && input.files[0]) {

            var reader = new FileReader();

            reader.onload = function (e) {
                $('#profil-alt')
                    .attr('src', e.target.result)
                    .width(400)
                    .height(400);
            };

            reader.readAsDataURL(input.files[0]);

            /*reader.onload = function (e) {
                $('#profil-alt')
                    .attr('src', e.target.result)
                    .width(400)
                    .height(400);
            };*/

            //reader.readAsDataURL(input.files[0]);

            var files = input.files[0];
        }
    }