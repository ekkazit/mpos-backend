var app = angular.module('app', []);

app.config(function ($interpolateProvider, $compileProvider) {
  $compileProvider.debugInfoEnabled(false);
  $interpolateProvider.startSymbol('@{').endSymbol('}');
});

app.factory('appFactory', function ($http) {
  var factory = {};

  factory.view = function (id) {
    return $http.get('/api/branchtype/get' + (id ? '/' + id : ''));
  };

  factory.getBranchType = function () {
    return $http.get('/api/branchtype/list');
  };

  return factory;
});

app.controller('ctrl', function ($scope, $http, appFactory) {
  $scope.branch_type = {};


  $scope.view = function (id) {
    $scope.branch = {};
    appFactory.view(id).success(function (data) {
      $scope.branch_type = data.branch_type;
    });
  };

  $scope.submit = function () {
    $('#forms').submit();
  };

  $scope.view($('#id').val() || '');
});

$(function () {
  $('#forms').submit(function () {
    $(this).ajaxSubmit({
      success: function (res) {
        if (res.result) {
          alert('บันทึกข้อมูลกลุ่มของสาขาสำเร็จแล้ว');
          window.location = '/admin/btype';
        }
      },
      error: function (xhr) {
      }
    });
    return false;
  });
});
