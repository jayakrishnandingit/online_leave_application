var ola = angular.module('ola', []);

// create angular controller
ola.controller('RegistrationFormController', function($scope, $http) {
    $scope.form_data = {};
    // function to submit the form after all validation has occurred            
    $scope.validate_and_proceed = function(isValid, tab, callback) {
        // check to make sure the form is completely valid
        if (isValid) {
            if (tab == 3) {
                $http.post(
                    '/subscriber/registration',
                    [$scope.form_data, 'do_registration'],
                    {'responseType' : 'json'}
                ).success(function(data, status, headers, config) {
                  // this callback will be called asynchronously
                  // when the response is available
                    alert('success');
                    console.log(data);
                    if (data.is_saved) {
                        eval(callback)(tab);
                    } else {
                        alert('form error');
                    }
                }).error(function(data, status, headers, config) {
                  // called asynchronously if an error occurs
                  // or server returns response with an error status.
                  alert('error');
                  console.log(data);
                });
            } else {
                eval(callback)(tab);
            }
        } else {
            $('#regError').show();
        }
    };

});

ola.controller('SubscriberEditFormController', function($scope, $http) {
    $scope.subscriber = {};
    $scope.form_data = {};
    $scope.get_subscriber = function(user_id) {
        $http.get(
            '/subscriber/' + user_id,
            {
                'responseType' : 'json',
            }
        ).success(function(data, status, headers, config) {
          // this callback will be called asynchronously
          // when the response is available
            $scope.subscriber = data.subscriber;
            $scope.form_data['first_name'] = data.subscriber.user.first_name;
            $scope.form_data['last_name'] = data.subscriber.user.last_name;
            $scope.form_data['email'] = data.subscriber.user.email;
            $scope.form_data['role'] = data.subscriber.group.id;
            $scope.form_data['no_of_leave_remaining'] = data.subscriber.no_of_leave_remaining;
            $scope.form_data['hidden_user'] = data.subscriber.user.id;
        }).error(function(data, status, headers, config) {
          // called asynchronously if an error occurs
          // or server returns response with an error status.
          console.log(data);
        });
    }
    $scope.get_subscriber(user_id);
    // function to submit the form after all validation has occurred            
    $scope.validate_and_proceed = function(isValid) {
        // check to make sure the form is completely valid
        if (isValid) {
            return;
        } else {
            $('#formError').show();
        }
    };

});

ola.directive('passwordCheck', ['$parse', function($parse) {
    return {
        restrict: 'A',
        require: 'ngModel',
        link: function(scope, element, attrs, ctrl) {
            var me = attrs.ngModel;
            var pwd_to_check = $parse(me);
            var matchTo = attrs.passwordCheck;
            var first_password = $parse(matchTo);
            scope.$watch(me, function(value) {
                if (pwd_to_check(scope) && first_password(scope)) {
                    ctrl.$setValidity('match', (pwd_to_check(scope) === first_password(scope)));
                }
            });
            scope.$watch(matchTo, function(value) {
                if (pwd_to_check(scope) && first_password(scope)) {
                    ctrl.$setValidity('match', (pwd_to_check(scope) === first_password(scope)));
                }
            });
        }
    }
}]);

ola.controller('SubscriberListController', function($scope, $http) {
    $scope.subscribers = [];
    $scope.prev_page_no = 1;
    $scope.current_page_no = 1;
    $scope.next_page_no = 1;
    $scope.nop = 1;
    $scope.nor = 10;
    $scope.fn = 'get_all';
    $scope.get_subscribers = function(page_no, no_of_records, show_all) {
        $http.get(
            '/subscriber',
            {
                'responseType' : 'json',
                'params' : {'page_no' : page_no, 'no_of_records' : no_of_records, 'show_all' : show_all, 'fn' : $scope.fn}
            }
        ).success(function(data, status, headers, config) {
          // this callback will be called asynchronously
          // when the response is available
            $scope.subscribers = data.subscribers;
            $scope.current_page_no = data.current_page_number;
            $scope.next_page_no = data.next_page_number;
            $scope.prev_page_no = data.prev_page_number;
            $scope.nop = data.num_of_pages;
            $scope.nor = data.no_of_records;
        }).error(function(data, status, headers, config) {
          // called asynchronously if an error occurs
          // or server returns response with an error status.
          console.log(data);
        });
    }
    $scope.get_subscribers($scope.current_page_no, $scope.nor, 0);
    $scope.get_next_page = function () {
        $scope.get_subscribers($scope.next_page_no, $scope.nor, 0);
    }
    $scope.get_prev_page = function () {
        $scope.get_subscribers($scope.prev_page_no, $scope.nor, 0);
    }
    $scope.get_page_change = function () {
        $scope.get_subscribers($scope.current_page_no, $scope.nor, 0);
    }
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
        case 2: $('#tab2').addClass('current');
                $('#adminRegistrationTab').slideDown(800);
                break;
        case 3: $('#tab3').addClass('current');
                $('#paymentTab').slideDown(800);
                $('#tempDisableDiv').show();
                break;
    }
}
