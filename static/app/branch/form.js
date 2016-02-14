var app = angular.module('app', []);

app.config(function ($interpolateProvider, $compileProvider) {
  $compileProvider.debugInfoEnabled(false);
  $interpolateProvider.startSymbol('@{').endSymbol('}');
});

app.factory('appFactory', function ($http) {
  var factory = {};

  factory.view = function (id) {
    return $http.get('/api/branch/get' + (id ? '/' + id : ''));
  };

  factory.getBranchType = function () {
    return $http.get('/api/branchtype/list');
  };

  return factory;
});

app.controller('ctrl', function ($scope, $http, appFactory) {
  $scope.branch = {};
  $scope.branch_types = [];
  $scope.branchtype = {};

  $scope.view = function (id) {
    $scope.branch = {};
    appFactory.view(id).success(function (data) {
      $scope.branch = data.branch;
      if ($scope.branch.branch_type_id) {
        $scope.branchtype = {id: $scope.branch.branch_type_id};
      } else {
        $scope.branchtype = 0;
      }
    });
  };

  $scope.getBranchType = function (id) {
    appFactory.getBranchType().success(function (data) {
      $scope.branch_types = data.branch_types;
    });
  };

  $scope.submit = function () {
    $('#forms').submit();
  };

  $scope.getBranchType();
  $scope.view($('#id').val() || '');
});

$(function () {
  $('#forms').submit(function () {
    $(this).ajaxSubmit({
      success: function (res) {
        if (res.result) {
          alert('บันทึกข้อมูลสาขาสำเร็จแล้ว');
          window.location = '/admin/branch';
        }
      },
      error: function (xhr) {
      }
    });
    return false;
  });
});
