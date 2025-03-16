"use strict";

function _typeof(o) { "@babel/helpers - typeof"; return _typeof = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function (o) { return typeof o; } : function (o) { return o && "function" == typeof Symbol && o.constructor === Symbol && o !== Symbol.prototype ? "symbol" : typeof o; }, _typeof(o); }
Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;
var _react = _interopRequireWildcard(require("react"));
var _card = require("@/components/ui/card");
var _button = require("@/components/ui/button");
var _select = require("@/components/ui/select");
var _slider = require("@/components/ui/slider");
var _badge = require("@/components/ui/badge");
var _lucideReact = require("lucide-react");
var _alert = require("@/components/ui/alert");
var _label = require("@/components/ui/label");
var _input = require("@/components/ui/input");
var _progress = require("@/components/ui/progress");
function _getRequireWildcardCache(e) { if ("function" != typeof WeakMap) return null; var r = new WeakMap(), t = new WeakMap(); return (_getRequireWildcardCache = function _getRequireWildcardCache(e) { return e ? t : r; })(e); }
function _interopRequireWildcard(e, r) { if (!r && e && e.__esModule) return e; if (null === e || "object" != _typeof(e) && "function" != typeof e) return { default: e }; var t = _getRequireWildcardCache(r); if (t && t.has(e)) return t.get(e); var n = { __proto__: null }, a = Object.defineProperty && Object.getOwnPropertyDescriptor; for (var u in e) if ("default" !== u && {}.hasOwnProperty.call(e, u)) { var i = a ? Object.getOwnPropertyDescriptor(e, u) : null; i && (i.get || i.set) ? Object.defineProperty(n, u, i) : n[u] = e[u]; } return n.default = e, t && t.set(e, n), n; }
function _toConsumableArray(r) { return _arrayWithoutHoles(r) || _iterableToArray(r) || _unsupportedIterableToArray(r) || _nonIterableSpread(); }
function _nonIterableSpread() { throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); }
function _iterableToArray(r) { if ("undefined" != typeof Symbol && null != r[Symbol.iterator] || null != r["@@iterator"]) return Array.from(r); }
function _arrayWithoutHoles(r) { if (Array.isArray(r)) return _arrayLikeToArray(r); }
function ownKeys(e, r) { var t = Object.keys(e); if (Object.getOwnPropertySymbols) { var o = Object.getOwnPropertySymbols(e); r && (o = o.filter(function (r) { return Object.getOwnPropertyDescriptor(e, r).enumerable; })), t.push.apply(t, o); } return t; }
function _objectSpread(e) { for (var r = 1; r < arguments.length; r++) { var t = null != arguments[r] ? arguments[r] : {}; r % 2 ? ownKeys(Object(t), !0).forEach(function (r) { _defineProperty(e, r, t[r]); }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(t)) : ownKeys(Object(t)).forEach(function (r) { Object.defineProperty(e, r, Object.getOwnPropertyDescriptor(t, r)); }); } return e; }
function _defineProperty(e, r, t) { return (r = _toPropertyKey(r)) in e ? Object.defineProperty(e, r, { value: t, enumerable: !0, configurable: !0, writable: !0 }) : e[r] = t, e; }
function _toPropertyKey(t) { var i = _toPrimitive(t, "string"); return "symbol" == _typeof(i) ? i : i + ""; }
function _toPrimitive(t, r) { if ("object" != _typeof(t) || !t) return t; var e = t[Symbol.toPrimitive]; if (void 0 !== e) { var i = e.call(t, r || "default"); if ("object" != _typeof(i)) return i; throw new TypeError("@@toPrimitive must return a primitive value."); } return ("string" === r ? String : Number)(t); }
function _slicedToArray(r, e) { return _arrayWithHoles(r) || _iterableToArrayLimit(r, e) || _unsupportedIterableToArray(r, e) || _nonIterableRest(); }
function _nonIterableRest() { throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); }
function _unsupportedIterableToArray(r, a) { if (r) { if ("string" == typeof r) return _arrayLikeToArray(r, a); var t = {}.toString.call(r).slice(8, -1); return "Object" === t && r.constructor && (t = r.constructor.name), "Map" === t || "Set" === t ? Array.from(r) : "Arguments" === t || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(t) ? _arrayLikeToArray(r, a) : void 0; } }
function _arrayLikeToArray(r, a) { (null == a || a > r.length) && (a = r.length); for (var e = 0, n = Array(a); e < a; e++) n[e] = r[e]; return n; }
function _iterableToArrayLimit(r, l) { var t = null == r ? null : "undefined" != typeof Symbol && r[Symbol.iterator] || r["@@iterator"]; if (null != t) { var e, n, i, u, a = [], f = !0, o = !1; try { if (i = (t = t.call(r)).next, 0 === l) { if (Object(t) !== t) return; f = !1; } else for (; !(f = (e = i.call(t)).done) && (a.push(e.value), a.length !== l); f = !0); } catch (r) { o = !0, n = r; } finally { try { if (!f && null != t.return && (u = t.return(), Object(u) !== u)) return; } finally { if (o) throw n; } } return a; } }
function _arrayWithHoles(r) { if (Array.isArray(r)) return r; }
function _regeneratorRuntime() { "use strict"; /*! regenerator-runtime -- Copyright (c) 2014-present, Facebook, Inc. -- license (MIT): https://github.com/facebook/regenerator/blob/main/LICENSE */ _regeneratorRuntime = function _regeneratorRuntime() { return e; }; var t, e = {}, r = Object.prototype, n = r.hasOwnProperty, o = Object.defineProperty || function (t, e, r) { t[e] = r.value; }, i = "function" == typeof Symbol ? Symbol : {}, a = i.iterator || "@@iterator", c = i.asyncIterator || "@@asyncIterator", u = i.toStringTag || "@@toStringTag"; function define(t, e, r) { return Object.defineProperty(t, e, { value: r, enumerable: !0, configurable: !0, writable: !0 }), t[e]; } try { define({}, ""); } catch (t) { define = function define(t, e, r) { return t[e] = r; }; } function wrap(t, e, r, n) { var i = e && e.prototype instanceof Generator ? e : Generator, a = Object.create(i.prototype), c = new Context(n || []); return o(a, "_invoke", { value: makeInvokeMethod(t, r, c) }), a; } function tryCatch(t, e, r) { try { return { type: "normal", arg: t.call(e, r) }; } catch (t) { return { type: "throw", arg: t }; } } e.wrap = wrap; var h = "suspendedStart", l = "suspendedYield", f = "executing", s = "completed", y = {}; function Generator() {} function GeneratorFunction() {} function GeneratorFunctionPrototype() {} var p = {}; define(p, a, function () { return this; }); var d = Object.getPrototypeOf, v = d && d(d(values([]))); v && v !== r && n.call(v, a) && (p = v); var g = GeneratorFunctionPrototype.prototype = Generator.prototype = Object.create(p); function defineIteratorMethods(t) { ["next", "throw", "return"].forEach(function (e) { define(t, e, function (t) { return this._invoke(e, t); }); }); } function AsyncIterator(t, e) { function invoke(r, o, i, a) { var c = tryCatch(t[r], t, o); if ("throw" !== c.type) { var u = c.arg, h = u.value; return h && "object" == _typeof(h) && n.call(h, "__await") ? e.resolve(h.__await).then(function (t) { invoke("next", t, i, a); }, function (t) { invoke("throw", t, i, a); }) : e.resolve(h).then(function (t) { u.value = t, i(u); }, function (t) { return invoke("throw", t, i, a); }); } a(c.arg); } var r; o(this, "_invoke", { value: function value(t, n) { function callInvokeWithMethodAndArg() { return new e(function (e, r) { invoke(t, n, e, r); }); } return r = r ? r.then(callInvokeWithMethodAndArg, callInvokeWithMethodAndArg) : callInvokeWithMethodAndArg(); } }); } function makeInvokeMethod(e, r, n) { var o = h; return function (i, a) { if (o === f) throw Error("Generator is already running"); if (o === s) { if ("throw" === i) throw a; return { value: t, done: !0 }; } for (n.method = i, n.arg = a;;) { var c = n.delegate; if (c) { var u = maybeInvokeDelegate(c, n); if (u) { if (u === y) continue; return u; } } if ("next" === n.method) n.sent = n._sent = n.arg;else if ("throw" === n.method) { if (o === h) throw o = s, n.arg; n.dispatchException(n.arg); } else "return" === n.method && n.abrupt("return", n.arg); o = f; var p = tryCatch(e, r, n); if ("normal" === p.type) { if (o = n.done ? s : l, p.arg === y) continue; return { value: p.arg, done: n.done }; } "throw" === p.type && (o = s, n.method = "throw", n.arg = p.arg); } }; } function maybeInvokeDelegate(e, r) { var n = r.method, o = e.iterator[n]; if (o === t) return r.delegate = null, "throw" === n && e.iterator.return && (r.method = "return", r.arg = t, maybeInvokeDelegate(e, r), "throw" === r.method) || "return" !== n && (r.method = "throw", r.arg = new TypeError("The iterator does not provide a '" + n + "' method")), y; var i = tryCatch(o, e.iterator, r.arg); if ("throw" === i.type) return r.method = "throw", r.arg = i.arg, r.delegate = null, y; var a = i.arg; return a ? a.done ? (r[e.resultName] = a.value, r.next = e.nextLoc, "return" !== r.method && (r.method = "next", r.arg = t), r.delegate = null, y) : a : (r.method = "throw", r.arg = new TypeError("iterator result is not an object"), r.delegate = null, y); } function pushTryEntry(t) { var e = { tryLoc: t[0] }; 1 in t && (e.catchLoc = t[1]), 2 in t && (e.finallyLoc = t[2], e.afterLoc = t[3]), this.tryEntries.push(e); } function resetTryEntry(t) { var e = t.completion || {}; e.type = "normal", delete e.arg, t.completion = e; } function Context(t) { this.tryEntries = [{ tryLoc: "root" }], t.forEach(pushTryEntry, this), this.reset(!0); } function values(e) { if (e || "" === e) { var r = e[a]; if (r) return r.call(e); if ("function" == typeof e.next) return e; if (!isNaN(e.length)) { var o = -1, i = function next() { for (; ++o < e.length;) if (n.call(e, o)) return next.value = e[o], next.done = !1, next; return next.value = t, next.done = !0, next; }; return i.next = i; } } throw new TypeError(_typeof(e) + " is not iterable"); } return GeneratorFunction.prototype = GeneratorFunctionPrototype, o(g, "constructor", { value: GeneratorFunctionPrototype, configurable: !0 }), o(GeneratorFunctionPrototype, "constructor", { value: GeneratorFunction, configurable: !0 }), GeneratorFunction.displayName = define(GeneratorFunctionPrototype, u, "GeneratorFunction"), e.isGeneratorFunction = function (t) { var e = "function" == typeof t && t.constructor; return !!e && (e === GeneratorFunction || "GeneratorFunction" === (e.displayName || e.name)); }, e.mark = function (t) { return Object.setPrototypeOf ? Object.setPrototypeOf(t, GeneratorFunctionPrototype) : (t.__proto__ = GeneratorFunctionPrototype, define(t, u, "GeneratorFunction")), t.prototype = Object.create(g), t; }, e.awrap = function (t) { return { __await: t }; }, defineIteratorMethods(AsyncIterator.prototype), define(AsyncIterator.prototype, c, function () { return this; }), e.AsyncIterator = AsyncIterator, e.async = function (t, r, n, o, i) { void 0 === i && (i = Promise); var a = new AsyncIterator(wrap(t, r, n, o), i); return e.isGeneratorFunction(r) ? a : a.next().then(function (t) { return t.done ? t.value : a.next(); }); }, defineIteratorMethods(g), define(g, u, "Generator"), define(g, a, function () { return this; }), define(g, "toString", function () { return "[object Generator]"; }), e.keys = function (t) { var e = Object(t), r = []; for (var n in e) r.push(n); return r.reverse(), function next() { for (; r.length;) { var t = r.pop(); if (t in e) return next.value = t, next.done = !1, next; } return next.done = !0, next; }; }, e.values = values, Context.prototype = { constructor: Context, reset: function reset(e) { if (this.prev = 0, this.next = 0, this.sent = this._sent = t, this.done = !1, this.delegate = null, this.method = "next", this.arg = t, this.tryEntries.forEach(resetTryEntry), !e) for (var r in this) "t" === r.charAt(0) && n.call(this, r) && !isNaN(+r.slice(1)) && (this[r] = t); }, stop: function stop() { this.done = !0; var t = this.tryEntries[0].completion; if ("throw" === t.type) throw t.arg; return this.rval; }, dispatchException: function dispatchException(e) { if (this.done) throw e; var r = this; function handle(n, o) { return a.type = "throw", a.arg = e, r.next = n, o && (r.method = "next", r.arg = t), !!o; } for (var o = this.tryEntries.length - 1; o >= 0; --o) { var i = this.tryEntries[o], a = i.completion; if ("root" === i.tryLoc) return handle("end"); if (i.tryLoc <= this.prev) { var c = n.call(i, "catchLoc"), u = n.call(i, "finallyLoc"); if (c && u) { if (this.prev < i.catchLoc) return handle(i.catchLoc, !0); if (this.prev < i.finallyLoc) return handle(i.finallyLoc); } else if (c) { if (this.prev < i.catchLoc) return handle(i.catchLoc, !0); } else { if (!u) throw Error("try statement without catch or finally"); if (this.prev < i.finallyLoc) return handle(i.finallyLoc); } } } }, abrupt: function abrupt(t, e) { for (var r = this.tryEntries.length - 1; r >= 0; --r) { var o = this.tryEntries[r]; if (o.tryLoc <= this.prev && n.call(o, "finallyLoc") && this.prev < o.finallyLoc) { var i = o; break; } } i && ("break" === t || "continue" === t) && i.tryLoc <= e && e <= i.finallyLoc && (i = null); var a = i ? i.completion : {}; return a.type = t, a.arg = e, i ? (this.method = "next", this.next = i.finallyLoc, y) : this.complete(a); }, complete: function complete(t, e) { if ("throw" === t.type) throw t.arg; return "break" === t.type || "continue" === t.type ? this.next = t.arg : "return" === t.type ? (this.rval = this.arg = t.arg, this.method = "return", this.next = "end") : "normal" === t.type && e && (this.next = e), y; }, finish: function finish(t) { for (var e = this.tryEntries.length - 1; e >= 0; --e) { var r = this.tryEntries[e]; if (r.finallyLoc === t) return this.complete(r.completion, r.afterLoc), resetTryEntry(r), y; } }, catch: function _catch(t) { for (var e = this.tryEntries.length - 1; e >= 0; --e) { var r = this.tryEntries[e]; if (r.tryLoc === t) { var n = r.completion; if ("throw" === n.type) { var o = n.arg; resetTryEntry(r); } return o; } } throw Error("illegal catch attempt"); }, delegateYield: function delegateYield(e, r, n) { return this.delegate = { iterator: values(e), resultName: r, nextLoc: n }, "next" === this.method && (this.arg = t), y; } }, e; }
function asyncGeneratorStep(n, t, e, r, o, a, c) { try { var i = n[a](c), u = i.value; } catch (n) { return void e(n); } i.done ? t(u) : Promise.resolve(u).then(r, o); }
function _asyncToGenerator(n) { return function () { var t = this, e = arguments; return new Promise(function (r, o) { var a = n.apply(t, e); function _next(n) { asyncGeneratorStep(a, r, o, _next, _throw, "next", n); } function _throw(n) { asyncGeneratorStep(a, r, o, _next, _throw, "throw", n); } _next(void 0); }); }; }
// Mock API for development - will be replaced with actual API calls
var API_URL = 'http://localhost:5000/api';
var fetchPersonalities = /*#__PURE__*/function () {
  var _ref = _asyncToGenerator(/*#__PURE__*/_regeneratorRuntime().mark(function _callee() {
    var response;
    return _regeneratorRuntime().wrap(function _callee$(_context) {
      while (1) switch (_context.prev = _context.next) {
        case 0:
          _context.prev = 0;
          _context.next = 3;
          return fetch("".concat(API_URL, "/personalities"));
        case 3:
          response = _context.sent;
          _context.next = 6;
          return response.json();
        case 6:
          return _context.abrupt("return", _context.sent);
        case 9:
          _context.prev = 9;
          _context.t0 = _context["catch"](0);
          console.error('Error fetching personalities:', _context.t0);
          return _context.abrupt("return", {});
        case 13:
        case "end":
          return _context.stop();
      }
    }, _callee, null, [[0, 9]]);
  }));
  return function fetchPersonalities() {
    return _ref.apply(this, arguments);
  };
}();
var createGame = /*#__PURE__*/function () {
  var _ref2 = _asyncToGenerator(/*#__PURE__*/_regeneratorRuntime().mark(function _callee2(personalities) {
    var response;
    return _regeneratorRuntime().wrap(function _callee2$(_context2) {
      while (1) switch (_context2.prev = _context2.next) {
        case 0:
          _context2.prev = 0;
          _context2.next = 3;
          return fetch("".concat(API_URL, "/create_game"), {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              personalities: personalities
            })
          });
        case 3:
          response = _context2.sent;
          _context2.next = 6;
          return response.json();
        case 6:
          return _context2.abrupt("return", _context2.sent);
        case 9:
          _context2.prev = 9;
          _context2.t0 = _context2["catch"](0);
          console.error('Error creating game:', _context2.t0);
          return _context2.abrupt("return", {
            error: 'Failed to create game'
          });
        case 13:
        case "end":
          return _context2.stop();
      }
    }, _callee2, null, [[0, 9]]);
  }));
  return function createGame(_x) {
    return _ref2.apply(this, arguments);
  };
}();
var startGame = /*#__PURE__*/function () {
  var _ref3 = _asyncToGenerator(/*#__PURE__*/_regeneratorRuntime().mark(function _callee3(gameId) {
    var response;
    return _regeneratorRuntime().wrap(function _callee3$(_context3) {
      while (1) switch (_context3.prev = _context3.next) {
        case 0:
          _context3.prev = 0;
          _context3.next = 3;
          return fetch("".concat(API_URL, "/start_game/").concat(gameId), {
            method: 'POST'
          });
        case 3:
          response = _context3.sent;
          _context3.next = 6;
          return response.json();
        case 6:
          return _context3.abrupt("return", _context3.sent);
        case 9:
          _context3.prev = 9;
          _context3.t0 = _context3["catch"](0);
          console.error('Error starting game:', _context3.t0);
          return _context3.abrupt("return", {
            error: 'Failed to start game'
          });
        case 13:
        case "end":
          return _context3.stop();
      }
    }, _callee3, null, [[0, 9]]);
  }));
  return function startGame(_x2) {
    return _ref3.apply(this, arguments);
  };
}();
var processNight = /*#__PURE__*/function () {
  var _ref4 = _asyncToGenerator(/*#__PURE__*/_regeneratorRuntime().mark(function _callee4(gameId) {
    var response;
    return _regeneratorRuntime().wrap(function _callee4$(_context4) {
      while (1) switch (_context4.prev = _context4.next) {
        case 0:
          _context4.prev = 0;
          _context4.next = 3;
          return fetch("".concat(API_URL, "/process_night/").concat(gameId), {
            method: 'POST'
          });
        case 3:
          response = _context4.sent;
          _context4.next = 6;
          return response.json();
        case 6:
          return _context4.abrupt("return", _context4.sent);
        case 9:
          _context4.prev = 9;
          _context4.t0 = _context4["catch"](0);
          console.error('Error processing night:', _context4.t0);
          return _context4.abrupt("return", {
            error: 'Failed to process night'
          });
        case 13:
        case "end":
          return _context4.stop();
      }
    }, _callee4, null, [[0, 9]]);
  }));
  return function processNight(_x3) {
    return _ref4.apply(this, arguments);
  };
}();
var resolveNight = /*#__PURE__*/function () {
  var _ref5 = _asyncToGenerator(/*#__PURE__*/_regeneratorRuntime().mark(function _callee5(gameId) {
    var response;
    return _regeneratorRuntime().wrap(function _callee5$(_context5) {
      while (1) switch (_context5.prev = _context5.next) {
        case 0:
          _context5.prev = 0;
          _context5.next = 3;
          return fetch("".concat(API_URL, "/resolve_night/").concat(gameId), {
            method: 'POST'
          });
        case 3:
          response = _context5.sent;
          _context5.next = 6;
          return response.json();
        case 6:
          return _context5.abrupt("return", _context5.sent);
        case 9:
          _context5.prev = 9;
          _context5.t0 = _context5["catch"](0);
          console.error('Error resolving night:', _context5.t0);
          return _context5.abrupt("return", {
            error: 'Failed to resolve night'
          });
        case 13:
        case "end":
          return _context5.stop();
      }
    }, _callee5, null, [[0, 9]]);
  }));
  return function resolveNight(_x4) {
    return _ref5.apply(this, arguments);
  };
}();
var startDiscussion = /*#__PURE__*/function () {
  var _ref6 = _asyncToGenerator(/*#__PURE__*/_regeneratorRuntime().mark(function _callee6(gameId) {
    var response;
    return _regeneratorRuntime().wrap(function _callee6$(_context6) {
      while (1) switch (_context6.prev = _context6.next) {
        case 0:
          _context6.prev = 0;
          _context6.next = 3;
          return fetch("".concat(API_URL, "/start_discussion/").concat(gameId), {
            method: 'POST'
          });
        case 3:
          response = _context6.sent;
          _context6.next = 6;
          return response.json();
        case 6:
          return _context6.abrupt("return", _context6.sent);
        case 9:
          _context6.prev = 9;
          _context6.t0 = _context6["catch"](0);
          console.error('Error starting discussion:', _context6.t0);
          return _context6.abrupt("return", {
            error: 'Failed to start discussion'
          });
        case 13:
        case "end":
          return _context6.stop();
      }
    }, _callee6, null, [[0, 9]]);
  }));
  return function startDiscussion(_x5) {
    return _ref6.apply(this, arguments);
  };
}();
var simulateDiscussion = /*#__PURE__*/function () {
  var _ref7 = _asyncToGenerator(/*#__PURE__*/_regeneratorRuntime().mark(function _callee7(gameId) {
    var response;
    return _regeneratorRuntime().wrap(function _callee7$(_context7) {
      while (1) switch (_context7.prev = _context7.next) {
        case 0:
          _context7.prev = 0;
          _context7.next = 3;
          return fetch("".concat(API_URL, "/simulate_discussion/").concat(gameId), {
            method: 'POST'
          });
        case 3:
          response = _context7.sent;
          _context7.next = 6;
          return response.json();
        case 6:
          return _context7.abrupt("return", _context7.sent);
        case 9:
          _context7.prev = 9;
          _context7.t0 = _context7["catch"](0);
          console.error('Error simulating discussion:', _context7.t0);
          return _context7.abrupt("return", {
            error: 'Failed to simulate discussion'
          });
        case 13:
        case "end":
          return _context7.stop();
      }
    }, _callee7, null, [[0, 9]]);
  }));
  return function simulateDiscussion(_x6) {
    return _ref7.apply(this, arguments);
  };
}();
var processVoting = /*#__PURE__*/function () {
  var _ref8 = _asyncToGenerator(/*#__PURE__*/_regeneratorRuntime().mark(function _callee8(gameId) {
    var response;
    return _regeneratorRuntime().wrap(function _callee8$(_context8) {
      while (1) switch (_context8.prev = _context8.next) {
        case 0:
          _context8.prev = 0;
          _context8.next = 3;
          return fetch("".concat(API_URL, "/process_voting/").concat(gameId), {
            method: 'POST'
          });
        case 3:
          response = _context8.sent;
          _context8.next = 6;
          return response.json();
        case 6:
          return _context8.abrupt("return", _context8.sent);
        case 9:
          _context8.prev = 9;
          _context8.t0 = _context8["catch"](0);
          console.error('Error processing voting:', _context8.t0);
          return _context8.abrupt("return", {
            error: 'Failed to process voting'
          });
        case 13:
        case "end":
          return _context8.stop();
      }
    }, _callee8, null, [[0, 9]]);
  }));
  return function processVoting(_x7) {
    return _ref8.apply(this, arguments);
  };
}();
var getGameState = /*#__PURE__*/function () {
  var _ref9 = _asyncToGenerator(/*#__PURE__*/_regeneratorRuntime().mark(function _callee9(gameId) {
    var response;
    return _regeneratorRuntime().wrap(function _callee9$(_context9) {
      while (1) switch (_context9.prev = _context9.next) {
        case 0:
          _context9.prev = 0;
          _context9.next = 3;
          return fetch("".concat(API_URL, "/game_state/").concat(gameId));
        case 3:
          response = _context9.sent;
          _context9.next = 6;
          return response.json();
        case 6:
          return _context9.abrupt("return", _context9.sent);
        case 9:
          _context9.prev = 9;
          _context9.t0 = _context9["catch"](0);
          console.error('Error fetching game state:', _context9.t0);
          return _context9.abrupt("return", {
            error: 'Failed to fetch game state'
          });
        case 13:
        case "end":
          return _context9.stop();
      }
    }, _callee9, null, [[0, 9]]);
  }));
  return function getGameState(_x8) {
    return _ref9.apply(this, arguments);
  };
}();
var resetGame = /*#__PURE__*/function () {
  var _ref10 = _asyncToGenerator(/*#__PURE__*/_regeneratorRuntime().mark(function _callee10(gameId) {
    var response;
    return _regeneratorRuntime().wrap(function _callee10$(_context10) {
      while (1) switch (_context10.prev = _context10.next) {
        case 0:
          _context10.prev = 0;
          _context10.next = 3;
          return fetch("".concat(API_URL, "/reset_game/").concat(gameId), {
            method: 'POST'
          });
        case 3:
          response = _context10.sent;
          _context10.next = 6;
          return response.json();
        case 6:
          return _context10.abrupt("return", _context10.sent);
        case 9:
          _context10.prev = 9;
          _context10.t0 = _context10["catch"](0);
          console.error('Error resetting game:', _context10.t0);
          return _context10.abrupt("return", {
            error: 'Failed to reset game'
          });
        case 13:
        case "end":
          return _context10.stop();
      }
    }, _callee10, null, [[0, 9]]);
  }));
  return function resetGame(_x9) {
    return _ref10.apply(this, arguments);
  };
}();
var PersonalityCard = function PersonalityCard(_ref11) {
  var personality = _ref11.personality,
    details = _ref11.details,
    selected = _ref11.selected,
    onSelect = _ref11.onSelect,
    onCustomize = _ref11.onCustomize;
  return /*#__PURE__*/_react.default.createElement(_card.Card, {
    className: "w-64 h-72 m-2 cursor-pointer transition-all ".concat(selected ? 'border-4 border-blue-500' : 'hover:shadow-md'),
    onClick: onSelect
  }, /*#__PURE__*/_react.default.createElement(_card.CardHeader, {
    className: "pb-2"
  }, /*#__PURE__*/_react.default.createElement(_card.CardTitle, null, personality), /*#__PURE__*/_react.default.createElement(_card.CardDescription, {
    className: "h-20 overflow-auto"
  }, details.description)), /*#__PURE__*/_react.default.createElement(_card.CardContent, {
    className: "pb-2"
  }, /*#__PURE__*/_react.default.createElement("div", {
    className: "space-y-2"
  }, Object.entries(details.attributes).map(function (_ref12) {
    var _ref13 = _slicedToArray(_ref12, 2),
      attr = _ref13[0],
      value = _ref13[1];
    return /*#__PURE__*/_react.default.createElement("div", {
      key: attr,
      className: "flex items-center justify-between"
    }, /*#__PURE__*/_react.default.createElement("span", {
      className: "text-sm capitalize"
    }, attr), /*#__PURE__*/_react.default.createElement("div", {
      className: "w-32"
    }, /*#__PURE__*/_react.default.createElement(_progress.Progress, {
      value: value * 100,
      className: "h-2"
    })));
  }))), /*#__PURE__*/_react.default.createElement(_card.CardFooter, null, /*#__PURE__*/_react.default.createElement(_button.Button, {
    variant: "outline",
    size: "sm",
    onClick: function onClick(e) {
      e.stopPropagation();
      onCustomize(personality);
    }
  }, "Customize")));
};
var CustomizePersonalityModal = function CustomizePersonalityModal(_ref14) {
  var personality = _ref14.personality,
    details = _ref14.details,
    onSave = _ref14.onSave,
    onCancel = _ref14.onCancel;
  var _useState = (0, _react.useState)(details.attributes),
    _useState2 = _slicedToArray(_useState, 2),
    attributes = _useState2[0],
    setAttributes = _useState2[1];
  var handleAttributeChange = function handleAttributeChange(attr, value) {
    setAttributes(function (prev) {
      return _objectSpread(_objectSpread({}, prev), {}, _defineProperty({}, attr, value[0] / 100));
    });
  };
  return /*#__PURE__*/_react.default.createElement("div", {
    className: "fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
  }, /*#__PURE__*/_react.default.createElement(_card.Card, {
    className: "w-96 max-h-[90vh] overflow-auto"
  }, /*#__PURE__*/_react.default.createElement(_card.CardHeader, null, /*#__PURE__*/_react.default.createElement(_card.CardTitle, null, "Customize ", personality), /*#__PURE__*/_react.default.createElement(_card.CardDescription, null, "Adjust the attributes to create your perfect personality")), /*#__PURE__*/_react.default.createElement(_card.CardContent, {
    className: "space-y-4"
  }, Object.entries(attributes).map(function (_ref15) {
    var _ref16 = _slicedToArray(_ref15, 2),
      attr = _ref16[0],
      value = _ref16[1];
    return /*#__PURE__*/_react.default.createElement("div", {
      key: attr,
      className: "space-y-2"
    }, /*#__PURE__*/_react.default.createElement("div", {
      className: "flex justify-between"
    }, /*#__PURE__*/_react.default.createElement(_label.Label, {
      htmlFor: attr,
      className: "capitalize"
    }, attr), /*#__PURE__*/_react.default.createElement("span", null, Math.round(value * 100), "%")), /*#__PURE__*/_react.default.createElement(_slider.Slider, {
      id: attr,
      value: [value * 100],
      min: 0,
      max: 100,
      step: 5,
      onValueChange: function onValueChange(val) {
        return handleAttributeChange(attr, val);
      }
    }));
  })), /*#__PURE__*/_react.default.createElement(_card.CardFooter, {
    className: "flex justify-between"
  }, /*#__PURE__*/_react.default.createElement(_button.Button, {
    variant: "outline",
    onClick: onCancel
  }, "Cancel"), /*#__PURE__*/_react.default.createElement(_button.Button, {
    onClick: function onClick() {
      return onSave(personality, attributes);
    }
  }, "Save Changes"))));
};
var ChatBubble = function ChatBubble(_ref17) {
  var player = _ref17.player,
    message = _ref17.message,
    isDead = _ref17.isDead;
  return /*#__PURE__*/_react.default.createElement("div", {
    className: "flex items-start gap-2 my-2 ".concat(isDead ? 'opacity-50' : '')
  }, /*#__PURE__*/_react.default.createElement("div", {
    className: "rounded-full w-8 h-8 flex items-center justify-center bg-gray-200 text-gray-700 flex-shrink-0"
  }, player[0]), /*#__PURE__*/_react.default.createElement("div", {
    className: "bg-gray-100 rounded-lg p-2 max-w-[80%]"
  }, /*#__PURE__*/_react.default.createElement("div", {
    className: "font-semibold"
  }, player), /*#__PURE__*/_react.default.createElement("div", null, message)));
};
var NightActionAnimation = function NightActionAnimation(_ref18) {
  var action = _ref18.action,
    target = _ref18.target,
    complete = _ref18.complete;
  var _useState3 = (0, _react.useState)(0),
    _useState4 = _slicedToArray(_useState3, 2),
    progress = _useState4[0],
    setProgress = _useState4[1];
  (0, _react.useEffect)(function () {
    var timer = setInterval(function () {
      setProgress(function (prev) {
        if (prev >= 100) {
          clearInterval(timer);
          complete();
          return 100;
        }
        return prev + 5;
      });
    }, 100);
    return function () {
      return clearInterval(timer);
    };
  }, [complete]);
  return /*#__PURE__*/_react.default.createElement("div", {
    className: "flex flex-col items-center justify-center p-4"
  }, /*#__PURE__*/_react.default.createElement("div", {
    className: "text-xl mb-4"
  }, action === 'mafia' && 'The Mafia is choosing their target...', action === 'detective' && 'The Detective is investigating...', action === 'doctor' && 'The Doctor is protecting someone...'), target && /*#__PURE__*/_react.default.createElement("div", {
    className: "text-2xl mb-4"
  }, "Selected: ", target), /*#__PURE__*/_react.default.createElement(_progress.Progress, {
    value: progress,
    className: "w-64 h-4 mb-4"
  }));
};
var GameSetup = function GameSetup(_ref19) {
  var onStartGame = _ref19.onStartGame;
  var _useState5 = (0, _react.useState)({}),
    _useState6 = _slicedToArray(_useState5, 2),
    personalities = _useState6[0],
    setPersonalities = _useState6[1];
  var _useState7 = (0, _react.useState)([]),
    _useState8 = _slicedToArray(_useState7, 2),
    selectedPersonalities = _useState8[0],
    setSelectedPersonalities = _useState8[1];
  var _useState9 = (0, _react.useState)(null),
    _useState10 = _slicedToArray(_useState9, 2),
    customizing = _useState10[0],
    setCustomizing = _useState10[1];
  var _useState11 = (0, _react.useState)({
      name: '',
      attributes: {}
    }),
    _useState12 = _slicedToArray(_useState11, 2),
    customPersonality = _useState12[0],
    setCustomPersonality = _useState12[1];
  var _useState13 = (0, _react.useState)(false),
    _useState14 = _slicedToArray(_useState13, 2),
    showCustomForm = _useState14[0],
    setShowCustomForm = _useState14[1];
  (0, _react.useEffect)(function () {
    var loadPersonalities = /*#__PURE__*/function () {
      var _ref20 = _asyncToGenerator(/*#__PURE__*/_regeneratorRuntime().mark(function _callee11() {
        var data;
        return _regeneratorRuntime().wrap(function _callee11$(_context11) {
          while (1) switch (_context11.prev = _context11.next) {
            case 0:
              _context11.next = 2;
              return fetchPersonalities();
            case 2:
              data = _context11.sent;
              setPersonalities(data);
            case 4:
            case "end":
              return _context11.stop();
          }
        }, _callee11);
      }));
      return function loadPersonalities() {
        return _ref20.apply(this, arguments);
      };
    }();
    loadPersonalities();
  }, []);
  var handleSelectPersonality = function handleSelectPersonality(personality) {
    if (selectedPersonalities.includes(personality)) {
      setSelectedPersonalities(function (prev) {
        return prev.filter(function (p) {
          return p !== personality;
        });
      });
    } else if (selectedPersonalities.length < 6) {
      setSelectedPersonalities(function (prev) {
        return [].concat(_toConsumableArray(prev), [personality]);
      });
    }
  };
  var handleCustomizePersonality = function handleCustomizePersonality(personality) {
    setCustomizing(personality);
  };
  var handleSaveCustomization = function handleSaveCustomization(personality, attributes) {
    setPersonalities(function (prev) {
      return _objectSpread(_objectSpread({}, prev), {}, _defineProperty({}, personality, _objectSpread(_objectSpread({}, prev[personality]), {}, {
        attributes: attributes
      })));
    });
    setCustomizing(null);
  };
  var handleAddCustomPersonality = function handleAddCustomPersonality() {
    if (customPersonality.name.trim() === '') return;
    setPersonalities(function (prev) {
      return _objectSpread(_objectSpread({}, prev), {}, _defineProperty({}, customPersonality.name, {
        description: "Custom personality",
        attributes: customPersonality.attributes,
        prompt_style: "You have a unique personality as ".concat(customPersonality.name, ".")
      }));
    });
    setCustomPersonality({
      name: '',
      attributes: {}
    });
    setShowCustomForm(false);
  };
  return /*#__PURE__*/_react.default.createElement("div", {
    className: "container mx-auto p-4"
  }, /*#__PURE__*/_react.default.createElement(_card.Card, {
    className: "mb-6"
  }, /*#__PURE__*/_react.default.createElement(_card.CardHeader, null, /*#__PURE__*/_react.default.createElement(_card.CardTitle, null, "Mafia Game Setup"), /*#__PURE__*/_react.default.createElement(_card.CardDescription, null, "Select 6 personalities for your game")), /*#__PURE__*/_react.default.createElement(_card.CardContent, null, /*#__PURE__*/_react.default.createElement("div", {
    className: "flex items-center justify-between mb-4"
  }, /*#__PURE__*/_react.default.createElement("div", {
    className: "text-lg font-medium"
  }, "Selected: ", selectedPersonalities.length, "/6"), /*#__PURE__*/_react.default.createElement(_button.Button, {
    disabled: selectedPersonalities.length !== 6,
    onClick: function onClick() {
      return onStartGame(selectedPersonalities);
    }
  }, "Start Game")), /*#__PURE__*/_react.default.createElement("div", {
    className: "mb-4"
  }, /*#__PURE__*/_react.default.createElement(_button.Button, {
    variant: "outline",
    onClick: function onClick() {
      return setShowCustomForm(true);
    }
  }, "Create Custom Personality")), showCustomForm && /*#__PURE__*/_react.default.createElement(_card.Card, {
    className: "mb-4 p-4"
  }, /*#__PURE__*/_react.default.createElement(_card.CardHeader, {
    className: "p-2"
  }, /*#__PURE__*/_react.default.createElement(_card.CardTitle, {
    className: "text-lg"
  }, "Create Custom Personality")), /*#__PURE__*/_react.default.createElement(_card.CardContent, {
    className: "p-2 space-y-4"
  }, /*#__PURE__*/_react.default.createElement("div", null, /*#__PURE__*/_react.default.createElement(_label.Label, {
    htmlFor: "name"
  }, "Name"), /*#__PURE__*/_react.default.createElement(_input.Input, {
    id: "name",
    value: customPersonality.name,
    onChange: function onChange(e) {
      return setCustomPersonality(function (prev) {
        return _objectSpread(_objectSpread({}, prev), {}, {
          name: e.target.value
        });
      });
    }
  })), ['truthfulness', 'aggressiveness', 'suspicion', 'persuasiveness', 'loyalty'].map(function (attr) {
    return /*#__PURE__*/_react.default.createElement("div", {
      key: attr,
      className: "space-y-2"
    }, /*#__PURE__*/_react.default.createElement("div", {
      className: "flex justify-between"
    }, /*#__PURE__*/_react.default.createElement(_label.Label, {
      htmlFor: attr,
      className: "capitalize"
    }, attr), /*#__PURE__*/_react.default.createElement("span", null, customPersonality.attributes[attr] ? Math.round(customPersonality.attributes[attr] * 100) : 50, "%")), /*#__PURE__*/_react.default.createElement(_slider.Slider, {
      id: attr,
      value: [customPersonality.attributes[attr] ? customPersonality.attributes[attr] * 100 : 50],
      min: 0,
      max: 100,
      step: 5,
      onValueChange: function onValueChange(val) {
        return setCustomPersonality(function (prev) {
          return _objectSpread(_objectSpread({}, prev), {}, {
            attributes: _objectSpread(_objectSpread({}, prev.attributes), {}, _defineProperty({}, attr, val[0] / 100))
          });
        });
      }
    }));
  })), /*#__PURE__*/_react.default.createElement(_card.CardFooter, {
    className: "p-2 flex justify-between"
  }, /*#__PURE__*/_react.default.createElement(_button.Button, {
    variant: "outline",
    onClick: function onClick() {
      return setShowCustomForm(false);
    }
  }, "Cancel"), /*#__PURE__*/_react.default.createElement(_button.Button, {
    onClick: handleAddCustomPersonality
  }, "Add Personality"))), /*#__PURE__*/_react.default.createElement("div", {
    className: "flex flex-wrap justify-center"
  }, Object.entries(personalities).map(function (_ref21) {
    var _ref22 = _slicedToArray(_ref21, 2),
      personality = _ref22[0],
      details = _ref22[1];
    return /*#__PURE__*/_react.default.createElement(PersonalityCard, {
      key: personality,
      personality: personality,
      details: details,
      selected: selectedPersonalities.includes(personality),
      onSelect: function onSelect() {
        return handleSelectPersonality(personality);
      },
      onCustomize: handleCustomizePersonality
    });
  })))), customizing && /*#__PURE__*/_react.default.createElement(CustomizePersonalityModal, {
    personality: customizing,
    details: personalities[customizing],
    onSave: handleSaveCustomization,
    onCancel: function onCancel() {
      return setCustomizing(null);
    }
  }));
};
var GamePlay = function GamePlay(_ref23) {
  var _gameState$players, _gameState$events;
  var gameId = _ref23.gameId;
  var _useState15 = (0, _react.useState)(null),
    _useState16 = _slicedToArray(_useState15, 2),
    gameState = _useState16[0],
    setGameState = _useState16[1];
  var _useState17 = (0, _react.useState)(true),
    _useState18 = _slicedToArray(_useState17, 2),
    loading = _useState18[0],
    setLoading = _useState18[1];
  var _useState19 = (0, _react.useState)(null),
    _useState20 = _slicedToArray(_useState19, 2),
    error = _useState20[0],
    setError = _useState20[1];
  var _useState21 = (0, _react.useState)(null),
    _useState22 = _slicedToArray(_useState21, 2),
    nightAction = _useState22[0],
    setNightAction = _useState22[1];
  var _useState23 = (0, _react.useState)(null),
    _useState24 = _slicedToArray(_useState23, 2),
    nightTarget = _useState24[0],
    setNightTarget = _useState24[1];
  var _useState25 = (0, _react.useState)([]),
    _useState26 = _slicedToArray(_useState25, 2),
    discussion = _useState26[0],
    setDiscussion = _useState26[1];
  var _useState27 = (0, _react.useState)(null),
    _useState28 = _slicedToArray(_useState27, 2),
    animation = _useState28[0],
    setAnimation = _useState28[1];
  var chatContainerRef = (0, _react.useRef)(null);
  (0, _react.useEffect)(function () {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [discussion]);
  var loadGameState = /*#__PURE__*/function () {
    var _ref24 = _asyncToGenerator(/*#__PURE__*/_regeneratorRuntime().mark(function _callee12() {
      var state;
      return _regeneratorRuntime().wrap(function _callee12$(_context12) {
        while (1) switch (_context12.prev = _context12.next) {
          case 0:
            setLoading(true);
            _context12.prev = 1;
            _context12.next = 4;
            return getGameState(gameId);
          case 4:
            state = _context12.sent;
            setGameState(state);
            _context12.next = 12;
            break;
          case 8:
            _context12.prev = 8;
            _context12.t0 = _context12["catch"](1);
            setError('Failed to load game state');
            console.error(_context12.t0);
          case 12:
            setLoading(false);
          case 13:
          case "end":
            return _context12.stop();
        }
      }, _callee12, null, [[1, 8]]);
    }));
    return function loadGameState() {
      return _ref24.apply(this, arguments);
    };
  }();
  (0, _react.useEffect)(function () {
    loadGameState();
  }, [gameId]);
  var handleStartGame = /*#__PURE__*/function () {
    var _ref25 = _asyncToGenerator(/*#__PURE__*/_regeneratorRuntime().mark(function _callee13() {
      return _regeneratorRuntime().wrap(function _callee13$(_context13) {
        while (1) switch (_context13.prev = _context13.next) {
          case 0:
            setLoading(true);
            _context13.prev = 1;
            _context13.next = 4;
            return startGame(gameId);
          case 4:
            _context13.next = 6;
            return loadGameState();
          case 6:
            _context13.next = 12;
            break;
          case 8:
            _context13.prev = 8;
            _context13.t0 = _context13["catch"](1);
            setError('Failed to start game');
            console.error(_context13.t0);
          case 12:
            setLoading(false);
          case 13:
          case "end":
            return _context13.stop();
        }
      }, _callee13, null, [[1, 8]]);
    }));
    return function handleStartGame() {
      return _ref25.apply(this, arguments);
    };
  }();
  var handleProcessNight = /*#__PURE__*/function () {
    var _ref26 = _asyncToGenerator(/*#__PURE__*/_regeneratorRuntime().mark(function _callee14() {
      var mafiaResult, dawnResult;
      return _regeneratorRuntime().wrap(function _callee14$(_context14) {
        while (1) switch (_context14.prev = _context14.next) {
          case 0:
            setLoading(true);
            _context14.prev = 1;
            // Process mafia action
            setAnimation('mafia');
            _context14.next = 5;
            return processNight(gameId);
          case 5:
            mafiaResult = _context14.sent;
            setNightTarget(mafiaResult.actions.mafia_target);

            // Wait for animation
            _context14.next = 9;
            return new Promise(function (resolve) {
              return setTimeout(resolve, 5000);
            });
          case 9:
            // Process detective action
            setAnimation('detective');
            setNightTarget(mafiaResult.actions.detective_target);

            // Wait for animation
            _context14.next = 13;
            return new Promise(function (resolve) {
              return setTimeout(resolve, 5000);
            });
          case 13:
            // Process doctor action
            setAnimation('doctor');
            setNightTarget(mafiaResult.actions.doctor_target);

            // Wait for animation
            _context14.next = 17;
            return new Promise(function (resolve) {
              return setTimeout(resolve, 5000);
            });
          case 17:
            setAnimation(null);
            setNightTarget(null);

            // Resolve night
            _context14.next = 21;
            return resolveNight(gameId);
          case 21:
            dawnResult = _context14.sent;
            _context14.next = 24;
            return loadGameState();
          case 24:
            _context14.next = 30;
            break;
          case 26:
            _context14.prev = 26;
            _context14.t0 = _context14["catch"](1);
            setError('Failed to process night');
            console.error(_context14.t0);
          case 30:
            setLoading(false);
          case 31:
          case "end":
            return _context14.stop();
        }
      }, _callee14, null, [[1, 26]]);
    }));
    return function handleProcessNight() {
      return _ref26.apply(this, arguments);
    };
  }();
  var handleStartDiscussion = /*#__PURE__*/function () {
    var _ref27 = _asyncToGenerator(/*#__PURE__*/_regeneratorRuntime().mark(function _callee15() {
      var result;
      return _regeneratorRuntime().wrap(function _callee15$(_context15) {
        while (1) switch (_context15.prev = _context15.next) {
          case 0:
            setLoading(true);
            _context15.prev = 1;
            _context15.next = 4;
            return startDiscussion(gameId);
          case 4:
            _context15.next = 6;
            return simulateDiscussion(gameId);
          case 6:
            result = _context15.sent;
            setDiscussion(result.discussion);
            _context15.next = 10;
            return loadGameState();
          case 10:
            _context15.next = 16;
            break;
          case 12:
            _context15.prev = 12;
            _context15.t0 = _context15["catch"](1);
            setError('Failed to conduct discussion');
            console.error(_context15.t0);
          case 16:
            setLoading(false);
          case 17:
          case "end":
            return _context15.stop();
        }
      }, _callee15, null, [[1, 12]]);
    }));
    return function handleStartDiscussion() {
      return _ref27.apply(this, arguments);
    };
  }();
  var handleProcessVoting = /*#__PURE__*/function () {
    var _ref28 = _asyncToGenerator(/*#__PURE__*/_regeneratorRuntime().mark(function _callee16() {
      var result;
      return _regeneratorRuntime().wrap(function _callee16$(_context16) {
        while (1) switch (_context16.prev = _context16.next) {
          case 0:
            setLoading(true);
            _context16.prev = 1;
            _context16.next = 4;
            return processVoting(gameId);
          case 4:
            result = _context16.sent;
            _context16.next = 7;
            return loadGameState();
          case 7:
            _context16.next = 13;
            break;
          case 9:
            _context16.prev = 9;
            _context16.t0 = _context16["catch"](1);
            setError('Failed to process voting');
            console.error(_context16.t0);
          case 13:
            setLoading(false);
          case 14:
          case "end":
            return _context16.stop();
        }
      }, _callee16, null, [[1, 9]]);
    }));
    return function handleProcessVoting() {
      return _ref28.apply(this, arguments);
    };
  }();
  var handleResetGame = /*#__PURE__*/function () {
    var _ref29 = _asyncToGenerator(/*#__PURE__*/_regeneratorRuntime().mark(function _callee17() {
      return _regeneratorRuntime().wrap(function _callee17$(_context17) {
        while (1) switch (_context17.prev = _context17.next) {
          case 0:
            setLoading(true);
            _context17.prev = 1;
            _context17.next = 4;
            return resetGame(gameId);
          case 4:
            setDiscussion([]);
            setNightAction(null);
            setNightTarget(null);
            _context17.next = 9;
            return loadGameState();
          case 9:
            _context17.next = 15;
            break;
          case 11:
            _context17.prev = 11;
            _context17.t0 = _context17["catch"](1);
            setError('Failed to reset game');
            console.error(_context17.t0);
          case 15:
            setLoading(false);
          case 16:
          case "end":
            return _context17.stop();
        }
      }, _callee17, null, [[1, 11]]);
    }));
    return function handleResetGame() {
      return _ref29.apply(this, arguments);
    };
  }();
  if (loading && !gameState) {
    return /*#__PURE__*/_react.default.createElement("div", {
      className: "p-8 text-center"
    }, "Loading game...");
  }
  if (error) {
    return /*#__PURE__*/_react.default.createElement(_alert.Alert, {
      variant: "destructive",
      className: "m-4"
    }, /*#__PURE__*/_react.default.createElement(_lucideReact.AlertCircle, {
      className: "h-4 w-4"
    }), /*#__PURE__*/_react.default.createElement(_alert.AlertTitle, null, "Error"), /*#__PURE__*/_react.default.createElement(_alert.AlertDescription, null, error));
  }
  if (!gameState) {
    return /*#__PURE__*/_react.default.createElement("div", {
      className: "p-8 text-center"
    }, "Game not found");
  }
  return /*#__PURE__*/_react.default.createElement("div", {
    className: "container mx-auto p-4"
  }, /*#__PURE__*/_react.default.createElement("div", {
    className: "flex justify-between items-center mb-4"
  }, /*#__PURE__*/_react.default.createElement("div", {
    className: "text-2xl font-bold"
  }, "Mafia Game"), /*#__PURE__*/_react.default.createElement("div", {
    className: "flex gap-2"
  }, /*#__PURE__*/_react.default.createElement(_badge.Badge, {
    variant: gameState.phase === 'setup' ? 'default' : 'outline'
  }, "Setup"), /*#__PURE__*/_react.default.createElement(_badge.Badge, {
    variant: gameState.phase === 'night' ? 'default' : 'outline'
  }, "Night"), /*#__PURE__*/_react.default.createElement(_badge.Badge, {
    variant: gameState.phase === 'dawn' ? 'default' : 'outline'
  }, "Dawn"), /*#__PURE__*/_react.default.createElement(_badge.Badge, {
    variant: gameState.phase === 'discussion' ? 'default' : 'outline'
  }, "Discussion"), /*#__PURE__*/_react.default.createElement(_badge.Badge, {
    variant: gameState.phase === 'voting' ? 'default' : 'outline'
  }, "Voting")), /*#__PURE__*/_react.default.createElement("div", null, "Round: ", gameState.round || 0)), gameState.game_over && /*#__PURE__*/_react.default.createElement(_alert.Alert, {
    className: "mb-4 bg-yellow-50"
  }, /*#__PURE__*/_react.default.createElement(_lucideReact.CheckCircle, {
    className: "h-4 w-4"
  }), /*#__PURE__*/_react.default.createElement(_alert.AlertTitle, null, "Game Over!"), /*#__PURE__*/_react.default.createElement(_alert.AlertDescription, null, "The ", gameState.winner, " team wins!")), /*#__PURE__*/_react.default.createElement("div", {
    className: "grid grid-cols-3 gap-4 mb-4"
  }, /*#__PURE__*/_react.default.createElement(_card.Card, null, /*#__PURE__*/_react.default.createElement(_card.CardHeader, null, /*#__PURE__*/_react.default.createElement(_card.CardTitle, {
    className: "flex items-center gap-2"
  }, /*#__PURE__*/_react.default.createElement(_lucideReact.Users, {
    className: "h-5 w-5"
  }), " Players")), /*#__PURE__*/_react.default.createElement(_card.CardContent, {
    className: "space-y-2"
  }, (_gameState$players = gameState.players) === null || _gameState$players === void 0 ? void 0 : _gameState$players.map(function (player) {
    return /*#__PURE__*/_react.default.createElement("div", {
      key: player.name,
      className: "flex items-center justify-between"
    }, /*#__PURE__*/_react.default.createElement("div", {
      className: "flex items-center gap-2"
    }, !player.alive && /*#__PURE__*/_react.default.createElement(_lucideReact.Skull, {
      className: "h-4 w-4 text-red-500"
    }), /*#__PURE__*/_react.default.createElement("span", null, player.name)), /*#__PURE__*/_react.default.createElement(_badge.Badge, null, player.personality));
  }))), /*#__PURE__*/_react.default.createElement(_card.Card, {
    className: "col-span-2"
  }, /*#__PURE__*/_react.default.createElement(_card.CardHeader, null, /*#__PURE__*/_react.default.createElement(_card.CardTitle, {
    className: "flex items-center gap-2"
  }, /*#__PURE__*/_react.default.createElement(_lucideReact.AlertCircle, {
    className: "h-5 w-5"
  }), " Game Events")), /*#__PURE__*/_react.default.createElement(_card.CardContent, {
    className: "h-40 overflow-auto"
  }, /*#__PURE__*/_react.default.createElement("ul", {
    className: "space-y-1"
  }, (_gameState$events = gameState.events) === null || _gameState$events === void 0 ? void 0 : _gameState$events.map(function (event, i) {
    return /*#__PURE__*/_react.default.createElement("li", {
      key: i,
      className: "text-sm border-l-2 border-blue-300 pl-2"
    }, event);
  }))))), animation && /*#__PURE__*/_react.default.createElement(_card.Card, {
    className: "mb-4"
  }, /*#__PURE__*/_react.default.createElement(_card.CardContent, {
    className: "p-6"
  }, /*#__PURE__*/_react.default.createElement(NightActionAnimation, {
    action: animation,
    target: nightTarget,
    complete: function complete() {}
  }))), gameState.phase === 'setup' && /*#__PURE__*/_react.default.createElement(_card.Card, {
    className: "mb-4"
  }, /*#__PURE__*/_react.default.createElement(_card.CardContent, {
    className: "p-6"
  }, /*#__PURE__*/_react.default.createElement("div", {
    className: "text-center"
  }, /*#__PURE__*/_react.default.createElement("p", {
    className: "mb-4"
  }, "All players have been assigned personalities. Ready to begin?"), /*#__PURE__*/_react.default.createElement(_button.Button, {
    onClick: handleStartGame
  }, "Begin Game")))), gameState.phase === 'night' && !animation && /*#__PURE__*/_react.default.createElement(_card.Card, {
    className: "mb-4"
  }, /*#__PURE__*/_react.default.createElement(_card.CardHeader, null, /*#__PURE__*/_react.default.createElement(_card.CardTitle, {
    className: "flex items-center gap-2"
  }, /*#__PURE__*/_react.default.createElement(_lucideReact.Moon, {
    className: "h-5 w-5"
  }), " Night Phase")), /*#__PURE__*/_react.default.createElement(_card.CardContent, {
    className: "p-6"
  }, /*#__PURE__*/_react.default.createElement("div", {
    className: "text-center"
  }, /*#__PURE__*/_react.default.createElement("p", {
    className: "mb-4"
  }, "Night has fallen. The Mafia, Detective, and Doctor will make their moves..."), /*#__PURE__*/_react.default.createElement(_button.Button, {
    onClick: handleProcessNight
  }, "Process Night Actions")))), gameState.phase === 'dawn' && /*#__PURE__*/_react.default.createElement(_card.Card, {
    className: "mb-4"
  }, /*#__PURE__*/_react.default.createElement(_card.CardHeader, null, /*#__PURE__*/_react.default.createElement(_card.CardTitle, {
    className: "flex items-center gap-2"
  }, /*#__PURE__*/_react.default.createElement(_lucideReact.Sun, {
    className: "h-5 w-5"
  }), " Dawn Announcement")), /*#__PURE__*/_react.default.createElement(_card.CardContent, {
    className: "p-6"
  }, /*#__PURE__*/_react.default.createElement("div", {
    className: "text-center"
  }, /*#__PURE__*/_react.default.createElement("p", {
    className: "mb-4"
  }, "The sun rises on a new day. Time for the town to discuss what happened."), /*#__PURE__*/_react.default.createElement(_button.Button, {
    onClick: handleStartDiscussion
  }, "Begin Discussion")))), (gameState.phase === 'discussion' || discussion.length > 0) && /*#__PURE__*/_react.default.createElement(_card.Card, {
    className: "mb-4"
  }, /*#__PURE__*/_react.default.createElement(_card.CardHeader, null, /*#__PURE__*/_react.default.createElement(_card.CardTitle, {
    className: "flex items-center gap-2"
  }, /*#__PURE__*/_react.default.createElement(_lucideReact.MessageSquare, {
    className: "h-5 w-5"
  }), " Town Discussion")), /*#__PURE__*/_react.default.createElement(_card.CardContent, null, /*#__PURE__*/_react.default.createElement("div", {
    className: "h-96 overflow-auto p-2",
    ref: chatContainerRef
  }, discussion.map(function (line, i) {
    if (line.startsWith('---')) {
      return /*#__PURE__*/_react.default.createElement("div", {
        key: i,
        className: "text-center text-gray-500 my-4"
      }, line);
    }
    var colonIndex = line.indexOf(':');
    if (colonIndex > 0) {
      var _gameState$players2;
      var playerName = line.substring(0, colonIndex);
      var message = line.substring(colonIndex + 1).trim();
      var player = (_gameState$players2 = gameState.players) === null || _gameState$players2 === void 0 ? void 0 : _gameState$players2.find(function (p) {
        return p.name === playerName;
      });
      var isDead = player && !player.alive;
      return /*#__PURE__*/_react.default.createElement(ChatBubble, {
        key: i,
        player: playerName,
        message: message,
        isDead: isDead
      });
    }
    return /*#__PURE__*/_react.default.createElement("div", {
      key: i
    }, line);
  }))), /*#__PURE__*/_react.default.createElement(_card.CardFooter, {
    className: "justify-center"
  }, gameState.phase === 'discussion' && /*#__PURE__*/_react.default.createElement(_button.Button, {
    onClick: handleProcessVoting
  }, "Proceed to Voting"))), gameState.game_over && /*#__PURE__*/_react.default.createElement("div", {
    className: "flex justify-center"
  }, /*#__PURE__*/_react.default.createElement(_button.Button, {
    size: "lg",
    onClick: handleResetGame
  }, "Play Again")));
};
var MafiaGame = function MafiaGame() {
  var _useState29 = (0, _react.useState)(null),
    _useState30 = _slicedToArray(_useState29, 2),
    gameId = _useState30[0],
    setGameId = _useState30[1];
  var _useState31 = (0, _react.useState)(false),
    _useState32 = _slicedToArray(_useState31, 2),
    gameStarted = _useState32[0],
    setGameStarted = _useState32[1];
  var handleStartGame = /*#__PURE__*/function () {
    var _ref30 = _asyncToGenerator(/*#__PURE__*/_regeneratorRuntime().mark(function _callee18(personalities) {
      var result;
      return _regeneratorRuntime().wrap(function _callee18$(_context18) {
        while (1) switch (_context18.prev = _context18.next) {
          case 0:
            _context18.prev = 0;
            _context18.next = 3;
            return createGame(personalities);
          case 3:
            result = _context18.sent;
            if (result.game_id) {
              setGameId(result.game_id);
              setGameStarted(true);
            }
            _context18.next = 10;
            break;
          case 7:
            _context18.prev = 7;
            _context18.t0 = _context18["catch"](0);
            console.error('Error starting game:', _context18.t0);
          case 10:
          case "end":
            return _context18.stop();
        }
      }, _callee18, null, [[0, 7]]);
    }));
    return function handleStartGame(_x10) {
      return _ref30.apply(this, arguments);
    };
  }();
  return /*#__PURE__*/_react.default.createElement("div", {
    className: "min-h-screen bg-gray-50"
  }, /*#__PURE__*/_react.default.createElement("header", {
    className: "bg-gray-800 text-white p-4"
  }, /*#__PURE__*/_react.default.createElement("div", {
    className: "container mx-auto"
  }, /*#__PURE__*/_react.default.createElement("h1", {
    className: "text-2xl font-bold"
  }, "AI Mafia Game"))), /*#__PURE__*/_react.default.createElement("main", {
    className: "container mx-auto py-6"
  }, !gameStarted ? /*#__PURE__*/_react.default.createElement(GameSetup, {
    onStartGame: handleStartGame
  }) : /*#__PURE__*/_react.default.createElement(GamePlay, {
    gameId: gameId
  })), /*#__PURE__*/_react.default.createElement("footer", {
    className: "bg-gray-100 p-4 mt-8"
  }, /*#__PURE__*/_react.default.createElement("div", {
    className: "container mx-auto text-center text-gray-500"
  }, "\xA9 2025 AI Mafia Game")));
};
var _default = exports.default = MafiaGame;