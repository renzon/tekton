var app = angular.module('app', ['rest'])
    .controller('AppCtrl', ['$scope', 'RestApi', function ($scope, RestApi) {
        $scope.users = [];
        $scope.searchingUsersFlag = false;
        $scope.moreResultsFlag = false;
        $scope.searchPrefix = ''
        $scope.searchUsers = function (emailPrefix) {
            $scope.searchPrefix = emailPrefix;
            $scope.searchingUsersFlag = true;
            RestApi.searchUsers(emailPrefix).success(function (obj) {
                $scope.users = obj.users;
                $scope.moreResultsFlag = obj.more;
                $scope.nextPage = obj.next_page;
            }).always(function () {
                $scope.searchingUsersFlag = false;
            });
        }
        $scope.searchUsers('');
    }]);

app.directive('permform', function () {
    return{
        restrict: 'E',
        replace: true,
        templateUrl: '/static/permission/html/permission_form.html',
        scope: {
            search: '=',
            showButton: '='
        },
        controller: ['$scope', function ($scope) {
            $scope.emailPrefix = '';
        }]
    };
});

app.directive('checkList', function () {
    return {
        scope: {
            list: '=checkList',
            value: '@'
        },
        link: function (scope, elem, attrs) {
            var handler = function (setup) {
                var checked = elem.prop('checked');
                var index = scope.list.indexOf(scope.value);

                if (checked && index == -1) {
                    if (setup) elem.prop('checked', false);
                    else scope.list.push(scope.value);
                } else if (!checked && index != -1) {
                    if (setup) elem.prop('checked', true);
                    else scope.list.splice(index, 1);
                }
            };

            var setupHandler = handler.bind(null, true);
            var changeHandler = handler.bind(null, false);

            elem.on('change', function () {
                scope.$apply(changeHandler);
            });
            scope.$watch('list', setupHandler, true);
        }
    };
});

app.directive('permtable', function () {
    return{
        restrict: 'E',
        replace: true,
        templateUrl: '/static/permission/html/permission_table.html',
        scope: {
            users: '=',
            nextPage: '=',
            showTable: '=',
            moreResultsFlag: '=',
            searchPrefix: '=',
            groups: '='
        },
        controller: ['$scope', 'RestApi', function ($scope, rest) {
            $scope.searchingNextPage = false;

            $scope.searchNextPage = function (nextPage) {
                $scope.searchingNextPage = true;
                rest.searchNextPage(nextPage).success(function (obj) {
                    for (var i = 0; i < obj.users.length; i++) {
                        $scope.users.push(obj.users[i]);
                    }
                    $scope.nextPage = obj.next_page;
                    $scope.moreResultsFlag = obj.more;
                }).always(function () {
                    $scope.searchingNextPage = false;
                });
            }

        }]
    };
});

app.directive('grouptd', function () {
    return{
        restrict: 'E',
        replace: true,
        templateUrl: '/static/permission/html/group_td.html',
        scope: {
            groups: '=',
            user: '='
        },
        controller: ['$scope', 'RestApi', function ($scope, rest) {
            $scope.updatingGroups = false;

            $scope.updateUserGroups = function (user) {
                $scope.updatingGroups = true;
                rest.updateUserGroups(user.update, {'groups': user.groups})
                    .error(function(){
                        alert('It is not possible to save changes. Refresh the page and try again');
                    })
                    .always(function () {
                        $scope.updatingGroups = false;
                    });
            }

        }]

    };
});