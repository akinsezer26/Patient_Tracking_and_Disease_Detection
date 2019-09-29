$("document").ready(function(){
    $("#btnRontgenTahlilAra").click(function(){
        var hastaAdi = $("#hastaAdi").val();
        var hastaSoyAdi = $("#hastaSoyAdi").val();
        var Tarih = $("#Tarih").val();
        var TahlilTipi = "Rontgen"

        $("table tbody").empty();
        $.ajax({
            url: "http://localhost:5000/tahlilAra/",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({"message": [hastaAdi,hastaSoyAdi,Tarih,TahlilTipi]}) 
               }).done(function(data) {
                for(i in data.response){
                        ID = JSON.stringify(data.response[i][0]).replace(/['"]+/g, ''); 
                        Name = JSON.stringify(data.response[i][1]).replace(/['"]+/g, ''); 
                        Surname = JSON.stringify(data.response[i][2]).replace(/['"]+/g, '');
                        Tarih = JSON.stringify(data.response[i][3]).replace(/['"]+/g, ''); 
            
                        var markup = "<tr><td>" + ID + "</td>  <td>" + Name + "</td><td>" + Surname + "</td> <td>" + Tarih + "</td><td><input type='checkbox' name='myCheckbox' id="+"checkbox" + i + "name='myCheckbox' onclick=\"selectOnlyThis(this)\"></td></tr>";
                        $("table tbody").append(markup);
                        }  
         });    
    });

    $("#submitRontgen").click(function(){
      var myCheckbox = document.getElementsByName("myCheckbox");
        var checkedID;
        for(i=0 ; i<myCheckbox.length;i++){
            if(myCheckbox[i].checked)
                checkedID = i;
        }
        var table = document.getElementsByTagName('table')[0];
        var checkedRow = table.rows[checkedID+1];
        var tahlilID = checkedRow.firstChild.textContent;
        var Ad = checkedRow.children[1].textContent;
        var Soyad = checkedRow.children[2].textContent;
        var Tarih = checkedRow.children[3].textContent;

        $.ajax({
            url: "http://localhost:5000/rontgenGir/",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({"message": [tahlilID,Ad,Soyad,Tarih]}) 
               }).done(function(data) {
                    alert("Rontgen Girildi");
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

  function readURLPic(input) {

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