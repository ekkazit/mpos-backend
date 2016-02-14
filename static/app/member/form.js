var app = angular.module('app', []);

app.config(function ($interpolateProvider) {
  $interpolateProvider.startSymbol('@{').endSymbol('}');
});

app.factory('appFactory', function ($http) {
  var factory = {};

  factory.view = function (id) {
    return $http.get('/api/member/get' + (id ? '/' + id : ''));
  };

  factory.getBranch = function () {
    return $http.get('/api/branch/list');
  };

  return factory;
});

app.controller('ctrl', function ($scope, $http, appFactory) {
  $scope.member = {};
  $scope.branches = [];
  $scope.branch = {};

  $scope.view = function (id) {
    $scope.member = {};
    appFactory.view(id).success(function (data) {
      $scope.member = data.member;

      if ($scope.member.branch_id) {
        $scope.branch = {id: $scope.member.branch_id};
      } else {
        $scope.branch = 0;
      }


      $('#na').prop('checked', true);
      if ($scope.member.gender) {
        $(':radio[value=' + $scope.member.gender + ']').prop('checked', true);
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
          alert('บันทึกข้อมูลสมาชิกสำเร็จแล้ว');
          window.location = '/admin/member';
        }
      },
      error: function (xhr) {
      }
    });
    return false;
  });
});

