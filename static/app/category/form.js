var app = angular.module('app', []);

app.config(function ($interpolateProvider, $compileProvider) {
  $compileProvider.debugInfoEnabled(false);
  $interpolateProvider.startSymbol('@{').endSymbol('}');
});

app.factory('appFactory', function ($http) {
  var factory = {};

  factory.view = function (id) {
    return $http.get('/api/category/get' + (id ? '/' + id : ''));
  };

  factory.getCategories = function (id) {
    return $http.get('/api/category/all' + (id ? '/' + id : ''));
  };

  return factory;
});

app.controller('ctrl', function ($scope, $http, appFactory) {
  $scope.category = {};
  $scope.categories = [];

  $scope.view = function (id) {
    $scope.category = {};
    appFactory.view(id).success(function (data) {
      $scope.category = data.category;
      if ($scope.category.parent_id) {
        $scope.parent = {id: $scope.category.parent_id};
      } else {
        $scope.parent = 0;
      }
    });
  };

  $scope.getCategories = function (id) {
    appFactory.getCategories(id).success(function (data) {
      $scope.categories = data.categories;
    });
  };

  $scope.submit = function () {
    $('#forms').submit();
  };
  $scope.getCategories($('#id').val() || '');
  $scope.view($('#id').val() || '');
});

$(function () {
  $('#forms').submit(function () {
    $(this).ajaxSubmit({
      success: function (res) {
        if (res.result) {
          alert('บันทึกข้อมูลประเภทสินค้าสำเร็จแล้ว');

          window.location = '/admin/category';
        }
      },
      error: function (xhr) {
      }
    });
    return false;
  });
});
