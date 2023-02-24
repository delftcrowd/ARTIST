/**
 * Checks if two objects and their contents match each other
 * @param {*} obj1 the first object to be compared
 * @param {*} obj2 the second object to be compared
 * @returns {boolean} true if these are equal, false otherwise
 */
export function deepEquals(obj1, obj2) {
  return JSON.stringify(obj1) === JSON.stringify(obj2);
}

/**
 * Creates a deep copy of an object, given as 'data'
 * @param {*} data multi-dimensional Object that needs to be copied deeply
 * @returns a deep copy of given Object
 */
export function deepCopy(data) {
  return JSON.parse(JSON.stringify(data));
}

/**
 * A method that gives a property a timeout before storing the data.
 * Besides reducing lag, it gives a smoother performance for the user.
 * @param {function} fn the function that will be delayed
 * @param {Number} delay the amount of delay in milliseconds, to be executed
 * @returns {function} a higher order function; executes parameter 'fn' with a delay
 */
export function debounce(fn, delay) {
  var timeoutID = null;

  return function () {
    clearTimeout(timeoutID);
    var args = arguments;
    var that = this;
    timeoutID = setTimeout(function () {
      fn.apply(that, args);
    }, delay);
  };
}
