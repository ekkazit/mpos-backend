var app = angular.module('app', []);

app.config(function ($interpolateProvider) {
  $interpolateProvider.startSymbol('@{').endSymbol('}');
});

app.factory('appFactory', function ($http) {
  var factory = {};

  factory.view = function (id) {
    return $http.get('/api/user/get' + (id ? '/' + id : ''));
  };

  factory.getBranch = function () {
    return $http.get('/api/branch/list');
  };

  return factory;
});

app.controller('ctrl', function ($scope, $http, appFactory) {
  $scope.user = {};
  $scope.branches = [];
  $scope.branch = {};

  $scope.view = function (id) {
    $scope.user = {};
    appFactory.view(id).success(function (data) {
      $scope.user = data.user;

      if ($scope.user.branch_id) {
        $scope.branch = {id: $scope.user.branch_id};
      } else {
        $scope.branch = 0;
      }


      $('#admin').prop('checked', true);
      if ($scope.user.user_type) {
        $(':radio[value=' + $scope.user.user_type + ']').prop('checked', true);
      }
    });
  };

  $scope.getBranch = function () {
    appFactory.getBranch().success(function (data) {
      $scope.branches = data.branches;
    });
  };

  $scope.submit = function () {
    $('#forms').submit();
  };

  $scope.getBranch();
  $scope.view($('#id').val() || '');
});


$(function () {
  $('#forms').submit(function () {
    $(this).ajaxSubmit({
      success: function (res) {
        if (res.result) {
          alert('บันทึกข้อมูลผู้ใช้สำเร็จแล้ว');
          window.location = '/admin/users';
        }
      },
      error: function (xhr) {
      }
    });
    return false;
  });
});
