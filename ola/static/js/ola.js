var validationApp = angular.module('validationApp', []);

// create angular controller
validationApp.controller('FormController', function($scope) {
    $scope.forms = [];
    $scope.form_data = {};
    // function to submit the form after all validation has occurred            
    $scope.validate_and_proceed = function(isValid, callback) {
        // check to make sure the form is completely valid
        if (isValid) {
            eval(callback);
            $scope.forms.push($scope.form_data);
            console.log($scope.forms);
        } else {
            $('#regError').show();
        }
    };

});

function showRegistrationTab(tab) {
    $.each($('ul.nav-tabs li a'), function (index, elem) {
        $(elem).removeClass('current');
    });
    $.each($('div.mainTab'), function(index, elem) {
        $(elem).hide();
    });
    $('#regError').hide();
    switch (parseInt(tab)) {
        case 1: $('#tab1').addClass('current');
                $('#companyRegistrationTab').slideDown(800);
                break;
        case 2: showAdminRegistrationTab();
                break;
        case 3: showInvitationTab();
                break;
    }
}

function showAdminRegistrationTab() {
    $('#tab2').addClass('current');
    $('#adminRegistrationTab').slideDown(800);
}

function showInvitationTab() {
    $('#tab3').addClass('current');
    $('#invitationTab').slideDown(800);
}