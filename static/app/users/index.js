var app = angular.module('app', ['pagination', 'sorted']);

app.config(function ($interpolateProvider, $compileProvider) {
  $compileProvider.debugInfoEnabled(false);
  $interpolateProvider.startSymbol('@{').endSymbol('}');
});

app.factory('appFactory', function ($http) {
  var factory = {};

  factory.load = function (is_active, term, sortOrder, sortDesc, page, rp) {
    return $http({
      url: '/api/user/search',
      method: 'post',
      data: {
        'is_active': is_active,
        'term': term,
        'sort': sortOrder,
        'desc': sortDesc,
        'page': page || 1,
        'rp': rp || 10
      }
    });
  };

  factory.remove = function (id) {
    return $http.get('/api/users/delete/' + id);
  };

  factory.deleteAll = function (items) {
    return $http({
      url: '/api/user/deleteall',
      method: 'post',
      data: {
        'items': items
      }
    });
  };

  return factory;
});

app.controller('ctrl', function ($scope, $http, appFactory) {
  $scope.users = [];
  $scope.page = 0;
  $scope.rp = 10;
  $scope.results = {};
  $scope.total = 0;
  $scope.pageCount = 0;
  $scope.sortOrder = 'id';
  $scope.sortDesc = false;

  $scope.sortBy = function (ord) {
    $scope.sortDesc = ($scope.sortOrder == ord) ? !$scope.sortDesc : true;
    $scope.sortOrder = ord;
    $scope.search();
  };

  $scope.search = function () {
    $scope.page = 0;
    $scope.total = 0;
    $scope.pageCount = 0;
    $scope.users = [];
    $scope.load();
    $scope.selected = [];
  };

  $scope.reset = function () {
    $('#search').val('');
    $scope.sortOrder = 'id';
    $scope.sortDesc = true;
    $scope.search();
  };

  $scope.load = function () {
    var isActive = $('#is_active').val();
    var term = $('#search').val();
    appFactory.load(isActive, term, $scope.sortOrder, $scope.sortDesc, $scope.page, $scope.rp).then(function (out) {
      res = out.data;
      $scope.users = res.users;
      $scope.total = res.total;
      $scope.pageCount = res.page_count;
      $scope.results = {totalPages: res.total_pages, currentPage: $scope.page};
    });
  };

  $scope.view = function (id) {
    window.location.href = '/admin/users/form/' + id;
  };

  $scope.remove = function (id) {
    if (confirm('คุณต้องการจะลบผู้ใช้ใช่หรือไม่ ?')) {
      appFactory.remove(id).success(function (data) {
        if (data.result) {
          alert('ลบรายการผู้ใช้สำเร็จแล้ว');
          $scope.search();
        }
      });
    }
  };

  $scope.$on('page', function (e, page) {
    $scope.page = page;
    if (page) {
      $scope.load();
    }
  });

  $scope.search();

  $scope.selected = [];
  var updateSelected = function (action, id) {
    if (action == 'add' & $scope.selected.indexOf(id) == -1) $scope.selected.push(id);
    if (action == 'remove' && $scope.selected.indexOf(id) != -1) $scope.selected.splice($scope.selected.indexOf(id), 1);
  }

  $scope.updateSelection = function ($event, id) {
    var checkbox = $event.target;
    var action = (checkbox.checked ? 'add' : 'remove');
    updateSelected(action, id);
  };

  $scope.selectAll = function ($event) {
    var checkbox = $event.target;
    var action = (checkbox.checked ? 'add' : 'remove');
    for (var i = 0; i < $scope.users.length; i++) {
      var entity = $scope.users[i];
      updateSelected(action, entity.id);
    }
  };

  $scope.getSelectedClass = function (entity) {
    return $scope.isSelected(entity.id) ? 'selected' : '';
  };

  $scope.isSelected = function (id) {
    return $scope.selected.indexOf(id) >= 0;
  };

  $scope.isSelectedAll = function () {
    return $scope.selected.length === $scope.users.length && $scope.users.length > 0;
  };

  $scope.deleteAll = function () {
    if (!$scope.selected.length)
      return;
    if (confirm('คุณต้องการจะลบผู้ใช้ที่เลือกใช่หรือไม่ ?')) {
      appFactory.deleteAll($scope.selected.join(',')).success(function (data) {
        if (data.result) {
          alert('ลบรายการผู้ใช้สำเร็จแล้ว');
          $scope.search();
        }
      });
    }
  };
});
