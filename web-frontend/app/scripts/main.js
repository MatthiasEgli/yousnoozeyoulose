/*!
 *
 *  Web Starter Kit
 *  Copyright 2014 Google Inc. All rights reserved.
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License
 *
 */
(function () {
  'use strict';

  var querySelector = document.querySelector.bind(document);

  var navdrawerContainer = querySelector('.navdrawer-container');
  var body = document.body;
  var appbarElement = querySelector('.app-bar');
  var menuBtn = querySelector('.menu');
  var main = querySelector('main');

  function closeMenu() {
    body.classList.remove('open');
    appbarElement.classList.remove('open');
    navdrawerContainer.classList.remove('open');
  }

  function toggleMenu() {
    body.classList.toggle('open');
    appbarElement.classList.toggle('open');
    navdrawerContainer.classList.toggle('open');
    navdrawerContainer.classList.add('opened');
  }

  main.addEventListener('click', closeMenu);
  menuBtn.addEventListener('click', toggleMenu);
  navdrawerContainer.addEventListener('click', function (event) {
    if (event.target.nodeName === 'A' || event.target.nodeName === 'LI') {
      closeMenu();
    }
  });
})();

Stripe.setPublishableKey('pk_test_sqyMF8VmsGm0H9G3guOLdjZ4');

var myApp = angular.module('myApp', ['ui.router', 'angularPayments']);

myApp.config(function($stateProvider, $urlRouterProvider) {
  //
  // For any unmatched url, redirect to /state1
  $urlRouterProvider.otherwise("/charge");
  //
  // Now set up the states
  $stateProvider
    .state('charge', {
      url: "/charge",
      templateUrl: "views/charge.html",
      controller: 'ChargeController'
    })
    .state('choose', {
      url: "/choose",
      templateUrl: "views/choose.html",
    })
    .state('login', {
      url: "/login",
      templateUrl: "views/login.html",
    });
});

myApp.controller('ChargeController', function($scope) {
  $scope.handleStripe = function(status, response){
    if(response.error) {
      console.log("error");
    } else {
      console.log("success");
      // got stripe token, now charge it or smt
      token = response.id;
    }
  };
});
