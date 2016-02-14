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

  factory.getProductItems = function (id) {
    return $http.get('/api/branchtype/getproduct' + (id ? '/' + id : ''));
  };

  factory.load = function (is_active, term, sortOrder, sortDesc, page, rp) {
    return $http({
      url: '/api/product/search',
      method: 'post',
      data: {
        'is_active': is_active,
        'term': term,
        'sort': sortOrder,
        'desc': sortDesc,
        'page': page || 1, 'rp': rp || 10
      }
    });
  };

  return factory;
});

app.controller('ctrl', function ($scope, $http, appFactory) {
  $scope.branch_type = {};
  $scope.product_items = [];
  // product info
  $scope.products = [];
  $scope.product = {};
  // product list dialog paging
  $scope.page = 0;
  $scope.rp = 5;
  $scope.results = {};
  $scope.total = 0;
  $scope.pageCount = 0;
  $scope.sortOrder = 'id';
  $scope.sortDesc = true;

  $scope.view = function (id) {
    $scope.branch = {};
    appFactory.view(id).success(function (data) {
      $scope.branch_type = data.branch_type;
    });
  };

  $scope.sortBy = function (ord) {
    $scope.sortDesc = ($scope.sortOrder == ord) ? !$scope.sortDesc : true;
    $scope.sortOrder = ord;
    $scope.search();
  };

  $scope.search = function () {
    $scope.page = 0;
    $scope.total = 0;
    $scope.pageCount = 0;
    $scope.products = [];
    $scope.load();
  };

  $scope.reset = function () {
    $('#search').val('');
    $scope.sortOrder = 'id';
    $scope.sortDesc = false;
    $scope.search();
  };

  $scope.load = function () {
    var isActive = $('#is_active').val();
    var term = $('#search').val();
    appFactory.load(isActive, term, $scope.sortOrder, $scope.sortDesc, $scope.page, $scope.rp).then(function (out) {
      var res = out.data;
      $scope.products = res.products;
      $scope.total = res.total;
      $scope.pageCount = res.page_count;
      $scope.results = {totalPages: res.total_pages, currentPage: $scope.page};
    });
  };

  $scope.openProduct = function () {
    $scope.reset();
    $('#product-modal').modal('show');
  };

  $scope.clearProduct = function () {
    $('#product').val('');
    $('#sale_price').val('');
    $('#cost_price').val('');
    $scope.product = {};
  };

  $scope.selecProduct = function ($index) {
    $scope.product = $scope.products[$index];
    $('#product').val($scope.product.product_name);
    $('#sale_price').val($scope.product.sale_price);
    $('#cost_price').val($scope.product.cost);
    $('#product-modal').modal('hide');
  };

  $scope.addItem = function () {
    var p = $scope.product;
    if (p.id) {
      $scope.addProductItem(p.id, p.product_name, $('#sale_price').val(), $('#cost_price').val());
      $scope.clearProduct();
    } else {
      alert('Please select product');
    }
  };

  $scope.addProductItem = function (id, name, price, cost) {
    $('#product_items').val('');
    var isUpdated = false;
    angular.forEach($scope.product_items, function (item) {
      if (id === item.id) {
        item.price = parseFloat(item.price) + parseFloat(price);
        item.cost = parseFloat(item.cost) + parseFloat(cost);
        isUpdated = true;
      }
    });

    if (!isUpdated) {
      $scope.product_items.push({
        'id': id,
        'name': name,
        'price': price || 0,
        'cost': cost || 0,
      });
    }
  };

  $scope.deleteItem = function ($index) {
    $scope.product_items.splice($index, 1);
  };

  $scope.submit = function () {
    $('#product_items').val(JSON.stringify($scope.product_items));
    console.log($('#product_items').val());
    $('#forms').submit();
  };

  $scope.getProductItems = function (id) {
    appFactory.getProductItems(id).then(function (out) {
      var res = out.data;
      if (res.product_items) {
        var product_items = res.product_items;
        angular.forEach(product_items, function (item) {
          $scope.product_items.push({
            id: item.product.id,
            name: item.product.product_name,
            price: item.sale_price,
            cost: item.cost,
          });
        });
      }
    });
  };

  $scope.getProductItems($('#id').val() || '');
  $scope.view($('#id').val() || '');
});

$(function () {
  $('#forms').submit(function () {
    $(this).ajaxSubmit({
      success: function (res) {
        if (res.result) {
          alert('บันทึกการตั้งราคาขายเรียบร้อยแล้ว');
          window.location = '/admin/btype';
        }
      },
      error: function (xhr) {
      }
    });
    return false;
  });
});
