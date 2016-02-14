var app = angular.module('app', []);

app.config(function ($interpolateProvider, $compileProvider) {
  $compileProvider.debugInfoEnabled(false);
  $interpolateProvider.startSymbol('@{').endSymbol('}');
});

app.factory('appFactory', function ($http) {
  var factory = {};

  factory.getCategories = function () {
    return $http.get('/api/category/list');
  };

  factory.getSubCategories = function (id) {
    if (id) {
      return $http.get('/api/category/sublist/' + id);
    }
    return $http.get('/api/category/sublist');
  };

  factory.view = function (id) {
    return $http.get('/api/product/get' + (id ? '/' + id : ''));
  };

  return factory;
});

app.controller('ctrl', function ($scope, $http, appFactory) {
  $scope.categories = [];
  $scope.subcategories = [];
  $scope.product = {};

  $scope.getCategories = function () {
    appFactory.getCategories().success(function (data) {
      $scope.categories = data.categories;
    });
  };

  $scope.getSubCategories = function (id) {
    appFactory.getSubCategories(id).success(function (data) {
      $scope.subcategories = data.subcategories;
    });
  };

  $scope.updateCategory = function () {
    if ($scope.category)
      $scope.getSubCategories($scope.category.id);
  };

  $scope.view = function (id) {
    $scope.product = {};
    appFactory.view(id).success(function (data) {
      $scope.product = data.product;
      if ($scope.product.category) {
        $scope.category = {id: $scope.product.category.id};
      } else {
        $scope.category = 0;
      }

      if ($scope.product.sub) {
        $scope.subcategory = {id: $scope.product.sub.id};
      } else {
        $scope.subcategory = 0;
      }

      $('#img').val($scope.product.img);
      $('#img_path').val($scope.product.img_path);
      $('#is_hot').prop('checked', $scope.product.is_hot == 'Y');
      $('#is_visible').prop('checked', $scope.product.is_visible == 'Y');
      showImage();
    });
  };

  $scope.submit = function () {
    $('#forms').submit();
  };

  $scope.getCategories();
  $scope.getSubCategories();
  $scope.view($('#id').val() || '');
});

function showImage() {
  if ($('#img_path').val()) {
    $('#pic').attr('src', $('#img_path').val());
    $('#pic').show();
    $('#no-pic').hide();
  } else {
    $('#pic').removeAttr('src');
    $('#pic').hide();
    $('#no-pic').show();
  }
}

$(function () {
  $('#removeimg').on('click', function () {
    $('#img').val('');
    $('#img_path').val('');
    showImage();
  });

  $('#addimg').click(function () {
    $('input[type=file]').click();
    return false;
  });

  $('input[type=file]').change(function () {
    $('#uploadform').submit();
  });

  $('#uploadform').submit(function () {
    $(this).ajaxSubmit({
      success: function (res) {
        if (res.img) {
          $('#img').val(res.img);
          $('#img_path').val(res.img_path);
        }
        showImage();
      },
      error: function (xhr) {
      }
    });
    return false;
  });

  showImage();

  $('#forms').submit(function () {
    $(this).ajaxSubmit({
      success: function (res) {
        if (res.result) {
          alert('บันทึกข้อมูลสินค้าสำเร็จแล้ว');
          window.location = '/admin/product';
        }
      },
      error: function (xhr) {
      }
    });
    return false;
  });
});
