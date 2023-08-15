$('.upd-data').click(function(){
    var userId = $(this).attr('uid')
    var doe = $(this).attr('doe')
    $.ajax({
        type: 'GET',
        url: "/update-datapg",
        contentType: 'application/json;charset=UTF-8',
        data: {'userId':userId, 'doe':doe},
        success: function(data,status){
            var userdetails = JSON.parse(data);
            if(userdetails.length > 0){
                $('#hide-dtable').hide();
                $('#hide-dttile').hide();
                document.getElementById('show-utitle').style.display = 'block';
                document.getElementById('show-uform').style.display = 'block';
                $('#dincome').val(userdetails[0][1]);
                $('#damts').val(userdetails[0][2]);
                $('#dtax').val(userdetails[0][3]);
                $('#dexp').val(userdetails[0][4]);
                $('#ddoe').val(userdetails[0][5]);
                $('#dcomment').val(userdetails[0][6]);
                $('#duserid').val(userdetails[0][0]);
            }
            else{
                alert('Error');
            }
        }
    });
});

$('.upd-plan').click(function(){
    var puid = $(this).attr('puid')
    var pdoe = $(this).attr('pdoe')
    $.ajax({
        type: 'GET',
        url: "/update-planpg",
        contentType: 'application/json;charset=UTF-8',
        data: {'puid':puid, 'pdoe':pdoe},
        success: function(data,status){
            var userplandetails = JSON.parse(data);
            if(userplandetails.length > 0){
                $('#hide-ptitle').hide();
                $('#hide-ptable').hide();
                document.getElementById('show-ptitle').style.display = 'block';
                document.getElementById('show-pform').style.display = 'block';
                $('#pincome').val(userplandetails[0][1]);
                $('#pamounts').val(userplandetails[0][2]);
                $('#ptax').val(userplandetails[0][3]);
                $('#pexp').val(userplandetails[0][4]);
                $('#pdoe').val(userplandetails[0][5]);
                $('#pcomments').val(userplandetails[0][6]);
                $('#puserid').val(userplandetails[0][0]);
            }
            else{
                alert('Error');
            }
        }
    });
});

$('.del-data').click(function(){
    var thisRow = $(this).parents('tr');
    var deldoe =$(this).attr('deldoe');
    var deluid =$(this).attr('deluid');
    $.ajax({
        type: 'GET',
        url: "/delete-data",
        contentType: 'application/json;charset=UTF-8',
        data: {'deldoe':deldoe,'deluid':deluid},
        success: function(data,status){
            thisRow.remove();
        }
    });
});

$('.del-plan').click(function(){
    var thisRow = $(this).parents('tr');
    var delplan =$(this).attr('delplan');
    var delpuid =$(this).attr('delpuid');
    $.ajax({
        type: 'GET',
        url: "/delete-plan",
        contentType: 'application/json;charset=UTF-8',
        data: {'delplan':delplan, 'delpuid':delpuid},
        success: function(data,status){
            thisRow.remove();
        }
    });
});

$('.chngpwd').click(function(){
    var newpwd =$('#newpwd').val();
    var repwd = $('#repwd').val();
    $.ajax({
        type: 'GET',
        url: "/pass-change",
        contentType: 'application/json;charset=UTF-8',
        data: {'newpwd':newpwd, 'repwd':repwd},
        success: function(data,status){
            var error = JSON.parse(data);
            if(error == "Password not match. Re-enter"){
                document.getElementById('showerror').style.display = 'block';
                document.getElementById('showerror').innerHTML = 'Error: Password not match. Re-enter';
            }
        }
    });
});

$('.anl-gr').click(function(){
    var grdt = $('#grall').val()
    $.ajax({
    type: 'GET',
    url: "/grapanalysis",
    contentType: 'application/json;charset=UTF-8',
    data: {'grdt':grdt},
    success: function(data,status){

    }
    });
});

function removeFlash() {
    const element = document.getElementById('div_flash');
    element.remove();
    $('#alert-close').hide();
}