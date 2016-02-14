angular.module('sorted', []).directive('sorted', function () {
  return {
    scope: true,
    transclude: true,
    template: '<a href="#" ng-click="doSort()" ng-transclude></a>' +
    '<span ng-show="doShow(true)"><i class="fa-down-dir"></i></span>' +
    '<span ng-show="doShow(false)"><i class="fa-up-dir"></i></span>',
    controller: function ($scope, $element, $attrs) {
      $scope.sort = $attrs.sorted;
      $scope.doSort = function () {
        $scope.sortBy($scope.sort);
      };
      $scope.doShow = function (asc) {
        return (asc != $scope.sortDesc) && ($scope.sortOrder == $scope.sort);
      };
    }
  };
});
