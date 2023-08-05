(function webpackUniversalModuleDefinition(root, factory) {
	if(typeof exports === 'object' && typeof module === 'object')
		module.exports = factory(require("react"), require("react-dom"));
	else if(typeof define === 'function' && define.amd)
		define(["react", "react-dom"], factory);
	else if(typeof exports === 'object')
		exports["dazzler_renderer"] = factory(require("react"), require("react-dom"));
	else
		root["dazzler_renderer"] = factory(root["React"], root["ReactDOM"]);
})(window, function(__WEBPACK_EXTERNAL_MODULE_react__, __WEBPACK_EXTERNAL_MODULE_react_dom__) {
return /******/ (function(modules) { // webpackBootstrap
/******/ 	// install a JSONP callback for chunk loading
/******/ 	function webpackJsonpCallback(data) {
/******/ 		var chunkIds = data[0];
/******/ 		var moreModules = data[1];
/******/ 		var executeModules = data[2];
/******/
/******/ 		// add "moreModules" to the modules object,
/******/ 		// then flag all "chunkIds" as loaded and fire callback
/******/ 		var moduleId, chunkId, i = 0, resolves = [];
/******/ 		for(;i < chunkIds.length; i++) {
/******/ 			chunkId = chunkIds[i];
/******/ 			if(installedChunks[chunkId]) {
/******/ 				resolves.push(installedChunks[chunkId][0]);
/******/ 			}
/******/ 			installedChunks[chunkId] = 0;
/******/ 		}
/******/ 		for(moduleId in moreModules) {
/******/ 			if(Object.prototype.hasOwnProperty.call(moreModules, moduleId)) {
/******/ 				modules[moduleId] = moreModules[moduleId];
/******/ 			}
/******/ 		}
/******/ 		if(parentJsonpFunction) parentJsonpFunction(data);
/******/
/******/ 		while(resolves.length) {
/******/ 			resolves.shift()();
/******/ 		}
/******/
/******/ 		// add entry modules from loaded chunk to deferred list
/******/ 		deferredModules.push.apply(deferredModules, executeModules || []);
/******/
/******/ 		// run deferred modules when all chunks ready
/******/ 		return checkDeferredModules();
/******/ 	};
/******/ 	function checkDeferredModules() {
/******/ 		var result;
/******/ 		for(var i = 0; i < deferredModules.length; i++) {
/******/ 			var deferredModule = deferredModules[i];
/******/ 			var fulfilled = true;
/******/ 			for(var j = 1; j < deferredModule.length; j++) {
/******/ 				var depId = deferredModule[j];
/******/ 				if(installedChunks[depId] !== 0) fulfilled = false;
/******/ 			}
/******/ 			if(fulfilled) {
/******/ 				deferredModules.splice(i--, 1);
/******/ 				result = __webpack_require__(__webpack_require__.s = deferredModule[0]);
/******/ 			}
/******/ 		}
/******/
/******/ 		return result;
/******/ 	}
/******/
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// object to store loaded and loading chunks
/******/ 	// undefined = chunk not loaded, null = chunk preloaded/prefetched
/******/ 	// Promise = chunk loading, 0 = chunk loaded
/******/ 	var installedChunks = {
/******/ 		"renderer": 0
/******/ 	};
/******/
/******/ 	var deferredModules = [];
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/ 	var jsonpArray = window["webpackJsonpdazzler_name_"] = window["webpackJsonpdazzler_name_"] || [];
/******/ 	var oldJsonpFunction = jsonpArray.push.bind(jsonpArray);
/******/ 	jsonpArray.push = webpackJsonpCallback;
/******/ 	jsonpArray = jsonpArray.slice();
/******/ 	for(var i = 0; i < jsonpArray.length; i++) webpackJsonpCallback(jsonpArray[i]);
/******/ 	var parentJsonpFunction = oldJsonpFunction;
/******/
/******/
/******/ 	// add entry module to deferred list
/******/ 	deferredModules.push([1,"commons"]);
/******/ 	// run deferred modules when ready
/******/ 	return checkDeferredModules();
/******/ })
/************************************************************************/
/******/ ({

/***/ "./src/renderer/js/components/Renderer.jsx":
/*!*************************************************!*\
  !*** ./src/renderer/js/components/Renderer.jsx ***!
  \*************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "default", function() { return Renderer; });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _Updater__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./Updater */ "./src/renderer/js/components/Updater.jsx");
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! prop-types */ "./node_modules/prop-types/index.js");
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(prop_types__WEBPACK_IMPORTED_MODULE_2__);
function _typeof(obj) { if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { _typeof = function _typeof(obj) { return typeof obj; }; } else { _typeof = function _typeof(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return _typeof(obj); }

function _extends() { _extends = Object.assign || function (target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i]; for (var key in source) { if (Object.prototype.hasOwnProperty.call(source, key)) { target[key] = source[key]; } } } return target; }; return _extends.apply(this, arguments); }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

function _possibleConstructorReturn(self, call) { if (call && (_typeof(call) === "object" || typeof call === "function")) { return call; } return _assertThisInitialized(self); }

function _assertThisInitialized(self) { if (self === void 0) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return self; }

function _getPrototypeOf(o) { _getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf : function _getPrototypeOf(o) { return o.__proto__ || Object.getPrototypeOf(o); }; return _getPrototypeOf(o); }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function"); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, writable: true, configurable: true } }); if (superClass) _setPrototypeOf(subClass, superClass); }

function _setPrototypeOf(o, p) { _setPrototypeOf = Object.setPrototypeOf || function _setPrototypeOf(o, p) { o.__proto__ = p; return o; }; return _setPrototypeOf(o, p); }





var Renderer =
/*#__PURE__*/
function (_React$Component) {
  _inherits(Renderer, _React$Component);

  function Renderer(props) {
    var _this;

    _classCallCheck(this, Renderer);

    _this = _possibleConstructorReturn(this, _getPrototypeOf(Renderer).call(this, props));
    _this.state = {
      reloadKey: 1
    };
    return _this;
  }

  _createClass(Renderer, [{
    key: "componentWillMount",
    value: function componentWillMount() {
      window.dazzler_base_url = this.props.baseUrl;
    }
  }, {
    key: "render",
    value: function render() {
      var _this2 = this;

      return react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        className: "dazzler-renderer"
      }, react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(_Updater__WEBPACK_IMPORTED_MODULE_1__["default"], _extends({}, this.props, {
        key: "upd-".concat(this.state.reloadKey),
        hotReload: function hotReload() {
          return _this2.setState({
            reloadKey: _this2.state.reloadKey + 1
          });
        }
      })));
    }
  }]);

  return Renderer;
}(react__WEBPACK_IMPORTED_MODULE_0___default.a.Component);


Renderer.propTypes = {
  baseUrl: prop_types__WEBPACK_IMPORTED_MODULE_2___default.a.string.isRequired,
  ping: prop_types__WEBPACK_IMPORTED_MODULE_2___default.a.bool,
  ping_interval: prop_types__WEBPACK_IMPORTED_MODULE_2___default.a.number,
  retries: prop_types__WEBPACK_IMPORTED_MODULE_2___default.a.number
};

/***/ }),

/***/ "./src/renderer/js/components/Updater.jsx":
/*!************************************************!*\
  !*** ./src/renderer/js/components/Updater.jsx ***!
  \************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "default", function() { return Updater; });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! prop-types */ "./node_modules/prop-types/index.js");
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(prop_types__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _requests__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../requests */ "./src/renderer/js/requests.js");
/* harmony import */ var _hydrator__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../hydrator */ "./src/renderer/js/hydrator.js");
/* harmony import */ var _requirements__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../requirements */ "./src/renderer/js/requirements.js");
/* harmony import */ var _commons_js_utils__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../commons/js/utils */ "./src/commons/js/utils.js");
function _typeof(obj) { if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { _typeof = function _typeof(obj) { return typeof obj; }; } else { _typeof = function _typeof(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return _typeof(obj); }

function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; var ownKeys = Object.keys(source); if (typeof Object.getOwnPropertySymbols === 'function') { ownKeys = ownKeys.concat(Object.getOwnPropertySymbols(source).filter(function (sym) { return Object.getOwnPropertyDescriptor(source, sym).enumerable; })); } ownKeys.forEach(function (key) { _defineProperty(target, key, source[key]); }); } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

function _possibleConstructorReturn(self, call) { if (call && (_typeof(call) === "object" || typeof call === "function")) { return call; } return _assertThisInitialized(self); }

function _getPrototypeOf(o) { _getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf : function _getPrototypeOf(o) { return o.__proto__ || Object.getPrototypeOf(o); }; return _getPrototypeOf(o); }

function _assertThisInitialized(self) { if (self === void 0) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function"); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, writable: true, configurable: true } }); if (superClass) _setPrototypeOf(subClass, superClass); }

function _setPrototypeOf(o, p) { _setPrototypeOf = Object.setPrototypeOf || function _setPrototypeOf(o, p) { o.__proto__ = p; return o; }; return _setPrototypeOf(o, p); }








var Updater =
/*#__PURE__*/
function (_React$Component) {
  _inherits(Updater, _React$Component);

  function Updater(props) {
    var _this;

    _classCallCheck(this, Updater);

    _this = _possibleConstructorReturn(this, _getPrototypeOf(Updater).call(this, props));
    _this.state = {
      layout: false,
      ready: false,
      page: null,
      bindings: {},
      packages: [],
      requirements: [],
      reloading: false,
      needRefresh: false
    }; // The api url for the page is the same but a post.
    // Fetch bindings, packages & requirements

    _this.pageApi = Object(_requests__WEBPACK_IMPORTED_MODULE_2__["apiRequest"])(window.location.href); // All components get connected.

    _this.boundComponents = {};
    _this.ws = null;
    _this.updateAspects = _this.updateAspects.bind(_assertThisInitialized(_this));
    _this.connect = _this.connect.bind(_assertThisInitialized(_this));
    _this.disconnect = _this.disconnect.bind(_assertThisInitialized(_this));
    _this.onMessage = _this.onMessage.bind(_assertThisInitialized(_this));
    return _this;
  }

  _createClass(Updater, [{
    key: "updateAspects",
    value: function updateAspects(identity, aspects) {
      var _this2 = this;

      return new Promise(function (resolve) {
        var bindings = Object.keys(aspects).map(function (key) {
          return _this2.state.bindings["".concat(identity, ".").concat(key)];
        }).filter(function (e) {
          return e;
        });

        if (!bindings) {
          return resolve(0);
        }

        bindings.forEach(function (binding) {
          return _this2.sendBinding(binding, aspects[binding.trigger.aspect]);
        });
        resolve();
      });
    }
  }, {
    key: "connect",
    value: function connect(identity, setAspects, getAspect) {
      this.boundComponents[identity] = {
        setAspects: setAspects,
        getAspect: getAspect
      };
    }
  }, {
    key: "disconnect",
    value: function disconnect(identity) {
      delete this.boundComponents[identity];
    }
  }, {
    key: "onMessage",
    value: function onMessage(response) {
      var _this3 = this;

      var data = JSON.parse(response.data);
      var identity = data.identity,
          kind = data.kind,
          payload = data.payload,
          storage = data.storage,
          request_id = data.request_id;
      var store;

      if (storage === 'session') {
        store = window.sessionStorage;
      } else {
        store = window.localStorage;
      }

      switch (kind) {
        case 'set-aspect':
          var component = this.boundComponents[identity];

          if (!component) {
            var error = "Component not found: ".concat(identity);
            this.ws.send(JSON.stringify({
              error: error,
              kind: 'error'
            }));
            console.error(error);
            return;
          }

          component.setAspects(Object(_hydrator__WEBPACK_IMPORTED_MODULE_3__["hydrateProps"])(payload, this.updateAspects, this.connect, this.disconnect)).then(function () {
            Object.keys(payload).forEach(function (k) {
              var key = "".concat(identity, ".").concat(k);
              var binding = _this3.state.bindings[key];

              if (binding) {
                _this3.sendBinding(binding, component.getAspect(k));
              } // What about returned components ?
              // They get their Wrapper.

            });
          });
          break;

        case 'get-aspect':
          var aspect = data.aspect;
          var wanted = this.boundComponents[identity];

          if (!wanted) {
            this.ws.send(JSON.stringify({
              kind: kind,
              identity: identity,
              aspect: aspect,
              request_id: request_id,
              error: "Aspect not found ".concat(identity, ".").concat(aspect)
            }));
            return;
          }

          var value = wanted.getAspect(aspect);
          this.ws.send(JSON.stringify({
            kind: kind,
            identity: identity,
            aspect: aspect,
            value: Object(_hydrator__WEBPACK_IMPORTED_MODULE_3__["prepareProp"])(value),
            request_id: request_id
          }));
          break;

        case 'set-storage':
          store.setItem(identity, JSON.stringify(payload));
          break;

        case 'get-storage':
          this.ws.send(JSON.stringify({
            kind: kind,
            identity: identity,
            request_id: request_id,
            value: JSON.parse(store.getItem(identity))
          }));
          break;

        case 'reload':
          var filenames = data.filenames,
              hot = data.hot,
              refresh = data.refresh,
              deleted = data.deleted;

          if (refresh) {
            this.ws.close();
            return this.setState({
              reloading: true,
              needRefresh: true
            });
          }

          if (hot) {
            // The ws connection will close, when it
            // reconnect it will do a hard reload of the page api.
            return this.setState({
              reloading: true
            });
          }

          filenames.forEach(_requirements__WEBPACK_IMPORTED_MODULE_4__["loadRequirement"]);
          deleted.forEach(function (r) {
            return Object(_commons_js_utils__WEBPACK_IMPORTED_MODULE_5__["disableCss"])(r.url);
          });
          break;

        case 'ping':
          // Just do nothing.
          break;
      }
    }
  }, {
    key: "sendBinding",
    value: function sendBinding(binding, value) {
      var _this4 = this;

      // Collect all values and send a binding payload
      var trigger = _objectSpread({}, binding.trigger, {
        value: Object(_hydrator__WEBPACK_IMPORTED_MODULE_3__["prepareProp"])(value)
      });

      var states = binding.states.map(function (state) {
        return _objectSpread({}, state, {
          value: _this4.boundComponents[state.identity] && Object(_hydrator__WEBPACK_IMPORTED_MODULE_3__["prepareProp"])(_this4.boundComponents[state.identity].getAspect(state.aspect))
        });
      });
      var payload = {
        trigger: trigger,
        states: states,
        kind: 'binding',
        page: this.state.page,
        key: binding.key
      };
      this.ws.send(JSON.stringify(payload));
    }
  }, {
    key: "_connectWS",
    value: function _connectWS() {
      var _this5 = this;

      // Setup websocket for updates
      var tries = 0;
      var hardClose = false;

      var connexion = function connexion() {
        _this5.ws = new WebSocket("ws".concat(window.location.href.startsWith('https') ? 's' : '', "://").concat(_this5.props.baseUrl && _this5.props.baseUrl || window.location.host).concat(window.location.pathname, "/ws"));

        _this5.ws.addEventListener('message', _this5.onMessage);

        _this5.ws.onopen = function () {
          if (_this5.state.reloading) {
            hardClose = true;

            _this5.ws.close();

            if (_this5.state.needRefresh) {
              window.location.reload();
            } else {
              _this5.props.hotReload();
            }
          } else {
            _this5.setState({
              ready: true
            });

            tries = 0;
          }
        };

        _this5.ws.onclose = function () {
          var reconnect = function reconnect() {
            tries++;
            connexion();
          };

          if (!hardClose && tries < _this5.props.retries) {
            setTimeout(reconnect, 1000);
          }
        };
      };

      connexion();
    }
  }, {
    key: "componentWillMount",
    value: function componentWillMount() {
      var _this6 = this;

      this.pageApi('', {
        method: 'POST'
      }).then(function (response) {
        _this6.setState({
          page: response.page,
          layout: response.layout,
          bindings: response.bindings,
          packages: response.packages,
          requirements: response.requirements
        });

        Object(_requirements__WEBPACK_IMPORTED_MODULE_4__["loadRequirements"])(response.requirements, response.packages).then(function () {
          if (Object.keys(response.bindings).length || response.reload) {
            _this6._connectWS();
          } else {
            _this6.setState({
              ready: true
            });
          }
        });
      });
    }
  }, {
    key: "render",
    value: function render() {
      var _this$state = this.state,
          layout = _this$state.layout,
          ready = _this$state.ready,
          reloading = _this$state.reloading;

      if (!ready) {
        return react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
          className: "dazzler-loading"
        }, "Loading...");
      }

      if (reloading) {
        return react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
          className: "dazzler-loading"
        }, "Reloading...");
      }

      if (!Object(_hydrator__WEBPACK_IMPORTED_MODULE_3__["isComponent"])(layout)) {
        throw new Error("Layout is not a component: ".concat(layout));
      }

      return react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        className: "dazzler-rendered"
      }, Object(_hydrator__WEBPACK_IMPORTED_MODULE_3__["hydrateComponent"])(layout.name, layout["package"], layout.identity, Object(_hydrator__WEBPACK_IMPORTED_MODULE_3__["hydrateProps"])(layout.aspects, this.updateAspects, this.connect, this.disconnect), this.updateAspects, this.connect, this.disconnect));
    }
  }]);

  return Updater;
}(react__WEBPACK_IMPORTED_MODULE_0___default.a.Component);


Updater.defaultProps = {};
Updater.propTypes = {
  baseUrl: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string.isRequired,
  ping: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.bool,
  ping_interval: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.number,
  retries: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.number,
  hotReload: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.func
};

/***/ }),

/***/ "./src/renderer/js/components/Wrapper.jsx":
/*!************************************************!*\
  !*** ./src/renderer/js/components/Wrapper.jsx ***!
  \************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "default", function() { return Wrapper; });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! prop-types */ "./node_modules/prop-types/index.js");
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(prop_types__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var ramda__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ramda */ "./node_modules/ramda/es/index.js");
/* harmony import */ var _commons_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../commons/js */ "./src/commons/js/index.js");
function _typeof(obj) { if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { _typeof = function _typeof(obj) { return typeof obj; }; } else { _typeof = function _typeof(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return _typeof(obj); }

function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; var ownKeys = Object.keys(source); if (typeof Object.getOwnPropertySymbols === 'function') { ownKeys = ownKeys.concat(Object.getOwnPropertySymbols(source).filter(function (sym) { return Object.getOwnPropertyDescriptor(source, sym).enumerable; })); } ownKeys.forEach(function (key) { _defineProperty(target, key, source[key]); }); } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

function _possibleConstructorReturn(self, call) { if (call && (_typeof(call) === "object" || typeof call === "function")) { return call; } return _assertThisInitialized(self); }

function _getPrototypeOf(o) { _getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf : function _getPrototypeOf(o) { return o.__proto__ || Object.getPrototypeOf(o); }; return _getPrototypeOf(o); }

function _assertThisInitialized(self) { if (self === void 0) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function"); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, writable: true, configurable: true } }); if (superClass) _setPrototypeOf(subClass, superClass); }

function _setPrototypeOf(o, p) { _setPrototypeOf = Object.setPrototypeOf || function _setPrototypeOf(o, p) { o.__proto__ = p; return o; }; return _setPrototypeOf(o, p); }





/**
 * Wraps components for aspects updating.
 */

var Wrapper =
/*#__PURE__*/
function (_React$Component) {
  _inherits(Wrapper, _React$Component);

  function Wrapper(props) {
    var _this;

    _classCallCheck(this, Wrapper);

    _this = _possibleConstructorReturn(this, _getPrototypeOf(Wrapper).call(this, props));
    _this.state = {
      aspects: props.aspects || {},
      ready: false,
      initial: false
    };
    _this.setAspects = _this.setAspects.bind(_assertThisInitialized(_this));
    _this.getAspect = _this.getAspect.bind(_assertThisInitialized(_this));
    _this.updateAspects = _this.updateAspects.bind(_assertThisInitialized(_this));
    return _this;
  }

  _createClass(Wrapper, [{
    key: "updateAspects",
    value: function updateAspects(aspects) {
      var _this2 = this;

      return this.setAspects(aspects).then(function () {
        return _this2.props.updateAspects(_this2.props.identity, aspects);
      });
    }
  }, {
    key: "setAspects",
    value: function setAspects(aspects) {
      var _this3 = this;

      return new Promise(function (resolve) {
        _this3.setState({
          aspects: _objectSpread({}, _this3.state.aspects, aspects)
        }, resolve);
      });
    }
  }, {
    key: "getAspect",
    value: function getAspect(aspect) {
      return this.state.aspects[aspect];
    }
  }, {
    key: "componentDidMount",
    value: function componentDidMount() {
      var _this4 = this;

      // Only update the component when mounted.
      // Otherwise gets a race condition with willUnmount
      this.props.connect(this.props.identity, this.setAspects, this.getAspect);

      if (!this.state.initial) {
        this.updateAspects(this.state.aspects).then(function () {
          return _this4.setState({
            ready: true,
            initial: true
          });
        });
      }
    }
  }, {
    key: "componentWillUnmount",
    value: function componentWillUnmount() {
      this.props.disconnect(this.props.identity);
    }
  }, {
    key: "render",
    value: function render() {
      var _this$props = this.props,
          component = _this$props.component,
          component_name = _this$props.component_name,
          package_name = _this$props.package_name;
      var _this$state = this.state,
          aspects = _this$state.aspects,
          ready = _this$state.ready;
      if (!ready) return null;
      return react__WEBPACK_IMPORTED_MODULE_0___default.a.cloneElement(component, _objectSpread({}, aspects, {
        updateAspects: this.updateAspects,
        identity: this.props.identity,
        class_name: Object(ramda__WEBPACK_IMPORTED_MODULE_2__["join"])(' ', Object(ramda__WEBPACK_IMPORTED_MODULE_2__["concat"])(["".concat(package_name.replace('_', '-').toLowerCase(), "-").concat(Object(_commons_js__WEBPACK_IMPORTED_MODULE_3__["camelToSpinal"])(component_name))], aspects.class_name ? aspects.class_name.split(' ') : []))
      }));
    }
  }]);

  return Wrapper;
}(react__WEBPACK_IMPORTED_MODULE_0___default.a.Component);


Wrapper.propTypes = {
  identity: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string.isRequired,
  updateAspects: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.func.isRequired,
  component: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.node.isRequired,
  connect: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.func.isRequired,
  component_name: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string.isRequired,
  package_name: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string.isRequired,
  disconnect: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.func.isRequired
};

/***/ }),

/***/ "./src/renderer/js/hydrator.js":
/*!*************************************!*\
  !*** ./src/renderer/js/hydrator.js ***!
  \*************************************/
/*! exports provided: isComponent, hydrateProps, hydrateComponent, prepareProp */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "isComponent", function() { return isComponent; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "hydrateProps", function() { return hydrateProps; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "hydrateComponent", function() { return hydrateComponent; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "prepareProp", function() { return prepareProp; });
/* harmony import */ var ramda__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ramda */ "./node_modules/ramda/es/index.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _components_Wrapper__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./components/Wrapper */ "./src/renderer/js/components/Wrapper.jsx");
function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; var ownKeys = Object.keys(source); if (typeof Object.getOwnPropertySymbols === 'function') { ownKeys = ownKeys.concat(Object.getOwnPropertySymbols(source).filter(function (sym) { return Object.getOwnPropertyDescriptor(source, sym).enumerable; })); } ownKeys.forEach(function (key) { _defineProperty(target, key, source[key]); }); } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

function _slicedToArray(arr, i) { return _arrayWithHoles(arr) || _iterableToArrayLimit(arr, i) || _nonIterableRest(); }

function _nonIterableRest() { throw new TypeError("Invalid attempt to destructure non-iterable instance"); }

function _iterableToArrayLimit(arr, i) { var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"] != null) _i["return"](); } finally { if (_d) throw _e; } } return _arr; }

function _arrayWithHoles(arr) { if (Array.isArray(arr)) return arr; }




function isComponent(c) {
  return Object(ramda__WEBPACK_IMPORTED_MODULE_0__["type"])(c) === 'Object' && c.hasOwnProperty('package') && c.hasOwnProperty('aspects') && c.hasOwnProperty('name') && c.hasOwnProperty('identity');
}
function hydrateProps(props, updateAspects, connect, disconnect) {
  var replace = {};
  Object.entries(props).forEach(function (_ref) {
    var _ref2 = _slicedToArray(_ref, 2),
        k = _ref2[0],
        v = _ref2[1];

    if (Object(ramda__WEBPACK_IMPORTED_MODULE_0__["type"])(v) === 'Array') {
      replace[k] = v.map(function (c) {
        if (!isComponent(c)) {
          // Mixing components and primitives
          return c;
        }

        var newProps = hydrateProps(c.aspects, updateAspects, connect, disconnect);

        if (!newProps.key) {
          newProps.key = c.identity;
        }

        return hydrateComponent(c.name, c["package"], c.identity, newProps, updateAspects, connect, disconnect);
      });
    } else if (isComponent(v)) {
      var newProps = hydrateProps(v.aspects, updateAspects, connect, disconnect);
      replace[k] = hydrateComponent(v.name, v["package"], v.identity, newProps, updateAspects, connect, disconnect);
    } else if (Object(ramda__WEBPACK_IMPORTED_MODULE_0__["type"])(v) === 'Object') {
      replace[k] = hydrateProps(v, updateAspects, connect, disconnect);
    }
  });
  return _objectSpread({}, props, replace);
}
function hydrateComponent(name, package_name, identity, props, updateAspects, connect, disconnect) {
  var pack = window[package_name];
  var element = react__WEBPACK_IMPORTED_MODULE_1___default.a.createElement(pack[name], props);
  return react__WEBPACK_IMPORTED_MODULE_1___default.a.createElement(_components_Wrapper__WEBPACK_IMPORTED_MODULE_2__["default"], {
    identity: identity,
    updateAspects: updateAspects,
    component: element,
    connect: connect,
    package_name: package_name,
    component_name: name,
    aspects: props,
    disconnect: disconnect,
    key: "wrapper-".concat(identity)
  });
}
function prepareProp(prop) {
  if (react__WEBPACK_IMPORTED_MODULE_1___default.a.isValidElement(prop)) {
    return {
      identity: prop.props.identity,
      aspects: Object(ramda__WEBPACK_IMPORTED_MODULE_0__["map"])(prepareProp, Object(ramda__WEBPACK_IMPORTED_MODULE_0__["omit"])(['identity', 'updateAspects', '_name', '_package', 'aspects', 'key'], prop.props.aspects)),
      name: prop.props.component_name,
      "package": prop.props.package_name
    };
  }

  if (Object(ramda__WEBPACK_IMPORTED_MODULE_0__["type"])(prop) === 'Array') {
    return prop.map(prepareProp);
  }

  if (Object(ramda__WEBPACK_IMPORTED_MODULE_0__["type"])(prop) === 'Object') {
    return Object(ramda__WEBPACK_IMPORTED_MODULE_0__["map"])(prepareProp, prop);
  }

  return prop;
}

/***/ }),

/***/ "./src/renderer/js/index.js":
/*!**********************************!*\
  !*** ./src/renderer/js/index.js ***!
  \**********************************/
/*! exports provided: Renderer, render */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "render", function() { return render; });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react_dom__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react-dom */ "react-dom");
/* harmony import */ var react_dom__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react_dom__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _components_Renderer__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./components/Renderer */ "./src/renderer/js/components/Renderer.jsx");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "Renderer", function() { return _components_Renderer__WEBPACK_IMPORTED_MODULE_2__["default"]; });





function render(_ref, element) {
  var baseUrl = _ref.baseUrl,
      ping = _ref.ping,
      ping_interval = _ref.ping_interval,
      retries = _ref.retries;
  react_dom__WEBPACK_IMPORTED_MODULE_1___default.a.render(react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(_components_Renderer__WEBPACK_IMPORTED_MODULE_2__["default"], {
    baseUrl: baseUrl,
    ping: ping,
    ping_interval: ping_interval,
    retries: retries
  }), element);
}



/***/ }),

/***/ "./src/renderer/js/requests.js":
/*!*************************************!*\
  !*** ./src/renderer/js/requests.js ***!
  \*************************************/
/*! exports provided: JSONHEADERS, xhrRequest, apiRequest */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "JSONHEADERS", function() { return JSONHEADERS; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "xhrRequest", function() { return xhrRequest; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "apiRequest", function() { return apiRequest; });
function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; var ownKeys = Object.keys(source); if (typeof Object.getOwnPropertySymbols === 'function') { ownKeys = ownKeys.concat(Object.getOwnPropertySymbols(source).filter(function (sym) { return Object.getOwnPropertyDescriptor(source, sym).enumerable; })); } ownKeys.forEach(function (key) { _defineProperty(target, key, source[key]); }); } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

/* eslint-disable no-magic-numbers */
var jsonPattern = /json/i;
/**
 * @typedef {Object} XhrOptions
 * @property {string} [method='GET']
 * @property {Object} [headers={}]
 * @property {string|Blob|ArrayBuffer|object|Array} [payload='']
 */

/**
 * @type {XhrOptions}
 */

var defaultXhrOptions = {
  method: 'GET',
  headers: {},
  payload: '',
  json: true
};
var JSONHEADERS = {
  'Content-Type': 'application/json'
};
/**
 * Xhr promise wrap.
 *
 * Fetch can't do put request, so xhr still useful.
 *
 * Auto parse json responses.
 * Cancellation: xhr.abort
 * @param {string} url
 * @param {XhrOptions} [options]
 * @return {Promise}
 */

function xhrRequest(url) {
  var options = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : defaultXhrOptions;
  return new Promise(function (resolve, reject) {
    var _defaultXhrOptions$op = _objectSpread({}, defaultXhrOptions, options),
        method = _defaultXhrOptions$op.method,
        headers = _defaultXhrOptions$op.headers,
        payload = _defaultXhrOptions$op.payload,
        json = _defaultXhrOptions$op.json;

    var xhr = new XMLHttpRequest();
    xhr.open(method, url);
    var head = json ? _objectSpread({}, JSONHEADERS, headers) : headers;
    Object.keys(head).forEach(function (k) {
      return xhr.setRequestHeader(k, head[k]);
    });

    xhr.onreadystatechange = function () {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status < 400) {
          var responseValue = xhr.response;

          if (jsonPattern.test(xhr.getResponseHeader('Content-Type'))) {
            responseValue = JSON.parse(xhr.responseText);
          }

          resolve(responseValue);
        } else {
          reject({
            error: 'RequestError',
            message: "XHR ".concat(url, " FAILED - STATUS: ").concat(xhr.status, " MESSAGE: ").concat(xhr.statusText),
            status: xhr.status,
            xhr: xhr
          });
        }
      }
    };

    xhr.onerror = function (err) {
      return reject(err);
    };

    xhr.send(json ? JSON.stringify(payload) : payload);
  });
}
/**
 * Auto get headers and refresh/retry.
 *
 * @param {function} getHeaders
 * @param {function} refresh
 * @param {string} baseUrl
 */

function apiRequest() {
  var baseUrl = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : '';
  return function () {
    var url = baseUrl + arguments[0];
    var options = arguments[1] || {};
    options.headers = _objectSpread({}, options.headers);
    return new Promise(function (resolve) {
      xhrRequest(url, options).then(resolve);
    });
  };
}

/***/ }),

/***/ "./src/renderer/js/requirements.js":
/*!*****************************************!*\
  !*** ./src/renderer/js/requirements.js ***!
  \*****************************************/
/*! exports provided: loadRequirement, loadRequirements */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "loadRequirement", function() { return loadRequirement; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "loadRequirements", function() { return loadRequirements; });
/* harmony import */ var _commons_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../commons/js */ "./src/commons/js/index.js");

function loadRequirement(requirement) {
  return new Promise(function (resolve, reject) {
    var url = requirement.url,
        kind = requirement.kind,
        meta = requirement.meta;
    var method;

    if (kind === 'js') {
      method = _commons_js__WEBPACK_IMPORTED_MODULE_0__["loadScript"];
    } else if (kind === 'css') {
      method = _commons_js__WEBPACK_IMPORTED_MODULE_0__["loadCss"];
    } else if (kind === 'map') {
      return resolve();
    } else {
      return reject({
        error: "Invalid requirement kind: ".concat(kind)
      });
    }

    return method(url, meta).then(resolve)["catch"](reject);
  });
}
function loadRequirements(requirements, packages) {
  return new Promise(function (resolve, reject) {
    var loadings = []; // Load packages first.

    Object.keys(packages).forEach(function (pack_name) {
      var pack = packages[pack_name];
      loadings = loadings.concat(pack.requirements.map(loadRequirement));
    }); // Then load requirements so they can use packages
    // and override css.

    Promise.all(loadings).then(function () {
      var i = 0; // Load in order.

      var handler = function handler() {
        if (i < requirements.length) {
          loadRequirement(requirements[i]).then(function () {
            i++;
            handler();
          });
        } else {
          resolve();
        }
      };

      handler();
    })["catch"](reject);
  });
}

/***/ }),

/***/ 1:
/*!****************************************!*\
  !*** multi ./src/renderer/js/index.js ***!
  \****************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__(/*! /home/t4rk/projects/experiments/dazzler/src/renderer/js/index.js */"./src/renderer/js/index.js");


/***/ }),

/***/ "react":
/*!****************************************************************************************************!*\
  !*** external {"commonjs":"react","commonjs2":"react","amd":"react","umd":"react","root":"React"} ***!
  \****************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = __WEBPACK_EXTERNAL_MODULE_react__;

/***/ }),

/***/ "react-dom":
/*!***********************************************************************************************************************!*\
  !*** external {"commonjs":"react-dom","commonjs2":"react-dom","amd":"react-dom","umd":"react-dom","root":"ReactDOM"} ***!
  \***********************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = __WEBPACK_EXTERNAL_MODULE_react_dom__;

/***/ })

/******/ });
});
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8vd2VicGFjay91bml2ZXJzYWxNb2R1bGVEZWZpbml0aW9uPyIsIndlYnBhY2s6Ly8vd2VicGFjay9ib290c3RyYXA/Iiwid2VicGFjazovLy8uL3NyYy9yZW5kZXJlci9qcy9jb21wb25lbnRzL1JlbmRlcmVyLmpzeD8iLCJ3ZWJwYWNrOi8vLy4vc3JjL3JlbmRlcmVyL2pzL2NvbXBvbmVudHMvVXBkYXRlci5qc3g/Iiwid2VicGFjazovLy8uL3NyYy9yZW5kZXJlci9qcy9jb21wb25lbnRzL1dyYXBwZXIuanN4PyIsIndlYnBhY2s6Ly8vLi9zcmMvcmVuZGVyZXIvanMvaHlkcmF0b3IuanM/Iiwid2VicGFjazovLy8uL3NyYy9yZW5kZXJlci9qcy9pbmRleC5qcz8iLCJ3ZWJwYWNrOi8vLy4vc3JjL3JlbmRlcmVyL2pzL3JlcXVlc3RzLmpzPyIsIndlYnBhY2s6Ly8vLi9zcmMvcmVuZGVyZXIvanMvcmVxdWlyZW1lbnRzLmpzPyIsIndlYnBhY2s6Ly8vZXh0ZXJuYWwge1wiY29tbW9uanNcIjpcInJlYWN0XCIsXCJjb21tb25qczJcIjpcInJlYWN0XCIsXCJhbWRcIjpcInJlYWN0XCIsXCJ1bWRcIjpcInJlYWN0XCIsXCJyb290XCI6XCJSZWFjdFwifT8iLCJ3ZWJwYWNrOi8vL2V4dGVybmFsIHtcImNvbW1vbmpzXCI6XCJyZWFjdC1kb21cIixcImNvbW1vbmpzMlwiOlwicmVhY3QtZG9tXCIsXCJhbWRcIjpcInJlYWN0LWRvbVwiLFwidW1kXCI6XCJyZWFjdC1kb21cIixcInJvb3RcIjpcIlJlYWN0RE9NXCJ9PyJdLCJuYW1lcyI6WyJSZW5kZXJlciIsInByb3BzIiwic3RhdGUiLCJyZWxvYWRLZXkiLCJ3aW5kb3ciLCJkYXp6bGVyX2Jhc2VfdXJsIiwiYmFzZVVybCIsInNldFN0YXRlIiwiUmVhY3QiLCJDb21wb25lbnQiLCJwcm9wVHlwZXMiLCJQcm9wVHlwZXMiLCJzdHJpbmciLCJpc1JlcXVpcmVkIiwicGluZyIsImJvb2wiLCJwaW5nX2ludGVydmFsIiwibnVtYmVyIiwicmV0cmllcyIsIlVwZGF0ZXIiLCJsYXlvdXQiLCJyZWFkeSIsInBhZ2UiLCJiaW5kaW5ncyIsInBhY2thZ2VzIiwicmVxdWlyZW1lbnRzIiwicmVsb2FkaW5nIiwibmVlZFJlZnJlc2giLCJwYWdlQXBpIiwiYXBpUmVxdWVzdCIsImxvY2F0aW9uIiwiaHJlZiIsImJvdW5kQ29tcG9uZW50cyIsIndzIiwidXBkYXRlQXNwZWN0cyIsImJpbmQiLCJjb25uZWN0IiwiZGlzY29ubmVjdCIsIm9uTWVzc2FnZSIsImlkZW50aXR5IiwiYXNwZWN0cyIsIlByb21pc2UiLCJyZXNvbHZlIiwiT2JqZWN0Iiwia2V5cyIsIm1hcCIsImtleSIsImZpbHRlciIsImUiLCJmb3JFYWNoIiwiYmluZGluZyIsInNlbmRCaW5kaW5nIiwidHJpZ2dlciIsImFzcGVjdCIsInNldEFzcGVjdHMiLCJnZXRBc3BlY3QiLCJyZXNwb25zZSIsImRhdGEiLCJKU09OIiwicGFyc2UiLCJraW5kIiwicGF5bG9hZCIsInN0b3JhZ2UiLCJyZXF1ZXN0X2lkIiwic3RvcmUiLCJzZXNzaW9uU3RvcmFnZSIsImxvY2FsU3RvcmFnZSIsImNvbXBvbmVudCIsImVycm9yIiwic2VuZCIsInN0cmluZ2lmeSIsImNvbnNvbGUiLCJoeWRyYXRlUHJvcHMiLCJ0aGVuIiwiayIsIndhbnRlZCIsInZhbHVlIiwicHJlcGFyZVByb3AiLCJzZXRJdGVtIiwiZ2V0SXRlbSIsImZpbGVuYW1lcyIsImhvdCIsInJlZnJlc2giLCJkZWxldGVkIiwiY2xvc2UiLCJsb2FkUmVxdWlyZW1lbnQiLCJyIiwiZGlzYWJsZUNzcyIsInVybCIsInN0YXRlcyIsInRyaWVzIiwiaGFyZENsb3NlIiwiY29ubmV4aW9uIiwiV2ViU29ja2V0Iiwic3RhcnRzV2l0aCIsImhvc3QiLCJwYXRobmFtZSIsImFkZEV2ZW50TGlzdGVuZXIiLCJvbm9wZW4iLCJyZWxvYWQiLCJob3RSZWxvYWQiLCJvbmNsb3NlIiwicmVjb25uZWN0Iiwic2V0VGltZW91dCIsIm1ldGhvZCIsImxvYWRSZXF1aXJlbWVudHMiLCJsZW5ndGgiLCJfY29ubmVjdFdTIiwiaXNDb21wb25lbnQiLCJFcnJvciIsImh5ZHJhdGVDb21wb25lbnQiLCJuYW1lIiwiZGVmYXVsdFByb3BzIiwiZnVuYyIsIldyYXBwZXIiLCJpbml0aWFsIiwiY29tcG9uZW50X25hbWUiLCJwYWNrYWdlX25hbWUiLCJjbG9uZUVsZW1lbnQiLCJjbGFzc19uYW1lIiwiam9pbiIsImNvbmNhdCIsInJlcGxhY2UiLCJ0b0xvd2VyQ2FzZSIsImNhbWVsVG9TcGluYWwiLCJzcGxpdCIsIm5vZGUiLCJjIiwidHlwZSIsImhhc093blByb3BlcnR5IiwiZW50cmllcyIsInYiLCJuZXdQcm9wcyIsInBhY2siLCJlbGVtZW50IiwiY3JlYXRlRWxlbWVudCIsInByb3AiLCJpc1ZhbGlkRWxlbWVudCIsIm9taXQiLCJyZW5kZXIiLCJSZWFjdERPTSIsImpzb25QYXR0ZXJuIiwiZGVmYXVsdFhock9wdGlvbnMiLCJoZWFkZXJzIiwianNvbiIsIkpTT05IRUFERVJTIiwieGhyUmVxdWVzdCIsIm9wdGlvbnMiLCJyZWplY3QiLCJ4aHIiLCJYTUxIdHRwUmVxdWVzdCIsIm9wZW4iLCJoZWFkIiwic2V0UmVxdWVzdEhlYWRlciIsIm9ucmVhZHlzdGF0ZWNoYW5nZSIsInJlYWR5U3RhdGUiLCJET05FIiwic3RhdHVzIiwicmVzcG9uc2VWYWx1ZSIsInRlc3QiLCJnZXRSZXNwb25zZUhlYWRlciIsInJlc3BvbnNlVGV4dCIsIm1lc3NhZ2UiLCJzdGF0dXNUZXh0Iiwib25lcnJvciIsImVyciIsImFyZ3VtZW50cyIsInJlcXVpcmVtZW50IiwibWV0YSIsImxvYWRTY3JpcHQiLCJsb2FkQ3NzIiwibG9hZGluZ3MiLCJwYWNrX25hbWUiLCJhbGwiLCJpIiwiaGFuZGxlciJdLCJtYXBwaW5ncyI6IkFBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsQ0FBQztBQUNELE87QUNWQTtBQUNBO0FB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S0FmTCxXQWdCVzNCLE1BaEJYO0FBaUJILEdBMUJNLENBQVA7QUEyQkgsQzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUNqREQsbUQ7Ozs7Ozs7Ozs7O0FDQUEsdUQiLCJmaWxlIjoiZGF6emxlcl9yZW5kZXJlcl85YmQyNThiNDkyZmI5ODNhNjZhNi5qcyIsInNvdXJjZXNDb250ZW50IjpbIihmdW5jdGlvbiB3ZWJwYWNrVW5pdmVyc2FsTW9kdWxlRGVmaW5pdGlvbihyb290LCBmYWN0b3J5KSB7XG5cdGlmKHR5cGVvZiBleHBvcnRzID09PSAnb2JqZWN0JyAmJiB0eXBlb2YgbW9kdWxlID09PSAnb2JqZWN0Jylcblx0XHRtb2R1bGUuZXhwb3J0cyA9IGZhY3RvcnkocmVxdWlyZShcInJlYWN0XCIpLCByZXF1aXJlKFwicmVhY3QtZG9tXCIpKTtcblx0ZWxzZSBpZih0eXBlb2YgZGVmaW5lID09PSAnZnVuY3Rpb24nICYmIGRlZmluZS5hbWQpXG5cdFx0ZGVmaW5lKFtcInJlYWN0XCIsIFwicmVhY3QtZG9tXCJdLCBmYWN0b3J5KTtcblx0ZWxzZSBpZih0eXBlb2YgZXhwb3J0cyA9PT0gJ29iamVjdCcpXG5cdFx0ZXhwb3J0c1tcImRhenpsZXJfcmVuZGVyZXJcIl0gPSBmYWN0b3J5KHJlcXVpcmUoXCJyZWFjdFwiKSwgcmVxdWlyZShcInJlYWN0LWRvbVwiKSk7XG5cdGVsc2Vcblx0XHRyb290W1wiZGF6emxlcl9yZW5kZXJlclwiXSA9IGZhY3Rvcnkocm9vdFtcIlJlYWN0XCJdLCByb290W1wiUmVhY3RET01cIl0pO1xufSkod2luZG93LCBmdW5jdGlvbihfX1dFQlBBQ0tfRVhURVJOQUxfTU9EVUxFX3JlYWN0X18sIF9fV0VCUEFDS19FWFRFUk5BTF9NT0RVTEVfcmVhY3RfZG9tX18pIHtcbnJldHVybiAiLCIgXHQvLyBpbnN0YWxsIGEgSlNPTlAgY2FsbGJhY2sgZm9yIGNodW5rIGxvYWRpbmdcbiBcdGZ1bmN0aW9uIHdlYnBhY2tKc29ucENhbGxiYWNrKGRhdGEpIHtcbiBcdFx0dmFyIGNodW5rSWRzID0gZGF0YVswXTtcbiBcdFx0dmFyIG1vcmVNb2R1bGVzID0gZGF0YVsxXTtcbiBcdFx0dmFyIGV4ZWN1dGVNb2R1bGVzID0gZGF0YVsyXTtcblxuIFx0XHQvLyBhZGQgXCJtb3JlTW9kdWxlc1wiIHRvIHRoZSBtb2R1bGVzIG9iamVjdCxcbiBcdFx0Ly8gdGhlbiBmbGFnIGFsbCBcImNodW5rSWRzXCIgYXMgbG9hZGVkIGFuZCBmaXJlIGNhbGxiYWNrXG4gXHRcdHZhciBtb2R1bGVJZCwgY2h1bmtJZCwgaSA9IDAsIHJlc29sdmVzID0gW107XG4gXHRcdGZvcig7aSA8IGNodW5rSWRzLmxlbmd0aDsgaSsrKSB7XG4gXHRcdFx0Y2h1bmtJZCA9IGNodW5rSWRzW2ldO1xuIFx0XHRcdGlmKGluc3RhbGxlZENodW5rc1tjaHVua0lkXSkge1xuIFx0XHRcdFx0cmVzb2x2ZXMucHVzaChpbnN0YWxsZWRDaHVua3NbY2h1bmtJZF1bMF0pO1xuIFx0XHRcdH1cbiBcdFx0XHRpbnN0YWxsZWRDaHVua3NbY2h1bmtJZF0gPSAwO1xuIFx0XHR9XG4gXHRcdGZvcihtb2R1bGVJZCBpbiBtb3JlTW9kdWxlcykge1xuIFx0XHRcdGlmKE9iamVjdC5wcm90b3R5cGUuaGFzT3duUHJvcGVydHkuY2FsbChtb3JlTW9kdWxlcywgbW9kdWxlSWQpKSB7XG4gXHRcdFx0XHRtb2R1bGVzW21vZHVsZUlkXSA9IG1vcmVNb2R1bGVzW21vZHVsZUlkXTtcbiBcdFx0XHR9XG4gXHRcdH1cbiBcdFx0aWYocGFyZW50SnNvbnBGdW5jdGlvbikgcGFyZW50SnNvbnBGdW5jdGlvbihkYXRhKTtcblxuIFx0XHR3aGlsZShyZXNvbHZlcy5sZW5ndGgpIHtcbiBcdFx0XHRyZXNvbHZlcy5zaGlmdCgpKCk7XG4gXHRcdH1cblxuIFx0XHQvLyBhZGQgZW50cnkgbW9kdWxlcyBmcm9tIGxvYWRlZCBjaHVuayB0byBkZWZlcnJlZCBsaXN0XG4gXHRcdGRlZmVycmVkTW9kdWxlcy5wdXNoLmFwcGx5KGRlZmVycmVkTW9kdWxlcywgZXhlY3V0ZU1vZHVsZXMgfHwgW10pO1xuXG4gXHRcdC8vIHJ1biBkZWZlcnJlZCBtb2R1bGVzIHdoZW4gYWxsIGNodW5rcyByZWFkeVxuIFx0XHRyZXR1cm4gY2hlY2tEZWZlcnJlZE1vZHVsZXMoKTtcbiBcdH07XG4gXHRmdW5jdGlvbiBjaGVja0RlZmVycmVkTW9kdWxlcygpIHtcbiBcdFx0dmFyIHJlc3VsdDtcbiBcdFx0Zm9yKHZhciBpID0gMDsgaSA8IGRlZmVycmVkTW9kdWxlcy5sZW5ndGg7IGkrKykge1xuIFx0XHRcdHZhciBkZWZlcnJlZE1vZHVsZSA9IGRlZmVycmVkTW9kdWxlc1tpXTtcbiBcdFx0XHR2YXIgZnVsZmlsbGVkID0gdHJ1ZTtcbiBcdFx0XHRmb3IodmFyIGogPSAxOyBqIDwgZGVmZXJyZWRNb2R1bGUubGVuZ3RoOyBqKyspIHtcbiBcdFx0XHRcdHZhciBkZXBJZCA9IGRlZmVycmVkTW9kdWxlW2pdO1xuIFx0XHRcdFx0aWYoaW5zdGFsbGVkQ2h1bmtzW2RlcElkXSAhPT0gMCkgZnVsZmlsbGVkID0gZmFsc2U7XG4gXHRcdFx0fVxuIFx0XHRcdGlmKGZ1bGZpbGxlZCkge1xuIFx0XHRcdFx0ZGVmZXJyZWRNb2R1bGVzLnNwbGljZShpLS0sIDEpO1xuIFx0XHRcdFx0cmVzdWx0ID0gX193ZWJwYWNrX3JlcXVpcmVfXyhfX3dlYnBhY2tfcmVxdWlyZV9fLnMgPSBkZWZlcnJlZE1vZHVsZVswXSk7XG4gXHRcdFx0fVxuIFx0XHR9XG5cbiBcdFx0cmV0dXJuIHJlc3VsdDtcbiBcdH1cblxuIFx0Ly8gVGhlIG1vZHVsZSBjYWNoZVxuIFx0dmFyIGluc3RhbGxlZE1vZHVsZXMgPSB7fTtcblxuIFx0Ly8gb2JqZWN0IHRvIHN0b3JlIGxvYWRlZCBhbmQgbG9hZGluZyBjaHVua3NcbiBcdC8vIHVuZGVmaW5lZCA9IGNodW5rIG5vdCBsb2FkZWQsIG51bGwgPSBjaHVuayBwcmVsb2FkZWQvcHJlZmV0Y2hlZFxuIFx0Ly8gUHJvbWlzZSA9IGNodW5rIGxvYWRpbmcsIDAgPSBjaHVuayBsb2FkZWRcbiBcdHZhciBpbnN0YWxsZWRDaHVua3MgPSB7XG4gXHRcdFwicmVuZGVyZXJcIjogMFxuIFx0fTtcblxuIFx0dmFyIGRlZmVycmVkTW9kdWxlcyA9IFtdO1xuXG4gXHQvLyBUaGUgcmVxdWlyZSBmdW5jdGlvblxuIFx0ZnVuY3Rpb24gX193ZWJwYWNrX3JlcXVpcmVfXyhtb2R1bGVJZCkge1xuXG4gXHRcdC8vIENoZWNrIGlmIG1vZHVsZSBpcyBpbiBjYWNoZVxuIFx0XHRpZihpbnN0YWxsZWRNb2R1bGVzW21vZHVsZUlkXSkge1xuIFx0XHRcdHJldHVybiBpbnN0YWxsZWRNb2R1bGVzW21vZHVsZUlkXS5leHBvcnRzO1xuIFx0XHR9XG4gXHRcdC8vIENyZWF0ZSBhIG5ldyBtb2R1bGUgKGFuZCBwdXQgaXQgaW50byB0aGUgY2FjaGUpXG4gXHRcdHZhciBtb2R1bGUgPSBpbnN0YWxsZWRNb2R1bGVzW21vZHVsZUlkXSA9IHtcbiBcdFx0XHRpOiBtb2R1bGVJZCxcbiBcdFx0XHRsOiBmYWxzZSxcbiBcdFx0XHRleHBvcnRzOiB7fVxuIFx0XHR9O1xuXG4gXHRcdC8vIEV4ZWN1dGUgdGhlIG1vZHVsZSBmdW5jdGlvblxuIFx0XHRtb2R1bGVzW21vZHVsZUlkXS5jYWxsKG1vZHVsZS5leHBvcnRzLCBtb2R1bGUsIG1vZHVsZS5leHBvcnRzLCBfX3dlYnBhY2tfcmVxdWlyZV9fKTtcblxuIFx0XHQvLyBGbGFnIHRoZSBtb2R1bGUgYXMgbG9hZGVkXG4gXHRcdG1vZHVsZS5sID0gdHJ1ZTtcblxuIFx0XHQvLyBSZXR1cm4gdGhlIGV4cG9ydHMgb2YgdGhlIG1vZHVsZVxuIFx0XHRyZXR1cm4gbW9kdWxlLmV4cG9ydHM7XG4gXHR9XG5cblxuIFx0Ly8gZXhwb3NlIHRoZSBtb2R1bGVzIG9iamVjdCAoX193ZWJwYWNrX21vZHVsZXNfXylcbiBcdF9fd2VicGFja19yZXF1aXJlX18ubSA9IG1vZHVsZXM7XG5cbiBcdC8vIGV4cG9zZSB0aGUgbW9kdWxlIGNhY2hlXG4gXHRfX3dlYnBhY2tfcmVxdWlyZV9fLmMgPSBpbnN0YWxsZWRNb2R1bGVzO1xuXG4gXHQvLyBkZWZpbmUgZ2V0dGVyIGZ1bmN0aW9uIGZvciBoYXJtb255IGV4cG9ydHNcbiBcdF9fd2VicGFja19yZXF1aXJlX18uZCA9IGZ1bmN0aW9uKGV4cG9ydHMsIG5hbWUsIGdldHRlcikge1xuIFx0XHRpZighX193ZWJwYWNrX3JlcXVpcmVfXy5vKGV4cG9ydHMsIG5hbWUpKSB7XG4gXHRcdFx0T2JqZWN0LmRlZmluZVByb3BlcnR5KGV4cG9ydHMsIG5hbWUsIHsgZW51bWVyYWJsZTogdHJ1ZSwgZ2V0OiBnZXR0ZXIgfSk7XG4gXHRcdH1cbiBcdH07XG5cbiBcdC8vIGRlZmluZSBfX2VzTW9kdWxlIG9uIGV4cG9ydHNcbiBcdF9fd2VicGFja19yZXF1aXJlX18uciA9IGZ1bmN0aW9uKGV4cG9ydHMpIHtcbiBcdFx0aWYodHlwZW9mIFN5bWJvbCAhPT0gJ3VuZGVmaW5lZCcgJiYgU3ltYm9sLnRvU3RyaW5nVGFnKSB7XG4gXHRcdFx0T2JqZWN0LmRlZmluZVByb3BlcnR5KGV4cG9ydHMsIFN5bWJvbC50b1N0cmluZ1RhZywgeyB2YWx1ZTogJ01vZHVsZScgfSk7XG4gXHRcdH1cbiBcdFx0T2JqZWN0LmRlZmluZVByb3BlcnR5KGV4cG9ydHMsICdfX2VzTW9kdWxlJywgeyB2YWx1ZTogdHJ1ZSB9KTtcbiBcdH07XG5cbiBcdC8vIGNyZWF0ZSBhIGZha2UgbmFtZXNwYWNlIG9iamVjdFxuIFx0Ly8gbW9kZSAmIDE6IHZhbHVlIGlzIGEgbW9kdWxlIGlkLCByZXF1aXJlIGl0XG4gXHQvLyBtb2RlICYgMjogbWVyZ2UgYWxsIHByb3BlcnRpZXMgb2YgdmFsdWUgaW50byB0aGUgbnNcbiBcdC8vIG1vZGUgJiA0OiByZXR1cm4gdmFsdWUgd2hlbiBhbHJlYWR5IG5zIG9iamVjdFxuIFx0Ly8gbW9kZSAmIDh8MTogYmVoYXZlIGxpa2UgcmVxdWlyZVxuIFx0X193ZWJwYWNrX3JlcXVpcmVfXy50ID0gZnVuY3Rpb24odmFsdWUsIG1vZGUpIHtcbiBcdFx0aWYobW9kZSAmIDEpIHZhbHVlID0gX193ZWJwYWNrX3JlcXVpcmVfXyh2YWx1ZSk7XG4gXHRcdGlmKG1vZGUgJiA4KSByZXR1cm4gdmFsdWU7XG4gXHRcdGlmKChtb2RlICYgNCkgJiYgdHlwZW9mIHZhbHVlID09PSAnb2JqZWN0JyAmJiB2YWx1ZSAmJiB2YWx1ZS5fX2VzTW9kdWxlKSByZXR1cm4gdmFsdWU7XG4gXHRcdHZhciBucyA9IE9iamVjdC5jcmVhdGUobnVsbCk7XG4gXHRcdF9fd2VicGFja19yZXF1aXJlX18ucihucyk7XG4gXHRcdE9iamVjdC5kZWZpbmVQcm9wZXJ0eShucywgJ2RlZmF1bHQnLCB7IGVudW1lcmFibGU6IHRydWUsIHZhbHVlOiB2YWx1ZSB9KTtcbiBcdFx0aWYobW9kZSAmIDIgJiYgdHlwZW9mIHZhbHVlICE9ICdzdHJpbmcnKSBmb3IodmFyIGtleSBpbiB2YWx1ZSkgX193ZWJwYWNrX3JlcXVpcmVfXy5kKG5zLCBrZXksIGZ1bmN0aW9uKGtleSkgeyByZXR1cm4gdmFsdWVba2V5XTsgfS5iaW5kKG51bGwsIGtleSkpO1xuIFx0XHRyZXR1cm4gbnM7XG4gXHR9O1xuXG4gXHQvLyBnZXREZWZhdWx0RXhwb3J0IGZ1bmN0aW9uIGZvciBjb21wYXRpYmlsaXR5IHdpdGggbm9uLWhhcm1vbnkgbW9kdWxlc1xuIFx0X193ZWJwYWNrX3JlcXVpcmVfXy5uID0gZnVuY3Rpb24obW9kdWxlKSB7XG4gXHRcdHZhciBnZXR0ZXIgPSBtb2R1bGUgJiYgbW9kdWxlLl9fZXNNb2R1bGUgP1xuIFx0XHRcdGZ1bmN0aW9uIGdldERlZmF1bHQoKSB7IHJldHVybiBtb2R1bGVbJ2RlZmF1bHQnXTsgfSA6XG4gXHRcdFx0ZnVuY3Rpb24gZ2V0TW9kdWxlRXhwb3J0cygpIHsgcmV0dXJuIG1vZHVsZTsgfTtcbiBcdFx0X193ZWJwYWNrX3JlcXVpcmVfXy5kKGdldHRlciwgJ2EnLCBnZXR0ZXIpO1xuIFx0XHRyZXR1cm4gZ2V0dGVyO1xuIFx0fTtcblxuIFx0Ly8gT2JqZWN0LnByb3RvdHlwZS5oYXNPd25Qcm9wZXJ0eS5jYWxsXG4gXHRfX3dlYnBhY2tfcmVxdWlyZV9fLm8gPSBmdW5jdGlvbihvYmplY3QsIHByb3BlcnR5KSB7IHJldHVybiBPYmplY3QucHJvdG90eXBlLmhhc093blByb3BlcnR5LmNhbGwob2JqZWN0LCBwcm9wZXJ0eSk7IH07XG5cbiBcdC8vIF9fd2VicGFja19wdWJsaWNfcGF0aF9fXG4gXHRfX3dlYnBhY2tfcmVxdWlyZV9fLnAgPSBcIlwiO1xuXG4gXHR2YXIganNvbnBBcnJheSA9IHdpbmRvd1tcIndlYnBhY2tKc29ucGRhenpsZXJfbmFtZV9cIl0gPSB3aW5kb3dbXCJ3ZWJwYWNrSnNvbnBkYXp6bGVyX25hbWVfXCJdIHx8IFtdO1xuIFx0dmFyIG9sZEpzb25wRnVuY3Rpb24gPSBqc29ucEFycmF5LnB1c2guYmluZChqc29ucEFycmF5KTtcbiBcdGpzb25wQXJyYXkucHVzaCA9IHdlYnBhY2tKc29ucENhbGxiYWNrO1xuIFx0anNvbnBBcnJheSA9IGpzb25wQXJyYXkuc2xpY2UoKTtcbiBcdGZvcih2YXIgaSA9IDA7IGkgPCBqc29ucEFycmF5Lmxlbmd0aDsgaSsrKSB3ZWJwYWNrSnNvbnBDYWxsYmFjayhqc29ucEFycmF5W2ldKTtcbiBcdHZhciBwYXJlbnRKc29ucEZ1bmN0aW9uID0gb2xkSnNvbnBGdW5jdGlvbjtcblxuXG4gXHQvLyBhZGQgZW50cnkgbW9kdWxlIHRvIGRlZmVycmVkIGxpc3RcbiBcdGRlZmVycmVkTW9kdWxlcy5wdXNoKFsxLFwiY29tbW9uc1wiXSk7XG4gXHQvLyBydW4gZGVmZXJyZWQgbW9kdWxlcyB3aGVuIHJlYWR5XG4gXHRyZXR1cm4gY2hlY2tEZWZlcnJlZE1vZHVsZXMoKTtcbiIsImltcG9ydCBSZWFjdCBmcm9tICdyZWFjdCc7XG5pbXBvcnQgVXBkYXRlciBmcm9tICcuL1VwZGF0ZXInO1xuaW1wb3J0IFByb3BUeXBlcyBmcm9tICdwcm9wLXR5cGVzJztcblxuZXhwb3J0IGRlZmF1bHQgY2xhc3MgUmVuZGVyZXIgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICAgIGNvbnN0cnVjdG9yKHByb3BzKSB7XG4gICAgICAgIHN1cGVyKHByb3BzKTtcbiAgICAgICAgdGhpcy5zdGF0ZSA9IHtcbiAgICAgICAgICAgIHJlbG9hZEtleTogMSxcbiAgICAgICAgfTtcbiAgICB9XG4gICAgY29tcG9uZW50V2lsbE1vdW50KCkge1xuICAgICAgICB3aW5kb3cuZGF6emxlcl9iYXNlX3VybCA9IHRoaXMucHJvcHMuYmFzZVVybDtcbiAgICB9XG5cbiAgICByZW5kZXIoKSB7XG4gICAgICAgIHJldHVybiAoXG4gICAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImRhenpsZXItcmVuZGVyZXJcIj5cbiAgICAgICAgICAgICAgICA8VXBkYXRlclxuICAgICAgICAgICAgICAgICAgICB7Li4udGhpcy5wcm9wc31cbiAgICAgICAgICAgICAgICAgICAga2V5PXtgdXBkLSR7dGhpcy5zdGF0ZS5yZWxvYWRLZXl9YH1cbiAgICAgICAgICAgICAgICAgICAgaG90UmVsb2FkPXsoKSA9PlxuICAgICAgICAgICAgICAgICAgICAgICAgdGhpcy5zZXRTdGF0ZSh7cmVsb2FkS2V5OiB0aGlzLnN0YXRlLnJlbG9hZEtleSArIDF9KVxuICAgICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgLz5cbiAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICApO1xuICAgIH1cbn1cblxuUmVuZGVyZXIucHJvcFR5cGVzID0ge1xuICAgIGJhc2VVcmw6IFByb3BUeXBlcy5zdHJpbmcuaXNSZXF1aXJlZCxcbiAgICBwaW5nOiBQcm9wVHlwZXMuYm9vbCxcbiAgICBwaW5nX2ludGVydmFsOiBQcm9wVHlwZXMubnVtYmVyLFxuICAgIHJldHJpZXM6IFByb3BUeXBlcy5udW1iZXIsXG59O1xuIiwiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcbmltcG9ydCBQcm9wVHlwZXMgZnJvbSAncHJvcC10eXBlcyc7XG5pbXBvcnQge2FwaVJlcXVlc3R9IGZyb20gJy4uL3JlcXVlc3RzJztcbmltcG9ydCB7XG4gICAgaHlkcmF0ZUNvbXBvbmVudCxcbiAgICBoeWRyYXRlUHJvcHMsXG4gICAgaXNDb21wb25lbnQsXG4gICAgcHJlcGFyZVByb3AsXG59IGZyb20gJy4uL2h5ZHJhdG9yJztcbmltcG9ydCB7bG9hZFJlcXVpcmVtZW50LCBsb2FkUmVxdWlyZW1lbnRzfSBmcm9tICcuLi9yZXF1aXJlbWVudHMnO1xuaW1wb3J0IHtkaXNhYmxlQ3NzfSBmcm9tICcuLi8uLi8uLi9jb21tb25zL2pzL3V0aWxzJztcblxuZXhwb3J0IGRlZmF1bHQgY2xhc3MgVXBkYXRlciBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gICAgY29uc3RydWN0b3IocHJvcHMpIHtcbiAgICAgICAgc3VwZXIocHJvcHMpO1xuICAgICAgICB0aGlzLnN0YXRlID0ge1xuICAgICAgICAgICAgbGF5b3V0OiBmYWxzZSxcbiAgICAgICAgICAgIHJlYWR5OiBmYWxzZSxcbiAgICAgICAgICAgIHBhZ2U6IG51bGwsXG4gICAgICAgICAgICBiaW5kaW5nczoge30sXG4gICAgICAgICAgICBwYWNrYWdlczogW10sXG4gICAgICAgICAgICByZXF1aXJlbWVudHM6IFtdLFxuICAgICAgICAgICAgcmVsb2FkaW5nOiBmYWxzZSxcbiAgICAgICAgICAgIG5lZWRSZWZyZXNoOiBmYWxzZSxcbiAgICAgICAgfTtcbiAgICAgICAgLy8gVGhlIGFwaSB1cmwgZm9yIHRoZSBwYWdlIGlzIHRoZSBzYW1lIGJ1dCBhIHBvc3QuXG4gICAgICAgIC8vIEZldGNoIGJpbmRpbmdzLCBwYWNrYWdlcyAmIHJlcXVpcmVtZW50c1xuICAgICAgICB0aGlzLnBhZ2VBcGkgPSBhcGlSZXF1ZXN0KHdpbmRvdy5sb2NhdGlvbi5ocmVmKTtcbiAgICAgICAgLy8gQWxsIGNvbXBvbmVudHMgZ2V0IGNvbm5lY3RlZC5cbiAgICAgICAgdGhpcy5ib3VuZENvbXBvbmVudHMgPSB7fTtcbiAgICAgICAgdGhpcy53cyA9IG51bGw7XG5cbiAgICAgICAgdGhpcy51cGRhdGVBc3BlY3RzID0gdGhpcy51cGRhdGVBc3BlY3RzLmJpbmQodGhpcyk7XG4gICAgICAgIHRoaXMuY29ubmVjdCA9IHRoaXMuY29ubmVjdC5iaW5kKHRoaXMpO1xuICAgICAgICB0aGlzLmRpc2Nvbm5lY3QgPSB0aGlzLmRpc2Nvbm5lY3QuYmluZCh0aGlzKTtcbiAgICAgICAgdGhpcy5vbk1lc3NhZ2UgPSB0aGlzLm9uTWVzc2FnZS5iaW5kKHRoaXMpO1xuICAgIH1cblxuICAgIHVwZGF0ZUFzcGVjdHMoaWRlbnRpdHksIGFzcGVjdHMpIHtcbiAgICAgICAgcmV0dXJuIG5ldyBQcm9taXNlKHJlc29sdmUgPT4ge1xuICAgICAgICAgICAgY29uc3QgYmluZGluZ3MgPSBPYmplY3Qua2V5cyhhc3BlY3RzKVxuICAgICAgICAgICAgICAgIC5tYXAoa2V5ID0+IHRoaXMuc3RhdGUuYmluZGluZ3NbYCR7aWRlbnRpdHl9LiR7a2V5fWBdKVxuICAgICAgICAgICAgICAgIC5maWx0ZXIoZSA9PiBlKTtcblxuICAgICAgICAgICAgaWYgKCFiaW5kaW5ncykge1xuICAgICAgICAgICAgICAgIHJldHVybiByZXNvbHZlKDApO1xuICAgICAgICAgICAgfVxuXG4gICAgICAgICAgICBiaW5kaW5ncy5mb3JFYWNoKGJpbmRpbmcgPT5cbiAgICAgICAgICAgICAgICB0aGlzLnNlbmRCaW5kaW5nKGJpbmRpbmcsIGFzcGVjdHNbYmluZGluZy50cmlnZ2VyLmFzcGVjdF0pXG4gICAgICAgICAgICApO1xuICAgICAgICAgICAgcmVzb2x2ZSgpO1xuICAgICAgICB9KTtcbiAgICB9XG5cbiAgICBjb25uZWN0KGlkZW50aXR5LCBzZXRBc3BlY3RzLCBnZXRBc3BlY3QpIHtcbiAgICAgICAgdGhpcy5ib3VuZENvbXBvbmVudHNbaWRlbnRpdHldID0ge1xuICAgICAgICAgICAgc2V0QXNwZWN0cyxcbiAgICAgICAgICAgIGdldEFzcGVjdCxcbiAgICAgICAgfTtcbiAgICB9XG5cbiAgICBkaXNjb25uZWN0KGlkZW50aXR5KSB7XG4gICAgICAgIGRlbGV0ZSB0aGlzLmJvdW5kQ29tcG9uZW50c1tpZGVudGl0eV07XG4gICAgfVxuXG4gICAgb25NZXNzYWdlKHJlc3BvbnNlKSB7XG4gICAgICAgIGNvbnN0IGRhdGEgPSBKU09OLnBhcnNlKHJlc3BvbnNlLmRhdGEpO1xuICAgICAgICBjb25zdCB7aWRlbnRpdHksIGtpbmQsIHBheWxvYWQsIHN0b3JhZ2UsIHJlcXVlc3RfaWR9ID0gZGF0YTtcbiAgICAgICAgbGV0IHN0b3JlO1xuICAgICAgICBpZiAoc3RvcmFnZSA9PT0gJ3Nlc3Npb24nKSB7XG4gICAgICAgICAgICBzdG9yZSA9IHdpbmRvdy5zZXNzaW9uU3RvcmFnZTtcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgIHN0b3JlID0gd2luZG93LmxvY2FsU3RvcmFnZTtcbiAgICAgICAgfVxuICAgICAgICBzd2l0Y2ggKGtpbmQpIHtcbiAgICAgICAgICAgIGNhc2UgJ3NldC1hc3BlY3QnOlxuICAgICAgICAgICAgICAgIGNvbnN0IGNvbXBvbmVudCA9IHRoaXMuYm91bmRDb21wb25lbnRzW2lkZW50aXR5XTtcbiAgICAgICAgICAgICAgICBpZiAoIWNvbXBvbmVudCkge1xuICAgICAgICAgICAgICAgICAgICBjb25zdCBlcnJvciA9IGBDb21wb25lbnQgbm90IGZvdW5kOiAke2lkZW50aXR5fWA7XG4gICAgICAgICAgICAgICAgICAgIHRoaXMud3Muc2VuZChKU09OLnN0cmluZ2lmeSh7ZXJyb3IsIGtpbmQ6ICdlcnJvcid9KSk7XG4gICAgICAgICAgICAgICAgICAgIGNvbnNvbGUuZXJyb3IoZXJyb3IpO1xuICAgICAgICAgICAgICAgICAgICByZXR1cm47XG4gICAgICAgICAgICAgICAgfVxuXG4gICAgICAgICAgICAgICAgY29tcG9uZW50XG4gICAgICAgICAgICAgICAgICAgIC5zZXRBc3BlY3RzKFxuICAgICAgICAgICAgICAgICAgICAgICAgaHlkcmF0ZVByb3BzKFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIHBheWxvYWQsXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgdGhpcy51cGRhdGVBc3BlY3RzLFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIHRoaXMuY29ubmVjdCxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICB0aGlzLmRpc2Nvbm5lY3RcbiAgICAgICAgICAgICAgICAgICAgICAgIClcbiAgICAgICAgICAgICAgICAgICAgKVxuICAgICAgICAgICAgICAgICAgICAudGhlbigoKSA9PiB7XG4gICAgICAgICAgICAgICAgICAgICAgICBPYmplY3Qua2V5cyhwYXlsb2FkKS5mb3JFYWNoKGsgPT4ge1xuICAgICAgICAgICAgICAgICAgICAgICAgICAgIGNvbnN0IGtleSA9IGAke2lkZW50aXR5fS4ke2t9YDtcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICBjb25zdCBiaW5kaW5nID0gdGhpcy5zdGF0ZS5iaW5kaW5nc1trZXldO1xuICAgICAgICAgICAgICAgICAgICAgICAgICAgIGlmIChiaW5kaW5nKSB7XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHRoaXMuc2VuZEJpbmRpbmcoXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBiaW5kaW5nLFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgY29tcG9uZW50LmdldEFzcGVjdChrKVxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICApO1xuICAgICAgICAgICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAvLyBXaGF0IGFib3V0IHJldHVybmVkIGNvbXBvbmVudHMgP1xuICAgICAgICAgICAgICAgICAgICAgICAgICAgIC8vIFRoZXkgZ2V0IHRoZWlyIFdyYXBwZXIuXG4gICAgICAgICAgICAgICAgICAgICAgICB9KTtcbiAgICAgICAgICAgICAgICAgICAgfSk7XG4gICAgICAgICAgICAgICAgYnJlYWs7XG4gICAgICAgICAgICBjYXNlICdnZXQtYXNwZWN0JzpcbiAgICAgICAgICAgICAgICBjb25zdCB7YXNwZWN0fSA9IGRhdGE7XG4gICAgICAgICAgICAgICAgY29uc3Qgd2FudGVkID0gdGhpcy5ib3VuZENvbXBvbmVudHNbaWRlbnRpdHldO1xuICAgICAgICAgICAgICAgIGlmICghd2FudGVkKSB7XG4gICAgICAgICAgICAgICAgICAgIHRoaXMud3Muc2VuZChcbiAgICAgICAgICAgICAgICAgICAgICAgIEpTT04uc3RyaW5naWZ5KHtcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICBraW5kLFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIGlkZW50aXR5LFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIGFzcGVjdCxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICByZXF1ZXN0X2lkLFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIGVycm9yOiBgQXNwZWN0IG5vdCBmb3VuZCAke2lkZW50aXR5fS4ke2FzcGVjdH1gLFxuICAgICAgICAgICAgICAgICAgICAgICAgfSlcbiAgICAgICAgICAgICAgICAgICAgKTtcbiAgICAgICAgICAgICAgICAgICAgcmV0dXJuO1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICBjb25zdCB2YWx1ZSA9IHdhbnRlZC5nZXRBc3BlY3QoYXNwZWN0KTtcbiAgICAgICAgICAgICAgICB0aGlzLndzLnNlbmQoXG4gICAgICAgICAgICAgICAgICAgIEpTT04uc3RyaW5naWZ5KHtcbiAgICAgICAgICAgICAgICAgICAgICAgIGtpbmQsXG4gICAgICAgICAgICAgICAgICAgICAgICBpZGVudGl0eSxcbiAgICAgICAgICAgICAgICAgICAgICAgIGFzcGVjdCxcbiAgICAgICAgICAgICAgICAgICAgICAgIHZhbHVlOiBwcmVwYXJlUHJvcCh2YWx1ZSksXG4gICAgICAgICAgICAgICAgICAgICAgICByZXF1ZXN0X2lkLFxuICAgICAgICAgICAgICAgICAgICB9KVxuICAgICAgICAgICAgICAgICk7XG4gICAgICAgICAgICAgICAgYnJlYWs7XG4gICAgICAgICAgICBjYXNlICdzZXQtc3RvcmFnZSc6XG4gICAgICAgICAgICAgICAgc3RvcmUuc2V0SXRlbShpZGVudGl0eSwgSlNPTi5zdHJpbmdpZnkocGF5bG9hZCkpO1xuICAgICAgICAgICAgICAgIGJyZWFrO1xuICAgICAgICAgICAgY2FzZSAnZ2V0LXN0b3JhZ2UnOlxuICAgICAgICAgICAgICAgIHRoaXMud3Muc2VuZChcbiAgICAgICAgICAgICAgICAgICAgSlNPTi5zdHJpbmdpZnkoe1xuICAgICAgICAgICAgICAgICAgICAgICAga2luZCxcbiAgICAgICAgICAgICAgICAgICAgICAgIGlkZW50aXR5LFxuICAgICAgICAgICAgICAgICAgICAgICAgcmVxdWVzdF9pZCxcbiAgICAgICAgICAgICAgICAgICAgICAgIHZhbHVlOiBKU09OLnBhcnNlKHN0b3JlLmdldEl0ZW0oaWRlbnRpdHkpKSxcbiAgICAgICAgICAgICAgICAgICAgfSlcbiAgICAgICAgICAgICAgICApO1xuICAgICAgICAgICAgICAgIGJyZWFrO1xuICAgICAgICAgICAgY2FzZSAncmVsb2FkJzpcbiAgICAgICAgICAgICAgICBjb25zdCB7ZmlsZW5hbWVzLCBob3QsIHJlZnJlc2gsIGRlbGV0ZWR9ID0gZGF0YTtcbiAgICAgICAgICAgICAgICBpZiAocmVmcmVzaCkge1xuICAgICAgICAgICAgICAgICAgICB0aGlzLndzLmNsb3NlKCk7XG4gICAgICAgICAgICAgICAgICAgIHJldHVybiB0aGlzLnNldFN0YXRlKHtyZWxvYWRpbmc6IHRydWUsIG5lZWRSZWZyZXNoOiB0cnVlfSk7XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIGlmIChob3QpIHtcbiAgICAgICAgICAgICAgICAgICAgLy8gVGhlIHdzIGNvbm5lY3Rpb24gd2lsbCBjbG9zZSwgd2hlbiBpdFxuICAgICAgICAgICAgICAgICAgICAvLyByZWNvbm5lY3QgaXQgd2lsbCBkbyBhIGhhcmQgcmVsb2FkIG9mIHRoZSBwYWdlIGFwaS5cbiAgICAgICAgICAgICAgICAgICAgcmV0dXJuIHRoaXMuc2V0U3RhdGUoe3JlbG9hZGluZzogdHJ1ZX0pO1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICBmaWxlbmFtZXMuZm9yRWFjaChsb2FkUmVxdWlyZW1lbnQpO1xuICAgICAgICAgICAgICAgIGRlbGV0ZWQuZm9yRWFjaChyID0+IGRpc2FibGVDc3Moci51cmwpKTtcbiAgICAgICAgICAgICAgICBicmVhaztcbiAgICAgICAgICAgIGNhc2UgJ3BpbmcnOlxuICAgICAgICAgICAgICAgIC8vIEp1c3QgZG8gbm90aGluZy5cbiAgICAgICAgICAgICAgICBicmVhaztcbiAgICAgICAgfVxuICAgIH1cblxuICAgIHNlbmRCaW5kaW5nKGJpbmRpbmcsIHZhbHVlKSB7XG4gICAgICAgIC8vIENvbGxlY3QgYWxsIHZhbHVlcyBhbmQgc2VuZCBhIGJpbmRpbmcgcGF5bG9hZFxuICAgICAgICBjb25zdCB0cmlnZ2VyID0ge1xuICAgICAgICAgICAgLi4uYmluZGluZy50cmlnZ2VyLFxuICAgICAgICAgICAgdmFsdWU6IHByZXBhcmVQcm9wKHZhbHVlKSxcbiAgICAgICAgfTtcbiAgICAgICAgY29uc3Qgc3RhdGVzID0gYmluZGluZy5zdGF0ZXMubWFwKHN0YXRlID0+ICh7XG4gICAgICAgICAgICAuLi5zdGF0ZSxcbiAgICAgICAgICAgIHZhbHVlOlxuICAgICAgICAgICAgICAgIHRoaXMuYm91bmRDb21wb25lbnRzW3N0YXRlLmlkZW50aXR5XSAmJlxuICAgICAgICAgICAgICAgIHByZXBhcmVQcm9wKFxuICAgICAgICAgICAgICAgICAgICB0aGlzLmJvdW5kQ29tcG9uZW50c1tzdGF0ZS5pZGVudGl0eV0uZ2V0QXNwZWN0KHN0YXRlLmFzcGVjdClcbiAgICAgICAgICAgICAgICApLFxuICAgICAgICB9KSk7XG5cbiAgICAgICAgY29uc3QgcGF5bG9hZCA9IHtcbiAgICAgICAgICAgIHRyaWdnZXIsXG4gICAgICAgICAgICBzdGF0ZXMsXG4gICAgICAgICAgICBraW5kOiAnYmluZGluZycsXG4gICAgICAgICAgICBwYWdlOiB0aGlzLnN0YXRlLnBhZ2UsXG4gICAgICAgICAgICBrZXk6IGJpbmRpbmcua2V5LFxuICAgICAgICB9O1xuICAgICAgICB0aGlzLndzLnNlbmQoSlNPTi5zdHJpbmdpZnkocGF5bG9hZCkpO1xuICAgIH1cblxuICAgIF9jb25uZWN0V1MoKSB7XG4gICAgICAgIC8vIFNldHVwIHdlYnNvY2tldCBmb3IgdXBkYXRlc1xuICAgICAgICBsZXQgdHJpZXMgPSAwO1xuICAgICAgICBsZXQgaGFyZENsb3NlID0gZmFsc2U7XG4gICAgICAgIGNvbnN0IGNvbm5leGlvbiA9ICgpID0+IHtcbiAgICAgICAgICAgIHRoaXMud3MgPSBuZXcgV2ViU29ja2V0KFxuICAgICAgICAgICAgICAgIGB3cyR7XG4gICAgICAgICAgICAgICAgICAgIHdpbmRvdy5sb2NhdGlvbi5ocmVmLnN0YXJ0c1dpdGgoJ2h0dHBzJykgPyAncycgOiAnJ1xuICAgICAgICAgICAgICAgIH06Ly8keyh0aGlzLnByb3BzLmJhc2VVcmwgJiYgdGhpcy5wcm9wcy5iYXNlVXJsKSB8fFxuICAgICAgICAgICAgICAgICAgICB3aW5kb3cubG9jYXRpb24uaG9zdH0ke3dpbmRvdy5sb2NhdGlvbi5wYXRobmFtZX0vd3NgXG4gICAgICAgICAgICApO1xuICAgICAgICAgICAgdGhpcy53cy5hZGRFdmVudExpc3RlbmVyKCdtZXNzYWdlJywgdGhpcy5vbk1lc3NhZ2UpO1xuICAgICAgICAgICAgdGhpcy53cy5vbm9wZW4gPSAoKSA9PiB7XG4gICAgICAgICAgICAgICAgaWYgKHRoaXMuc3RhdGUucmVsb2FkaW5nKSB7XG4gICAgICAgICAgICAgICAgICAgIGhhcmRDbG9zZSA9IHRydWU7XG4gICAgICAgICAgICAgICAgICAgIHRoaXMud3MuY2xvc2UoKTtcbiAgICAgICAgICAgICAgICAgICAgaWYgKHRoaXMuc3RhdGUubmVlZFJlZnJlc2gpIHtcbiAgICAgICAgICAgICAgICAgICAgICAgIHdpbmRvdy5sb2NhdGlvbi5yZWxvYWQoKTtcbiAgICAgICAgICAgICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgICAgICAgICAgICAgIHRoaXMucHJvcHMuaG90UmVsb2FkKCk7XG4gICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgICAgICAgICB0aGlzLnNldFN0YXRlKHtyZWFkeTogdHJ1ZX0pO1xuICAgICAgICAgICAgICAgICAgICB0cmllcyA9IDA7XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgfTtcbiAgICAgICAgICAgIHRoaXMud3Mub25jbG9zZSA9ICgpID0+IHtcbiAgICAgICAgICAgICAgICBjb25zdCByZWNvbm5lY3QgPSAoKSA9PiB7XG4gICAgICAgICAgICAgICAgICAgIHRyaWVzKys7XG4gICAgICAgICAgICAgICAgICAgIGNvbm5leGlvbigpO1xuICAgICAgICAgICAgICAgIH07XG4gICAgICAgICAgICAgICAgaWYgKCFoYXJkQ2xvc2UgJiYgdHJpZXMgPCB0aGlzLnByb3BzLnJldHJpZXMpIHtcbiAgICAgICAgICAgICAgICAgICAgc2V0VGltZW91dChyZWNvbm5lY3QsIDEwMDApO1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgIH07XG4gICAgICAgIH07XG4gICAgICAgIGNvbm5leGlvbigpO1xuICAgIH1cblxuICAgIGNvbXBvbmVudFdpbGxNb3VudCgpIHtcbiAgICAgICAgdGhpcy5wYWdlQXBpKCcnLCB7bWV0aG9kOiAnUE9TVCd9KS50aGVuKHJlc3BvbnNlID0+IHtcbiAgICAgICAgICAgIHRoaXMuc2V0U3RhdGUoe1xuICAgICAgICAgICAgICAgIHBhZ2U6IHJlc3BvbnNlLnBhZ2UsXG4gICAgICAgICAgICAgICAgbGF5b3V0OiByZXNwb25zZS5sYXlvdXQsXG4gICAgICAgICAgICAgICAgYmluZGluZ3M6IHJlc3BvbnNlLmJpbmRpbmdzLFxuICAgICAgICAgICAgICAgIHBhY2thZ2VzOiByZXNwb25zZS5wYWNrYWdlcyxcbiAgICAgICAgICAgICAgICByZXF1aXJlbWVudHM6IHJlc3BvbnNlLnJlcXVpcmVtZW50cyxcbiAgICAgICAgICAgIH0pO1xuICAgICAgICAgICAgbG9hZFJlcXVpcmVtZW50cyhyZXNwb25zZS5yZXF1aXJlbWVudHMsIHJlc3BvbnNlLnBhY2thZ2VzKS50aGVuKFxuICAgICAgICAgICAgICAgICgpID0+IHtcbiAgICAgICAgICAgICAgICAgICAgaWYgKFxuICAgICAgICAgICAgICAgICAgICAgICAgT2JqZWN0LmtleXMocmVzcG9uc2UuYmluZGluZ3MpLmxlbmd0aCB8fFxuICAgICAgICAgICAgICAgICAgICAgICAgcmVzcG9uc2UucmVsb2FkXG4gICAgICAgICAgICAgICAgICAgICkge1xuICAgICAgICAgICAgICAgICAgICAgICAgdGhpcy5fY29ubmVjdFdTKCk7XG4gICAgICAgICAgICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAgICAgICAgICAgICB0aGlzLnNldFN0YXRlKHtyZWFkeTogdHJ1ZX0pO1xuICAgICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgKTtcbiAgICAgICAgfSk7XG4gICAgfVxuXG4gICAgcmVuZGVyKCkge1xuICAgICAgICBjb25zdCB7bGF5b3V0LCByZWFkeSwgcmVsb2FkaW5nfSA9IHRoaXMuc3RhdGU7XG4gICAgICAgIGlmICghcmVhZHkpIHtcbiAgICAgICAgICAgIHJldHVybiA8ZGl2IGNsYXNzTmFtZT1cImRhenpsZXItbG9hZGluZ1wiPkxvYWRpbmcuLi48L2Rpdj47XG4gICAgICAgIH1cbiAgICAgICAgaWYgKHJlbG9hZGluZykge1xuICAgICAgICAgICAgcmV0dXJuIDxkaXYgY2xhc3NOYW1lPVwiZGF6emxlci1sb2FkaW5nXCI+UmVsb2FkaW5nLi4uPC9kaXY+O1xuICAgICAgICB9XG4gICAgICAgIGlmICghaXNDb21wb25lbnQobGF5b3V0KSkge1xuICAgICAgICAgICAgdGhyb3cgbmV3IEVycm9yKGBMYXlvdXQgaXMgbm90IGEgY29tcG9uZW50OiAke2xheW91dH1gKTtcbiAgICAgICAgfVxuXG4gICAgICAgIHJldHVybiAoXG4gICAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImRhenpsZXItcmVuZGVyZWRcIj5cbiAgICAgICAgICAgICAgICB7aHlkcmF0ZUNvbXBvbmVudChcbiAgICAgICAgICAgICAgICAgICAgbGF5b3V0Lm5hbWUsXG4gICAgICAgICAgICAgICAgICAgIGxheW91dC5wYWNrYWdlLFxuICAgICAgICAgICAgICAgICAgICBsYXlvdXQuaWRlbnRpdHksXG4gICAgICAgICAgICAgICAgICAgIGh5ZHJhdGVQcm9wcyhcbiAgICAgICAgICAgICAgICAgICAgICAgIGxheW91dC5hc3BlY3RzLFxuICAgICAgICAgICAgICAgICAgICAgICAgdGhpcy51cGRhdGVBc3BlY3RzLFxuICAgICAgICAgICAgICAgICAgICAgICAgdGhpcy5jb25uZWN0LFxuICAgICAgICAgICAgICAgICAgICAgICAgdGhpcy5kaXNjb25uZWN0XG4gICAgICAgICAgICAgICAgICAgICksXG4gICAgICAgICAgICAgICAgICAgIHRoaXMudXBkYXRlQXNwZWN0cyxcbiAgICAgICAgICAgICAgICAgICAgdGhpcy5jb25uZWN0LFxuICAgICAgICAgICAgICAgICAgICB0aGlzLmRpc2Nvbm5lY3RcbiAgICAgICAgICAgICAgICApfVxuICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICk7XG4gICAgfVxufVxuXG5VcGRhdGVyLmRlZmF1bHRQcm9wcyA9IHt9O1xuXG5VcGRhdGVyLnByb3BUeXBlcyA9IHtcbiAgICBiYXNlVXJsOiBQcm9wVHlwZXMuc3RyaW5nLmlzUmVxdWlyZWQsXG4gICAgcGluZzogUHJvcFR5cGVzLmJvb2wsXG4gICAgcGluZ19pbnRlcnZhbDogUHJvcFR5cGVzLm51bWJlcixcbiAgICByZXRyaWVzOiBQcm9wVHlwZXMubnVtYmVyLFxuICAgIGhvdFJlbG9hZDogUHJvcFR5cGVzLmZ1bmMsXG59O1xuIiwiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcbmltcG9ydCBQcm9wVHlwZXMgZnJvbSAncHJvcC10eXBlcyc7XG5pbXBvcnQge2NvbmNhdCwgam9pbn0gZnJvbSAncmFtZGEnO1xuaW1wb3J0IHtjYW1lbFRvU3BpbmFsfSBmcm9tICcuLi8uLi8uLi9jb21tb25zL2pzJztcblxuLyoqXG4gKiBXcmFwcyBjb21wb25lbnRzIGZvciBhc3BlY3RzIHVwZGF0aW5nLlxuICovXG5leHBvcnQgZGVmYXVsdCBjbGFzcyBXcmFwcGVyIGV4dGVuZHMgUmVhY3QuQ29tcG9uZW50IHtcbiAgICBjb25zdHJ1Y3Rvcihwcm9wcykge1xuICAgICAgICBzdXBlcihwcm9wcyk7XG4gICAgICAgIHRoaXMuc3RhdGUgPSB7XG4gICAgICAgICAgICBhc3BlY3RzOiBwcm9wcy5hc3BlY3RzIHx8IHt9LFxuICAgICAgICAgICAgcmVhZHk6IGZhbHNlLFxuICAgICAgICAgICAgaW5pdGlhbDogZmFsc2UsXG4gICAgICAgIH07XG4gICAgICAgIHRoaXMuc2V0QXNwZWN0cyA9IHRoaXMuc2V0QXNwZWN0cy5iaW5kKHRoaXMpO1xuICAgICAgICB0aGlzLmdldEFzcGVjdCA9IHRoaXMuZ2V0QXNwZWN0LmJpbmQodGhpcyk7XG4gICAgICAgIHRoaXMudXBkYXRlQXNwZWN0cyA9IHRoaXMudXBkYXRlQXNwZWN0cy5iaW5kKHRoaXMpO1xuICAgIH1cblxuICAgIHVwZGF0ZUFzcGVjdHMoYXNwZWN0cykge1xuICAgICAgICByZXR1cm4gdGhpcy5zZXRBc3BlY3RzKGFzcGVjdHMpLnRoZW4oKCkgPT5cbiAgICAgICAgICAgIHRoaXMucHJvcHMudXBkYXRlQXNwZWN0cyh0aGlzLnByb3BzLmlkZW50aXR5LCBhc3BlY3RzKVxuICAgICAgICApO1xuICAgIH1cblxuICAgIHNldEFzcGVjdHMoYXNwZWN0cykge1xuICAgICAgICByZXR1cm4gbmV3IFByb21pc2UocmVzb2x2ZSA9PiB7XG4gICAgICAgICAgICB0aGlzLnNldFN0YXRlKFxuICAgICAgICAgICAgICAgIHthc3BlY3RzOiB7Li4udGhpcy5zdGF0ZS5hc3BlY3RzLCAuLi5hc3BlY3RzfX0sXG4gICAgICAgICAgICAgICAgcmVzb2x2ZVxuICAgICAgICAgICAgKTtcbiAgICAgICAgfSk7XG4gICAgfVxuXG4gICAgZ2V0QXNwZWN0KGFzcGVjdCkge1xuICAgICAgICByZXR1cm4gdGhpcy5zdGF0ZS5hc3BlY3RzW2FzcGVjdF07XG4gICAgfVxuXG4gICAgY29tcG9uZW50RGlkTW91bnQoKSB7XG4gICAgICAgIC8vIE9ubHkgdXBkYXRlIHRoZSBjb21wb25lbnQgd2hlbiBtb3VudGVkLlxuICAgICAgICAvLyBPdGhlcndpc2UgZ2V0cyBhIHJhY2UgY29uZGl0aW9uIHdpdGggd2lsbFVubW91bnRcbiAgICAgICAgdGhpcy5wcm9wcy5jb25uZWN0KFxuICAgICAgICAgICAgdGhpcy5wcm9wcy5pZGVudGl0eSxcbiAgICAgICAgICAgIHRoaXMuc2V0QXNwZWN0cyxcbiAgICAgICAgICAgIHRoaXMuZ2V0QXNwZWN0XG4gICAgICAgICk7XG4gICAgICAgIGlmICghdGhpcy5zdGF0ZS5pbml0aWFsKSB7XG4gICAgICAgICAgICB0aGlzLnVwZGF0ZUFzcGVjdHModGhpcy5zdGF0ZS5hc3BlY3RzKS50aGVuKCgpID0+XG4gICAgICAgICAgICAgICAgdGhpcy5zZXRTdGF0ZSh7cmVhZHk6IHRydWUsIGluaXRpYWw6IHRydWV9KVxuICAgICAgICAgICAgKTtcbiAgICAgICAgfVxuICAgIH1cblxuICAgIGNvbXBvbmVudFdpbGxVbm1vdW50KCkge1xuICAgICAgICB0aGlzLnByb3BzLmRpc2Nvbm5lY3QodGhpcy5wcm9wcy5pZGVudGl0eSk7XG4gICAgfVxuXG4gICAgcmVuZGVyKCkge1xuICAgICAgICBjb25zdCB7Y29tcG9uZW50LCBjb21wb25lbnRfbmFtZSwgcGFja2FnZV9uYW1lfSA9IHRoaXMucHJvcHM7XG4gICAgICAgIGNvbnN0IHthc3BlY3RzLCByZWFkeX0gPSB0aGlzLnN0YXRlO1xuICAgICAgICBpZiAoIXJlYWR5KSByZXR1cm4gbnVsbDtcblxuICAgICAgICByZXR1cm4gUmVhY3QuY2xvbmVFbGVtZW50KGNvbXBvbmVudCwge1xuICAgICAgICAgICAgLi4uYXNwZWN0cyxcbiAgICAgICAgICAgIHVwZGF0ZUFzcGVjdHM6IHRoaXMudXBkYXRlQXNwZWN0cyxcbiAgICAgICAgICAgIGlkZW50aXR5OiB0aGlzLnByb3BzLmlkZW50aXR5LFxuICAgICAgICAgICAgY2xhc3NfbmFtZTogam9pbihcbiAgICAgICAgICAgICAgICAnICcsXG4gICAgICAgICAgICAgICAgY29uY2F0KFxuICAgICAgICAgICAgICAgICAgICBbXG4gICAgICAgICAgICAgICAgICAgICAgICBgJHtwYWNrYWdlX25hbWVcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAucmVwbGFjZSgnXycsICctJylcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAudG9Mb3dlckNhc2UoKX0tJHtjYW1lbFRvU3BpbmFsKGNvbXBvbmVudF9uYW1lKX1gLFxuICAgICAgICAgICAgICAgICAgICBdLFxuICAgICAgICAgICAgICAgICAgICBhc3BlY3RzLmNsYXNzX25hbWUgPyBhc3BlY3RzLmNsYXNzX25hbWUuc3BsaXQoJyAnKSA6IFtdXG4gICAgICAgICAgICAgICAgKVxuICAgICAgICAgICAgKSxcbiAgICAgICAgfSk7XG4gICAgfVxufVxuXG5XcmFwcGVyLnByb3BUeXBlcyA9IHtcbiAgICBpZGVudGl0eTogUHJvcFR5cGVzLnN0cmluZy5pc1JlcXVpcmVkLFxuICAgIHVwZGF0ZUFzcGVjdHM6IFByb3BUeXBlcy5mdW5jLmlzUmVxdWlyZWQsXG4gICAgY29tcG9uZW50OiBQcm9wVHlwZXMubm9kZS5pc1JlcXVpcmVkLFxuICAgIGNvbm5lY3Q6IFByb3BUeXBlcy5mdW5jLmlzUmVxdWlyZWQsXG4gICAgY29tcG9uZW50X25hbWU6IFByb3BUeXBlcy5zdHJpbmcuaXNSZXF1aXJlZCxcbiAgICBwYWNrYWdlX25hbWU6IFByb3BUeXBlcy5zdHJpbmcuaXNSZXF1aXJlZCxcbiAgICBkaXNjb25uZWN0OiBQcm9wVHlwZXMuZnVuYy5pc1JlcXVpcmVkLFxufTtcbiIsImltcG9ydCB7bWFwLCBvbWl0LCB0eXBlfSBmcm9tICdyYW1kYSc7XG5pbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IFdyYXBwZXIgZnJvbSAnLi9jb21wb25lbnRzL1dyYXBwZXInO1xuXG5leHBvcnQgZnVuY3Rpb24gaXNDb21wb25lbnQoYykge1xuICAgIHJldHVybiAoXG4gICAgICAgIHR5cGUoYykgPT09ICdPYmplY3QnICYmXG4gICAgICAgIChjLmhhc093blByb3BlcnR5KCdwYWNrYWdlJykgJiZcbiAgICAgICAgICAgIGMuaGFzT3duUHJvcGVydHkoJ2FzcGVjdHMnKSAmJlxuICAgICAgICAgICAgYy5oYXNPd25Qcm9wZXJ0eSgnbmFtZScpICYmXG4gICAgICAgICAgICBjLmhhc093blByb3BlcnR5KCdpZGVudGl0eScpKVxuICAgICk7XG59XG5cbmV4cG9ydCBmdW5jdGlvbiBoeWRyYXRlUHJvcHMocHJvcHMsIHVwZGF0ZUFzcGVjdHMsIGNvbm5lY3QsIGRpc2Nvbm5lY3QpIHtcbiAgICBjb25zdCByZXBsYWNlID0ge307XG4gICAgT2JqZWN0LmVudHJpZXMocHJvcHMpLmZvckVhY2goKFtrLCB2XSkgPT4ge1xuICAgICAgICBpZiAodHlwZSh2KSA9PT0gJ0FycmF5Jykge1xuICAgICAgICAgICAgcmVwbGFjZVtrXSA9IHYubWFwKGMgPT4ge1xuICAgICAgICAgICAgICAgIGlmICghaXNDb21wb25lbnQoYykpIHtcbiAgICAgICAgICAgICAgICAgICAgLy8gTWl4aW5nIGNvbXBvbmVudHMgYW5kIHByaW1pdGl2ZXNcbiAgICAgICAgICAgICAgICAgICAgcmV0dXJuIGM7XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIGNvbnN0IG5ld1Byb3BzID0gaHlkcmF0ZVByb3BzKFxuICAgICAgICAgICAgICAgICAgICBjLmFzcGVjdHMsXG4gICAgICAgICAgICAgICAgICAgIHVwZGF0ZUFzcGVjdHMsXG4gICAgICAgICAgICAgICAgICAgIGNvbm5lY3QsXG4gICAgICAgICAgICAgICAgICAgIGRpc2Nvbm5lY3RcbiAgICAgICAgICAgICAgICApO1xuICAgICAgICAgICAgICAgIGlmICghbmV3UHJvcHMua2V5KSB7XG4gICAgICAgICAgICAgICAgICAgIG5ld1Byb3BzLmtleSA9IGMuaWRlbnRpdHk7XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIHJldHVybiBoeWRyYXRlQ29tcG9uZW50KFxuICAgICAgICAgICAgICAgICAgICBjLm5hbWUsXG4gICAgICAgICAgICAgICAgICAgIGMucGFja2FnZSxcbiAgICAgICAgICAgICAgICAgICAgYy5pZGVudGl0eSxcbiAgICAgICAgICAgICAgICAgICAgbmV3UHJvcHMsXG4gICAgICAgICAgICAgICAgICAgIHVwZGF0ZUFzcGVjdHMsXG4gICAgICAgICAgICAgICAgICAgIGNvbm5lY3QsXG4gICAgICAgICAgICAgICAgICAgIGRpc2Nvbm5lY3RcbiAgICAgICAgICAgICAgICApO1xuICAgICAgICAgICAgfSk7XG4gICAgICAgIH0gZWxzZSBpZiAoaXNDb21wb25lbnQodikpIHtcbiAgICAgICAgICAgIGNvbnN0IG5ld1Byb3BzID0gaHlkcmF0ZVByb3BzKFxuICAgICAgICAgICAgICAgIHYuYXNwZWN0cyxcbiAgICAgICAgICAgICAgICB1cGRhdGVBc3BlY3RzLFxuICAgICAgICAgICAgICAgIGNvbm5lY3QsXG4gICAgICAgICAgICAgICAgZGlzY29ubmVjdFxuICAgICAgICAgICAgKTtcbiAgICAgICAgICAgIHJlcGxhY2Vba10gPSBoeWRyYXRlQ29tcG9uZW50KFxuICAgICAgICAgICAgICAgIHYubmFtZSxcbiAgICAgICAgICAgICAgICB2LnBhY2thZ2UsXG4gICAgICAgICAgICAgICAgdi5pZGVudGl0eSxcbiAgICAgICAgICAgICAgICBuZXdQcm9wcyxcbiAgICAgICAgICAgICAgICB1cGRhdGVBc3BlY3RzLFxuICAgICAgICAgICAgICAgIGNvbm5lY3QsXG4gICAgICAgICAgICAgICAgZGlzY29ubmVjdFxuICAgICAgICAgICAgKTtcbiAgICAgICAgfSBlbHNlIGlmICh0eXBlKHYpID09PSAnT2JqZWN0Jykge1xuICAgICAgICAgICAgcmVwbGFjZVtrXSA9IGh5ZHJhdGVQcm9wcyh2LCB1cGRhdGVBc3BlY3RzLCBjb25uZWN0LCBkaXNjb25uZWN0KTtcbiAgICAgICAgfVxuICAgIH0pO1xuICAgIHJldHVybiB7Li4ucHJvcHMsIC4uLnJlcGxhY2V9O1xufVxuXG5leHBvcnQgZnVuY3Rpb24gaHlkcmF0ZUNvbXBvbmVudChcbiAgICBuYW1lLFxuICAgIHBhY2thZ2VfbmFtZSxcbiAgICBpZGVudGl0eSxcbiAgICBwcm9wcyxcbiAgICB1cGRhdGVBc3BlY3RzLFxuICAgIGNvbm5lY3QsXG4gICAgZGlzY29ubmVjdFxuKSB7XG4gICAgY29uc3QgcGFjayA9IHdpbmRvd1twYWNrYWdlX25hbWVdO1xuICAgIGNvbnN0IGVsZW1lbnQgPSBSZWFjdC5jcmVhdGVFbGVtZW50KHBhY2tbbmFtZV0sIHByb3BzKTtcbiAgICByZXR1cm4gKFxuICAgICAgICA8V3JhcHBlclxuICAgICAgICAgICAgaWRlbnRpdHk9e2lkZW50aXR5fVxuICAgICAgICAgICAgdXBkYXRlQXNwZWN0cz17dXBkYXRlQXNwZWN0c31cbiAgICAgICAgICAgIGNvbXBvbmVudD17ZWxlbWVudH1cbiAgICAgICAgICAgIGNvbm5lY3Q9e2Nvbm5lY3R9XG4gICAgICAgICAgICBwYWNrYWdlX25hbWU9e3BhY2thZ2VfbmFtZX1cbiAgICAgICAgICAgIGNvbXBvbmVudF9uYW1lPXtuYW1lfVxuICAgICAgICAgICAgYXNwZWN0cz17cHJvcHN9XG4gICAgICAgICAgICBkaXNjb25uZWN0PXtkaXNjb25uZWN0fVxuICAgICAgICAgICAga2V5PXtgd3JhcHBlci0ke2lkZW50aXR5fWB9XG4gICAgICAgIC8+XG4gICAgKTtcbn1cblxuZXhwb3J0IGZ1bmN0aW9uIHByZXBhcmVQcm9wKHByb3ApIHtcbiAgICBpZiAoUmVhY3QuaXNWYWxpZEVsZW1lbnQocHJvcCkpIHtcbiAgICAgICAgcmV0dXJuIHtcbiAgICAgICAgICAgIGlkZW50aXR5OiBwcm9wLnByb3BzLmlkZW50aXR5LFxuICAgICAgICAgICAgYXNwZWN0czogbWFwKFxuICAgICAgICAgICAgICAgIHByZXBhcmVQcm9wLFxuICAgICAgICAgICAgICAgIG9taXQoXG4gICAgICAgICAgICAgICAgICAgIFtcbiAgICAgICAgICAgICAgICAgICAgICAgICdpZGVudGl0eScsXG4gICAgICAgICAgICAgICAgICAgICAgICAndXBkYXRlQXNwZWN0cycsXG4gICAgICAgICAgICAgICAgICAgICAgICAnX25hbWUnLFxuICAgICAgICAgICAgICAgICAgICAgICAgJ19wYWNrYWdlJyxcbiAgICAgICAgICAgICAgICAgICAgICAgICdhc3BlY3RzJyxcbiAgICAgICAgICAgICAgICAgICAgICAgICdrZXknLFxuICAgICAgICAgICAgICAgICAgICBdLFxuICAgICAgICAgICAgICAgICAgICBwcm9wLnByb3BzLmFzcGVjdHNcbiAgICAgICAgICAgICAgICApXG4gICAgICAgICAgICApLFxuICAgICAgICAgICAgbmFtZTogcHJvcC5wcm9wcy5jb21wb25lbnRfbmFtZSxcbiAgICAgICAgICAgIHBhY2thZ2U6IHByb3AucHJvcHMucGFja2FnZV9uYW1lLFxuICAgICAgICB9O1xuICAgIH1cbiAgICBpZiAodHlwZShwcm9wKSA9PT0gJ0FycmF5Jykge1xuICAgICAgICByZXR1cm4gcHJvcC5tYXAocHJlcGFyZVByb3ApO1xuICAgIH1cbiAgICBpZiAodHlwZShwcm9wKSA9PT0gJ09iamVjdCcpIHtcbiAgICAgICAgcmV0dXJuIG1hcChwcmVwYXJlUHJvcCwgcHJvcCk7XG4gICAgfVxuICAgIHJldHVybiBwcm9wO1xufVxuIiwiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcbmltcG9ydCBSZWFjdERPTSBmcm9tICdyZWFjdC1kb20nO1xuaW1wb3J0IFJlbmRlcmVyIGZyb20gJy4vY29tcG9uZW50cy9SZW5kZXJlcic7XG5cbmZ1bmN0aW9uIHJlbmRlcih7YmFzZVVybCwgcGluZywgcGluZ19pbnRlcnZhbCwgcmV0cmllc30sIGVsZW1lbnQpIHtcbiAgICBSZWFjdERPTS5yZW5kZXIoXG4gICAgICAgIDxSZW5kZXJlclxuICAgICAgICAgICAgYmFzZVVybD17YmFzZVVybH1cbiAgICAgICAgICAgIHBpbmc9e3Bpbmd9XG4gICAgICAgICAgICBwaW5nX2ludGVydmFsPXtwaW5nX2ludGVydmFsfVxuICAgICAgICAgICAgcmV0cmllcz17cmV0cmllc31cbiAgICAgICAgLz4sXG4gICAgICAgIGVsZW1lbnRcbiAgICApO1xufVxuXG5leHBvcnQge1JlbmRlcmVyLCByZW5kZXJ9O1xuIiwiLyogZXNsaW50LWRpc2FibGUgbm8tbWFnaWMtbnVtYmVycyAqL1xuXG5jb25zdCBqc29uUGF0dGVybiA9IC9qc29uL2k7XG5cbi8qKlxuICogQHR5cGVkZWYge09iamVjdH0gWGhyT3B0aW9uc1xuICogQHByb3BlcnR5IHtzdHJpbmd9IFttZXRob2Q9J0dFVCddXG4gKiBAcHJvcGVydHkge09iamVjdH0gW2hlYWRlcnM9e31dXG4gKiBAcHJvcGVydHkge3N0cmluZ3xCbG9ifEFycmF5QnVmZmVyfG9iamVjdHxBcnJheX0gW3BheWxvYWQ9JyddXG4gKi9cblxuLyoqXG4gKiBAdHlwZSB7WGhyT3B0aW9uc31cbiAqL1xuY29uc3QgZGVmYXVsdFhock9wdGlvbnMgPSB7XG4gICAgbWV0aG9kOiAnR0VUJyxcbiAgICBoZWFkZXJzOiB7fSxcbiAgICBwYXlsb2FkOiAnJyxcbiAgICBqc29uOiB0cnVlLFxufTtcblxuZXhwb3J0IGNvbnN0IEpTT05IRUFERVJTID0ge1xuICAgICdDb250ZW50LVR5cGUnOiAnYXBwbGljYXRpb24vanNvbicsXG59O1xuXG4vKipcbiAqIFhociBwcm9taXNlIHdyYXAuXG4gKlxuICogRmV0Y2ggY2FuJ3QgZG8gcHV0IHJlcXVlc3QsIHNvIHhociBzdGlsbCB1c2VmdWwuXG4gKlxuICogQXV0byBwYXJzZSBqc29uIHJlc3BvbnNlcy5cbiAqIENhbmNlbGxhdGlvbjogeGhyLmFib3J0XG4gKiBAcGFyYW0ge3N0cmluZ30gdXJsXG4gKiBAcGFyYW0ge1hock9wdGlvbnN9IFtvcHRpb25zXVxuICogQHJldHVybiB7UHJvbWlzZX1cbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIHhoclJlcXVlc3QodXJsLCBvcHRpb25zID0gZGVmYXVsdFhock9wdGlvbnMpIHtcbiAgICByZXR1cm4gbmV3IFByb21pc2UoKHJlc29sdmUsIHJlamVjdCkgPT4ge1xuICAgICAgICBjb25zdCB7bWV0aG9kLCBoZWFkZXJzLCBwYXlsb2FkLCBqc29ufSA9IHtcbiAgICAgICAgICAgIC4uLmRlZmF1bHRYaHJPcHRpb25zLFxuICAgICAgICAgICAgLi4ub3B0aW9ucyxcbiAgICAgICAgfTtcbiAgICAgICAgY29uc3QgeGhyID0gbmV3IFhNTEh0dHBSZXF1ZXN0KCk7XG4gICAgICAgIHhoci5vcGVuKG1ldGhvZCwgdXJsKTtcbiAgICAgICAgY29uc3QgaGVhZCA9IGpzb24gPyB7Li4uSlNPTkhFQURFUlMsIC4uLmhlYWRlcnN9IDogaGVhZGVycztcbiAgICAgICAgT2JqZWN0LmtleXMoaGVhZCkuZm9yRWFjaChrID0+IHhoci5zZXRSZXF1ZXN0SGVhZGVyKGssIGhlYWRba10pKTtcbiAgICAgICAgeGhyLm9ucmVhZHlzdGF0ZWNoYW5nZSA9ICgpID0+IHtcbiAgICAgICAgICAgIGlmICh4aHIucmVhZHlTdGF0ZSA9PT0gWE1MSHR0cFJlcXVlc3QuRE9ORSkge1xuICAgICAgICAgICAgICAgIGlmICh4aHIuc3RhdHVzIDwgNDAwKSB7XG4gICAgICAgICAgICAgICAgICAgIGxldCByZXNwb25zZVZhbHVlID0geGhyLnJlc3BvbnNlO1xuICAgICAgICAgICAgICAgICAgICBpZiAoXG4gICAgICAgICAgICAgICAgICAgICAgICBqc29uUGF0dGVybi50ZXN0KHhoci5nZXRSZXNwb25zZUhlYWRlcignQ29udGVudC1UeXBlJykpXG4gICAgICAgICAgICAgICAgICAgICkge1xuICAgICAgICAgICAgICAgICAgICAgICAgcmVzcG9uc2VWYWx1ZSA9IEpTT04ucGFyc2UoeGhyLnJlc3BvbnNlVGV4dCk7XG4gICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICAgICAgcmVzb2x2ZShyZXNwb25zZVZhbHVlKTtcbiAgICAgICAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgICAgICAgICByZWplY3Qoe1xuICAgICAgICAgICAgICAgICAgICAgICAgZXJyb3I6ICdSZXF1ZXN0RXJyb3InLFxuICAgICAgICAgICAgICAgICAgICAgICAgbWVzc2FnZTogYFhIUiAke3VybH0gRkFJTEVEIC0gU1RBVFVTOiAke1xuICAgICAgICAgICAgICAgICAgICAgICAgICAgIHhoci5zdGF0dXNcbiAgICAgICAgICAgICAgICAgICAgICAgIH0gTUVTU0FHRTogJHt4aHIuc3RhdHVzVGV4dH1gLFxuICAgICAgICAgICAgICAgICAgICAgICAgc3RhdHVzOiB4aHIuc3RhdHVzLFxuICAgICAgICAgICAgICAgICAgICAgICAgeGhyLFxuICAgICAgICAgICAgICAgICAgICB9KTtcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICB9XG4gICAgICAgIH07XG4gICAgICAgIHhoci5vbmVycm9yID0gZXJyID0+IHJlamVjdChlcnIpO1xuICAgICAgICB4aHIuc2VuZChqc29uID8gSlNPTi5zdHJpbmdpZnkocGF5bG9hZCkgOiBwYXlsb2FkKTtcbiAgICB9KTtcbn1cblxuLyoqXG4gKiBBdXRvIGdldCBoZWFkZXJzIGFuZCByZWZyZXNoL3JldHJ5LlxuICpcbiAqIEBwYXJhbSB7ZnVuY3Rpb259IGdldEhlYWRlcnNcbiAqIEBwYXJhbSB7ZnVuY3Rpb259IHJlZnJlc2hcbiAqIEBwYXJhbSB7c3RyaW5nfSBiYXNlVXJsXG4gKi9cbmV4cG9ydCBmdW5jdGlvbiBhcGlSZXF1ZXN0KGJhc2VVcmwgPSAnJykge1xuICAgIHJldHVybiBmdW5jdGlvbigpIHtcbiAgICAgICAgY29uc3QgdXJsID0gYmFzZVVybCArIGFyZ3VtZW50c1swXTtcbiAgICAgICAgY29uc3Qgb3B0aW9ucyA9IGFyZ3VtZW50c1sxXSB8fCB7fTtcbiAgICAgICAgb3B0aW9ucy5oZWFkZXJzID0gey4uLm9wdGlvbnMuaGVhZGVyc307XG4gICAgICAgIHJldHVybiBuZXcgUHJvbWlzZShyZXNvbHZlID0+IHtcbiAgICAgICAgICAgIHhoclJlcXVlc3QodXJsLCBvcHRpb25zKS50aGVuKHJlc29sdmUpO1xuICAgICAgICB9KTtcbiAgICB9O1xufVxuIiwiaW1wb3J0IHtsb2FkQ3NzLCBsb2FkU2NyaXB0fSBmcm9tICcuLi8uLi9jb21tb25zL2pzJztcblxuZXhwb3J0IGZ1bmN0aW9uIGxvYWRSZXF1aXJlbWVudChyZXF1aXJlbWVudCkge1xuICAgIHJldHVybiBuZXcgUHJvbWlzZSgocmVzb2x2ZSwgcmVqZWN0KSA9PiB7XG4gICAgICAgIGNvbnN0IHt1cmwsIGtpbmQsIG1ldGF9ID0gcmVxdWlyZW1lbnQ7XG4gICAgICAgIGxldCBtZXRob2Q7XG4gICAgICAgIGlmIChraW5kID09PSAnanMnKSB7XG4gICAgICAgICAgICBtZXRob2QgPSBsb2FkU2NyaXB0O1xuICAgICAgICB9IGVsc2UgaWYgKGtpbmQgPT09ICdjc3MnKSB7XG4gICAgICAgICAgICBtZXRob2QgPSBsb2FkQ3NzO1xuICAgICAgICB9IGVsc2UgaWYgKGtpbmQgPT09ICdtYXAnKSB7XG4gICAgICAgICAgICByZXR1cm4gcmVzb2x2ZSgpO1xuICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgcmV0dXJuIHJlamVjdCh7ZXJyb3I6IGBJbnZhbGlkIHJlcXVpcmVtZW50IGtpbmQ6ICR7a2luZH1gfSk7XG4gICAgICAgIH1cbiAgICAgICAgcmV0dXJuIG1ldGhvZCh1cmwsIG1ldGEpXG4gICAgICAgICAgICAudGhlbihyZXNvbHZlKVxuICAgICAgICAgICAgLmNhdGNoKHJlamVjdCk7XG4gICAgfSk7XG59XG5cbmV4cG9ydCBmdW5jdGlvbiBsb2FkUmVxdWlyZW1lbnRzKHJlcXVpcmVtZW50cywgcGFja2FnZXMpIHtcbiAgICByZXR1cm4gbmV3IFByb21pc2UoKHJlc29sdmUsIHJlamVjdCkgPT4ge1xuICAgICAgICBsZXQgbG9hZGluZ3MgPSBbXTtcbiAgICAgICAgLy8gTG9hZCBwYWNrYWdlcyBmaXJzdC5cbiAgICAgICAgT2JqZWN0LmtleXMocGFja2FnZXMpLmZvckVhY2gocGFja19uYW1lID0+IHtcbiAgICAgICAgICAgIGNvbnN0IHBhY2sgPSBwYWNrYWdlc1twYWNrX25hbWVdO1xuICAgICAgICAgICAgbG9hZGluZ3MgPSBsb2FkaW5ncy5jb25jYXQocGFjay5yZXF1aXJlbWVudHMubWFwKGxvYWRSZXF1aXJlbWVudCkpO1xuICAgICAgICB9KTtcbiAgICAgICAgLy8gVGhlbiBsb2FkIHJlcXVpcmVtZW50cyBzbyB0aGV5IGNhbiB1c2UgcGFja2FnZXNcbiAgICAgICAgLy8gYW5kIG92ZXJyaWRlIGNzcy5cbiAgICAgICAgUHJvbWlzZS5hbGwobG9hZGluZ3MpXG4gICAgICAgICAgICAudGhlbigoKSA9PiB7XG4gICAgICAgICAgICAgICAgbGV0IGkgPSAwO1xuICAgICAgICAgICAgICAgIC8vIExvYWQgaW4gb3JkZXIuXG4gICAgICAgICAgICAgICAgY29uc3QgaGFuZGxlciA9ICgpID0+IHtcbiAgICAgICAgICAgICAgICAgICAgaWYgKGkgPCByZXF1aXJlbWVudHMubGVuZ3RoKSB7XG4gICAgICAgICAgICAgICAgICAgICAgICBsb2FkUmVxdWlyZW1lbnQocmVxdWlyZW1lbnRzW2ldKS50aGVuKCgpID0+IHtcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICBpKys7XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgaGFuZGxlcigpO1xuICAgICAgICAgICAgICAgICAgICAgICAgfSk7XG4gICAgICAgICAgICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAgICAgICAgICAgICByZXNvbHZlKCk7XG4gICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICB9O1xuICAgICAgICAgICAgICAgIGhhbmRsZXIoKTtcbiAgICAgICAgICAgIH0pXG4gICAgICAgICAgICAuY2F0Y2gocmVqZWN0KTtcbiAgICB9KTtcbn1cbiIsIm1vZHVsZS5leHBvcnRzID0gX19XRUJQQUNLX0VYVEVSTkFMX01PRFVMRV9yZWFjdF9fOyIsIm1vZHVsZS5leHBvcnRzID0gX19XRUJQQUNLX0VYVEVSTkFMX01PRFVMRV9yZWFjdF9kb21fXzsiXSwic291cmNlUm9vdCI6IiJ9